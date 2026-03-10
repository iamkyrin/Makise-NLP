from classifier import classify_document
from extractor import extract_entities

classify = classify_document("Write a for loop in python")

extractt = extract_entities("Apple, Apple, Apple is the UK of everything")

print(extractt)
