import spacy
import subprocess
import sys
import os

def load_nlp():
    model_name = "en_core_web_sm"

    try:
        # Try to load the model
        return spacy.load(model_name)
    except OSError:
        # Download the model using spaCy's built-in method
        print(f"Downloading {model_name}...")
        spacy.cli.download(model_name)
        return spacy.load(model_name)

nlp = load_nlp()
def extract_entities(text):
    docList = {}
    count = {}
    x = 0
    doc = nlp(text)
    for ent in doc.ents:
        if ent.text not in docList.keys():
           count[ent.text] = 1
        elif ent.text in docList.keys():
           count[ent.text] += 1

        key = f"{ent.text}_{count[ent.text]}"

        docList[ent.text] = ent.label_
        docList[key] = ent.label_
    return docList
