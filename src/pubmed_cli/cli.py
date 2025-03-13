#!/usr/bin/env python3
# src/pubmed_cli/cli.py
import argparse
import logging
import csv
from pubmed_cli.pubmed_module import get_pubmed_articles

def main():
    parser = argparse.ArgumentParser(
        description="Fetch PubMed papers with at least one author affiliated with a pharmaceutical/biotech company."
    )
    parser.add_argument("query", help="PubMed query (e.g., 'pharma[AD] OR biotech[AD]')")
    parser.add_argument("-d", "--debug", action="store_true", help="Print debug information during execution.")
    parser.add_argument("-f", "--file", help="Filename to save the results as CSV. If not provided, output will be printed to the console.")
    parser.add_argument("--max", type=int, default=10, help="Maximum number of results to fetch (default: 10)")
    args = parser.parse_args()

    # Configure logging based on debug flag
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.debug("Starting query with: %s", args.query)
    try:
        articles_data = get_pubmed_articles(args.query, max_results=args.max)
    except Exception as e:
        logging.error("Error fetching data: %s", e)
        return

    if args.file:
        # Write results to CSV file
        keys = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]
        try:
            with open(args.file, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                writer.writeheader()
                writer.writerows(articles_data)
            logging.info("Results saved to file: %s", args.file)
        except Exception as e:
            logging.error("Error writing to file %s: %s", args.file, e)
    else:
        # Print the results to the console
        for article in articles_data:
            print("PubmedID:", article["PubmedID"])
            print("Title:", article["Title"])
            print("Publication Date:", article["Publication Date"])
            print("Non-academic Author(s):", article["Non-academic Author(s)"])
            print("Company Affiliation(s):", article["Company Affiliation(s)"])
            print("Corresponding Author Email:", article["Corresponding Author Email"])
            print("-" * 80)

if __name__ == "__main__":
    main()
