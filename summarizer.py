from transformers import BartForConditionalGeneration, BartTokenizer
summarizer = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

def summarize(text, output_choice):
    max_length = 0
    min_length = 0
    inputs = tokenizer(text, return_tensors="pt")
    if output_choice == "Short":
        max_length = 40
        min_length = 15
    elif output_choice == "Medium":
        max_length = 120
        min_length = 60
    elif output_choice == "Detailed":
        max_length = 200
        min_length = 120

    generated_text = summarizer.generate(**inputs, max_length=max_length, min_length=min_length)
    decode = tokenizer.decode(generated_text[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return decode