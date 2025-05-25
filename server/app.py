from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gpt4all import GPT4All
import os

app = Flask(__name__)
CORS(app)

SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../blender_scripts"))
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "models"))

model = GPT4All(
    model_name="deepseek-coder-6.7b-instruct.Q4_0.gguf",
    model_path=MODEL_PATH,
    allow_download=False
)

@app.route('/generate', methods=['POST'])
def generate_code():
    data = request.get_json()
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "No prompt provided!"}), 400

    try:
        system_prompt = """You are a Blender Python expert. Write code that:
        1. Deletes all existing objects
        2. Uses only 'bpy' and 'mathutils' modules
        3. Adds camera and lighting
        4. Outputs ONLY code, no comments"""

        full_prompt = f"### System:\n{system_prompt}\n### User:\n{prompt}\n### Assistant:"

        response = model.generate(
            full_prompt,
            max_tokens=2000,
            temp=0.5,
            n_batch=512
        )
        code = response.strip()

        with open(os.path.join(SCRIPT_DIR, "auto_script.py"), 'w', encoding='utf-8') as f:
            f.write(code)

        return jsonify({"code": code})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/render')
def get_render():
    return send_from_directory(os.path.join(SCRIPT_DIR, "output"), "render.png")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
