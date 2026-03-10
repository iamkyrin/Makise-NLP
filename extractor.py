import spacy

nlp = spacy.load("en_core_web_sm")
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
