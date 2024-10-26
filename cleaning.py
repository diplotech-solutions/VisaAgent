import re

contractions = {
    "'s": " is",
    "n't": " not",
    "'m": " am",
    "'ll": " will",
    "'d": " would",
    "'ve": " have",
    "'re": " are",
}

def clean_text(text):
    for contraction, full_form in contractions.items():
        text = text.replace(contraction, full_form)

    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    text = text.lower()

    return text

if __name__ == "__main__":
    sample_text = "The website's link isn't working. Check http://example.com"
    cleaned_text = clean_text(sample_text)
    print("Cleaned text: ", cleaned_text)
