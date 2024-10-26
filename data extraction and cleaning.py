"""
FURTHER DEVELOPMENT IN THIS SCRIPT:
1. Develop the scraping function to categorize the text based on types: Normal text, tables, etc..., and store them appropriately like CSV for tables, plain text for normal text
2. Develop the cleaning process to handle different text types accordingly
3. Update the 'Website' keyword to accept multiple URLs as input for scraping and process them in loop
"""

import requests
from bs4 import BeautifulSoup
import re
import csv


def scrape_website(website):
    response = requests.get(website)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Targeting the specific section of the page containing the visa information
    main_content = soup.find('div', class_='c-rte--default')

    # Check if the page contains table-like data
    table = soup.find('table')
    if table:
        # Extract table headers
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        rows = []

        # Extract table rows
        for row in table.find_all('tr')[1:]:
            rows.append([td.get_text(strip=True) for td in row.find_all('td')])

        # Save table data to CSV
        with open('visa_requirements.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        return "Table data extracted and saved to CSV."

    if main_content:
        return main_content.get_text()

    return ""


def clean_text(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    # Now assigning the cleaned content to text for contractions
    text = cleaned_content.lower()

    contractions = {
        "'s": " is",
        "n't": " not",
        "'m": " am",
        "'ll": " will",
        "'d": " would",
        "'ve": " have",
        "'re": " are",
    }

    for contraction, full_form in contractions.items():
        text = text.replace(contraction, full_form)

    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]


def scrape_and_process(website):
    raw_html = scrape_website(website)

    if "Table data extracted" not in raw_html:  # Check if table was processed
        cleaned_body_content = clean_text(raw_html)
        split_content = split_dom_content(cleaned_body_content)
        return split_content
    else:
        return raw_html  # Return message about table extraction


website = "https://manama.diplo.de/bh-en/service/05-VisaEinreise/visa/1731254"

processed_content = scrape_and_process(website)
print(processed_content)



"""
def scrape_website(website):
    response = requests.get(website)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Targeting the specific section of the page containing the visa information
    main_content = soup.find('div', class_='c-rte--default')

    # Check if the page contains table-like data
    table = soup.find('table')
    if table:
        # Extract table headers
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        rows = []

        # Extract table rows
        for row in table.find_all('tr')[1:]:
            rows.append([td.get_text(strip=True) for td in row.find_all('td')])

        # Save table data to CSV
        with open('visa_requirements.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

        return "Table data extracted and saved to CSV."

    if main_content:
        return main_content.get_text()

    return ""
"""