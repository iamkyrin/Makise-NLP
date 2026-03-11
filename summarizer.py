from transformers import BartForConditionalGeneration, BartTokenizer

summarizer = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

def summarize(text):
    inputs = tokenizer(text, return_tensors="pt")

    generated_text = summarizer.generate(**inputs, max_length=130, min_length=30)
    decode = tokenizer.decode(generated_text[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return decode