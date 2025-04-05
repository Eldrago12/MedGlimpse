from flask import Flask, request, jsonify
from flask_cors import CORS
import tempfile
import os
from openai_integration import process_initial_analysis, handle_followup

app = Flask(__name__)
CORS(app)

@app.route('/upload_pdfs', methods=['POST'])
def upload_pdfs():
    print("Received files:", list(request.files.keys()))

    if 'pdfs' not in request.files:
        return jsonify({'error': 'No PDF files uploaded'}), 400

    files = request.files.getlist('pdfs')
    print("Files count:", len(files))

    if len(files) > 3:
        return jsonify({'error': 'Maximum 3 PDF files allowed'}), 400

    temp_paths = []
    try:
        for file in files:
            if not file.filename.lower().endswith('.pdf'):
                return jsonify({'error': 'Only PDF files allowed'}), 400

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            file.save(temp_file.name)
            temp_paths.append(temp_file.name)
            temp_file.close()

        analysis_result = process_initial_analysis(temp_paths)

        for path in temp_paths:
            if os.path.exists(path):
                os.unlink(path)

        if 'error' in analysis_result:
            return jsonify({'error': analysis_result['error']}), 500

        return jsonify({
            'summary': analysis_result.get('summary', ''),
            'citations': analysis_result.get('citations', []),
            'thread_id': analysis_result.get('thread_id', ''),
            'assistant_id': analysis_result.get('assistant_id', '')
        }), 200

    except Exception as e:
        for path in temp_paths:
            if os.path.exists(path):
                os.unlink(path)
        return jsonify({'error': f'Processing error: {str(e)}'}), 500

@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.get_json()

    required_fields = ['thread_id', 'assistant_id', 'question']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing thread_id, assistant_id, or question'}), 400

    try:
        response = handle_followup(
            data['thread_id'],
            data['assistant_id'],
            data['question']
        )

        if 'error' in response:
            return jsonify({'error': response['error']}), 500

        return jsonify({
            'response': response.get('response', 'No response generated')
        }), 200

    except Exception as e:
        return jsonify({'error': f'Question error: {str(e)}'}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File size exceeds 20MB limit'}), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
