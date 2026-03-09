from transformers import pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
def classify_document(text):

    candidate_labels = ['Research Paper', 'Legal Documents', 'Academic Paper', 'Academic Report',
                        'Medical Report', 'Technical Documentation', 'News article',
                        'Financial Paper', 'Coding', 'Programming', 'Data science paper']
    result = classifier(text, candidate_labels)
    multiplier = 100
    result2 = [item * multiplier for item in result['scores']]
    """print(result2)
    print(result)
    print(f"Highest Probability: {result['labels'][0]}")
    print(f"Second Highest Probability {result['labels'][1]}")"""

    return result['labels'][0]

# classify_document("Write a for loop in python")

