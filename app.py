from flask import Flask, render_template, request, jsonify
from lula_finder import process_chat_file, generate_results_html
from flask_compress import Compress
import os

app = Flask(__name__)
Compress(app)  # Enable response compression
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB limit

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

        if not file.filename.lower().endswith('.txt'):
            return jsonify(error="Formato inválido! Use .txt"), 400

        # Read with size validation
        file_data = file.read(4 * 1024 * 1024)  # 4MB
        if len(file_data) == 4 * 1024 * 1024:
            return jsonify(error="Arquivo muito grande (máx. 4MB)"), 400

        file_content = file_data.decode('utf-8')
        counts = process_chat_file(file_content)
        return jsonify(results=generate_results_html(counts))

    except UnicodeDecodeError:
        return jsonify(error="Arquivo com codificação inválida"), 400
    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}")
        return jsonify(error=f"Erro interno: {str(e)}"), 500

# Vercel handler remains the same
def vercel_handler(request):
    with app.app_context():
        response = app.full_dispatch_request()
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data().decode('utf-8')
        }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))