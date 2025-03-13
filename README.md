# PubMed CLI Tool

The **PubMed CLI Tool** is a command-line application that fetches PubMed papers with at least one author affiliated with a pharmaceutical or biotech company. It supports the full PubMed query syntax, allowing for advanced and flexible searches.

## Code Organization

The project is organized using a modular structure along with Poetry for dependency management and packaging. The key components are:

- **pyproject.toml:**  
  Contains the project metadata, dependencies, and configuration for Poetry. It also defines an executable command (`get-papers-list`) which launches the CLI tool.

- **README.md:**  
  This file, which explains the project details, installation instructions, usage, and tools used.

- **src/pubmed_cli/**  
  This directory contains the application code:
  - **`pubmed_module.py`:**  
    Contains functions to interact with the PubMed E-utilities API. It handles querying PubMed (using ESearch and EFetch), parsing XML responses, and filtering articles to find those with company-affiliated authors.
  
  - **`cli.py`:**  
    Implements the command-line interface (CLI). It uses Python's `argparse` module to process command-line arguments (e.g., query string, debug flag, output file option) and displays the fetched results accordingly.

  - **`__init__.py`:**  
    An empty file that marks the `pubmed_cli` directory as a Python package.

## Installation and Execution

### Prerequisites

- **Python 3.8 or higher:**  
  Download and install Python from [python.org](https://www.python.org/).

- **Poetry:**  
  Poetry is used for dependency management and packaging. Follow the [Poetry installation guide](https://python-poetry.org/docs/#installation) to install it on your system.

### Steps to Install and Run

1. **Clone the Repository:**

```bash
git clone <repository-url>
cd pubmed-cli
```

## Installation and Execution

### Install Dependencies

In your project directory, run:

```bash
poetry install
# This command reads the pyproject.toml file and installs the required dependencies (e.g., requests).
```

## Execute the CLI Tool
Use the executable command defined in the pyproject.toml file. For example:

### Run a Query and Save to CSV
This command runs the query with debug logging enabled, fetches up to 20 results, and saves the output to results.csv:

```bash
poetry run get-papers-list "pharma[AD] OR biotech[AD]" -d -f results.csv --max 20
```

### Run a Query and Print to Console
This command runs a query for papers with "cancer" in the title published in 2021, prints debug information, and displays up to 15 results on the console:

```bash
poetry run get-papers-list "cancer[Title] AND 2021[DP]" -d --max 15
```

### Display Help Information
To see all available options and usage instructions, run:

```bash
poetry run get-papers-list -h
```
## Usage Details
The CLI tool accepts a full PubMed query as a positional argument. You can use any valid query string supported by PubMed's search engine. Additional options include:

Positional Argument: Query
The query string (e.g., "diabetes[Title]" or a more complex query like ("("cancer"[Title] AND "2020"[DP]) OR "diabetes"[Title]")) is used to search the PubMed database.

# Usage Details

The CLI tool accepts a full **PubMed query** as a **positional argument**. You can use any valid query string supported by PubMed's search engine. Additional options include:

## **Positional Argument: Query**
The query string (e.g., `"diabetes[Title]"` or a more complex query like `("("cancer"[Title] AND "2020"[DP]) OR "diabetes"[Title]")`) is used to search the PubMed database.

## **Options**
### `-d` or `--debug`
Enables **debug logging**, which prints detailed information about the execution process.

### `-f` or `--file`
Specifies the **filename** for saving the output as a **CSV file**. If this option is not provided, the output is printed to the console.

### `--max`
Sets the **maximum number of results** to fetch (**default: 10**).

# Output Details

For each fetched paper, the CLI tool retrieves and displays the following information:

- **PubmedID**: Unique identifier for the paper.  
- **Title**: The title of the paper.  
- **Publication Date**: Date when the paper was published.  
- **Non-academic Author(s)**: Names of authors with affiliations indicating a pharmaceutical or biotech company.  
- **Company Affiliation(s)**: The affiliation details of the non-academic authors.  
- **Corresponding Author Email**: Email address of the corresponding author (if available).  

If the `--file` option is used, the output is saved as a **CSV file** with headers corresponding to the fields above.

## Python
The program is written in Python (version 3.8 or higher).  
[Python Official Website](https://www.python.org/)

## Poetry
Poetry is used for dependency management, packaging, and creating executable commands.  
[Poetry Official Documentation](https://python-poetry.org/docs/)

## Requests
The `requests` library is used to handle HTTP requests to the PubMed API.  
[Requests Library on PyPI](https://pypi.org/project/requests/)

## PubMed E-utilities API
The tool interacts with the PubMed API using the E-utilities (`ESearch` and `EFetch`) for querying and fetching data from PubMed.  
[NCBI E-utilities Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25500/)

## LLMs for Code Assistance
This code was designed with the assistance of a large language model (LLM- GPT-o3-mini) to help structure and generate Python code examples.

## License
This project is licensed under the **MIT License**.