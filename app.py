from flask import Flask, render_template, request, jsonify
from lula_finder import process_chat_file, generate_results_html
import os

app = Flask(__name__)

# Disable debug mode for production
app.debug = False

@app.route('/')
def index():
    return render_template('LulaFinder.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'file' not in request.files:
            return jsonify(error="Nenhum arquivo enviado!"), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify(error="Nome de arquivo inválido!"), 400
        
        if file and file.filename.endswith('.txt'):
            # Read with size limit (10MB)
            file_content = file.read(10 * 1024 * 1024).decode('utf-8')
            counts = process_chat_file(file_content)
            results_html = generate_results_html(counts)
            return jsonify(results=results_html)
        
        return jsonify(error="Formato de arquivo inválido! Use .txt"), 400

    except Exception as e:
        return jsonify(error=f"Erro interno: {str(e)}"), 500

# Vercel serverless function handler
def vercel_handler(request):
    with app.app_context():
        # Convert Vercel request to Flask request
        with request.request:
            response = app.full_dispatch_request()
        
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data().decode('utf-8')
        }

# Local development
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))