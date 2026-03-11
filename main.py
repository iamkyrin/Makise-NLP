from classifier import classify_document
from extractor import extract_entities
from summarizer import summarize

text = """Tesla CEO Elon Musk announced plans to expand the company's Gigafactory in Austin, Texas. The factory, which currently employs over 20,000 workers, will add a new production line for the upcoming Model Y refresh. The expansion is expected to cost $2 billion and create 5,000 new jobs in the region. Texas Governor Greg Abbott welcomed the announcement, calling it a major win for the state's economy."""
classify = classify_document(text)
extract = extract_entities(text)
summary = summarize(text)
print(f"Classify - {classify}")
print(f"Extract - {extract}")
print(f"Summary - {summary}")
