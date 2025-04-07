from flask import Flask, render_template, request, jsonify
from lula_finder import process_chat_file, generate_results_html
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('LulaFinderNoPython.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify(error="Nenhum arquivo enviado!"), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="Nome de arquivo inválido!"), 400
    
    if file and file.filename.endswith('.txt'):
        file_content = file.read().decode('utf-8')
        counts = process_chat_file(file_content)
        results_html = generate_results_html(counts)
        return jsonify(results=results_html)
    
    return jsonify(error="Formato de arquivo inválido! Use .txt"), 400

if __name__ == '__main__':
    app.run(debug=True)