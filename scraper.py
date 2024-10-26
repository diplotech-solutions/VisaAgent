import requests
from bs4 import BeautifulSoup
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_website(website):
    try:
        response = requests.get(website)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        main_content = soup.find('div', class_='c-rte--default')
        if main_content:
            logging.info(f"Successfully scraped content from {website}")
            return main_content.get_text()
        else:
            logging.warning(f"No main content found for {website}")
            return ""
    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while fetching {website}: {e}")
        return ""

def clean_text(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    text = cleaned_content.lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

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

    return text

def scrape_and_process(websites):
    all_cleaned_content = []
    for website in websites:
        raw_html = scrape_website(website)
        if raw_html:
            cleaned_content = clean_text(raw_html)
            all_cleaned_content.append((website, cleaned_content))
        else:
            logging.warning(f"Skipping website due to missing content: {website}")
    return all_cleaned_content



