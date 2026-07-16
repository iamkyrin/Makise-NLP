import spacy
import subprocess
import sys
import os

def load_nlp():
    model_name = "en_core_web_sm"

    try:
        return spacy.load(model_name)
    except OSError:
        print(f"Downloading {model_name}...")
        subprocess.run([
            sys.executable,
            "-m",
            "spacy",
            "download",
            model_name,
            "--user"
        ], check=True)
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
