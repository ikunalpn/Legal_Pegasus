from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import pdfplumber

def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages])
    return text
tokenizer = AutoTokenizer.from_pretrained("akhilm97/pegasus_indian_legal")
model = AutoModelForSeq2SeqLM.from_pretrained("akhilm97/pegasus_indian_legal")

def summarize_text(text):
    input_tokenized = tokenizer.encode(text, return_tensors='pt', max_length=1024, truncation=True)
    summary_ids = model.generate(input_tokenized,
                                num_beams=9,
                                no_repeat_ngram_size=3,
                                length_penalty=2.0,
                                min_length=150,
                                max_length=300,
                                early_stopping=True)
    summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids][0]
    return summary
