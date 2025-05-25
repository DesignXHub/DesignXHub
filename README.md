# DesignXHub
AI-powered platform to generate 3D models in Blender using natural language.

## Setup Instructions:
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place your model file here:
`server/models/deepseek-coder-6.7b-instruct.Q4_0.gguf`

3. Run the server:
```bash
cd server && python app.py
```

4. In Blender:
- Open `blender_watcher.py`
- Click Run Script

Then use the frontend in `web/index.html`.