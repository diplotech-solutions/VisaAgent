# main.py

from scraper import scrape_and_process
from train import train_model
from datasets import Dataset


def main():
    websites = [
        "https://www.auswaertiges-amt.de/en/visa-service/-/231148",
        "https://manama.diplo.de/bh-en/service/05-VisaEinreise/visabestimmungen/1706736"
    ]

    cleaned_content_list = scrape_and_process(websites)

    text_data = [content for _, content in cleaned_content_list]

    dataset = Dataset.from_dict({"text": text_data})

    #print(dataset)

    train_model(dataset)


if __name__ == "__main__":
    main()
