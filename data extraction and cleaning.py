import requests
from bs4 import BeautifulSoup
import re


def scrape_website(website):
    response = requests.get(website)
    soup = BeautifulSoup(response.content, 'html.parser')

    main_content = soup.find('div', class_='c-rte--default')

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


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]


def scrape_and_process(website):
    raw_html = scrape_website(website)

    cleaned_body_content = clean_text(raw_html)

    split_content = split_dom_content(cleaned_body_content)

    return split_content

website = ("https://manama.diplo.de/bh-en/service/05-VisaEinreise/visa/1731254")

processed_content = scrape_and_process(website)
print(processed_content)