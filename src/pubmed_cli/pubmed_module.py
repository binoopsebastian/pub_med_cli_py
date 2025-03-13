# src/pubmed_cli/pubmed_module.py
import requests
import xml.etree.ElementTree as ET
import re

def is_company_affiliated(affiliation):
    """
    Returns True if the affiliation string suggests the author is from a
    pharmaceutical/biotech company.
    """
    keywords = ["pharma", "biotech", "biotechnology", "inc.", "corp", "ltd", "llc", "ag", "sa", "gmbh"]
    return any(keyword in affiliation.lower() for keyword in keywords)

def extract_email(text):
    """
    Extracts an email address from the given text if present.
    """
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def fetch_pubmed_data(query, max_results=10):
    """
    Uses the ESearch utility to fetch PubMed IDs based on the provided query.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "xml"
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    id_list = [id_elem.text for id_elem in root.findall(".//Id")]
    return id_list

def fetch_article_details(pmid):
    """
    Uses the EFetch utility to download article details in XML format for a given PubMed ID.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return ET.fromstring(response.content)

def parse_article(article):
    """
    Extracts the following fields from a PubMedArticle XML element:
      - PubmedID
      - Title
      - Publication Date
      - Non-academic Author(s)
      - Company Affiliation(s)
      - Corresponding Author Email
    """
    pmid = article.findtext(".//PMID")
    title = article.findtext(".//ArticleTitle")
    
    # Extract publication date (try PubDate then ArticleDate)
    pub_date = ""
    pub_date_elem = article.find(".//PubDate")
    if pub_date_elem is not None:
        year = pub_date_elem.findtext("Year")
        month = pub_date_elem.findtext("Month")
        day = pub_date_elem.findtext("Day")
        if year and month and day:
            pub_date = f"{year}-{month}-{day}"
        else:
            pub_date = year if year else ""
    else:
        article_date = article.find(".//ArticleDate")
        if article_date is not None:
            year = article_date.findtext("Year")
            month = article_date.findtext("Month")
            day = article_date.findtext("Day")
            if year and month and day:
                pub_date = f"{year}-{month}-{day}"
            else:
                pub_date = year if year else ""
    
    non_academic_authors = []
    company_affiliations = set()
    corresponding_email = None

    for author in article.findall(".//Author"):
        lastname = author.findtext("LastName")
        forename = author.findtext("ForeName")
        name = f"{forename} {lastname}" if forename and lastname else author.findtext("CollectiveName", default="")
        for aff in author.findall("AffiliationInfo/Affiliation"):
            aff_text = aff.text or ""
            if is_company_affiliated(aff_text):
                non_academic_authors.append(name)
                company_affiliations.add(aff_text)
                if corresponding_email is None:
                    email = extract_email(aff_text)
                    if email:
                        corresponding_email = email

    return {
        "PubmedID": pmid,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Author(s)": "; ".join(non_academic_authors),
        "Company Affiliation(s)": "; ".join(company_affiliations),
        "Corresponding Author Email": corresponding_email if corresponding_email else ""
    }

def get_pubmed_articles(query, max_results=10):
    """
    Orchestrates the process:
      - Fetches a list of PubMed IDs via ESearch.
      - Retrieves and parses each article using EFetch.
      - Returns a list of dictionaries for articles that include at least one non-academic (company affiliated) author.
    """
    articles_data = []
    pmid_list = fetch_pubmed_data(query, max_results=max_results)
    for pmid in pmid_list:
        article_xml = fetch_article_details(pmid)
        article = article_xml.find(".//PubmedArticle")
        if article is not None:
            parsed_data = parse_article(article)
            if parsed_data["Non-academic Author(s)"]:
                articles_data.append(parsed_data)
    return articles_data
