# Visa AI Assistant

This repository provides a solution to automate the scraping, cleaning, and fine-tuning of the LLaMA-3.1-8B model using unsloth AI for assisting in gerneral queries on german visa application.

## Project Structure

- `main.py`: The main script that orchestrates scraping and training.
- `scraper.py`: Handles the website scraping and text cleaning functionality.
- `train.py`: Handles the model training logic.
- `requirements.txt`: Dependencies required to run the project.
- `.gitignore`: Ignore list for unnecessary files to exclude from Git commits.

## Instructions to Run the Code
To get started, clone this repository to your local machine using the following command:

```bash
git clone git@github.com:diplotech-solutions/VisaAgent.git
```

Once cloned, navigate into the repository directory:

```bash
cd VisaAgent
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the main script:

```bash
python main.py
```
