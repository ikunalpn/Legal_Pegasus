from flask import Flask, request, render_template
from utils.legal_pegasus import extract_text_from_pdf, summarize_text
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file uploaded')
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='No file selected')
        if file:
            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)
            text = extract_text_from_pdf(file_path)
            summary = summarize_text(text)
            os.remove(file_path)  # Remove the uploaded file
            return render_template('index.html', summary=summary)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
