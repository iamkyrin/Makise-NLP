from classifier import classify_document
from extractor import extract_entities
from summarizer import summarize

def main(text):
    classify = classify_document(text)
    extract = extract_entities(text)
    summary = summarize(text)
    print(f"Classify - {classify}")
    print(f"Extract - {extract}")
    print(f"Summary - {summary}")
