#!/bin/bash

# F5-TTS Inference Web Server Launcher
echo "🚀 Starting F5-TTS Inference Web Server..."

# Activate the local pytorch virtual environment
source /home/ubuntu/F5-TTS/pytorch_venv/bin/activate

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "❌ Error: Failed to activate pytorch virtual environment"
    exit 1
fi

# Navigate to F5-TTS directory
cd /home/ubuntu/F5-TTS

# Check if we're in the right directory
if [[ ! -f "README.md" ]]; then
    echo "❌ Error: Not in F5-TTS directory"
    exit 1
fi

# Check if F5-TTS is installed
if ! command -v f5-tts_infer-gradio &> /dev/null; then
    echo "❌ Error: f5-tts_infer-gradio command not found"
    echo "Please ensure F5-TTS is properly installed"
    exit 1
fi

echo "✅ Environment: $VIRTUAL_ENV"
echo "✅ Directory: $(pwd)"
echo "✅ Starting F5-TTS Inference Web Interface..."
echo ""
echo "🌐 Web Interfaces will be available at:"
echo "   - F5-TTS Local:   http://localhost:7860"
echo "   - F5-TTS Network: http://0.0.0.0:7860"
echo "   - Voice API:      http://0.0.0.0:7861"
echo ""
echo "Press Ctrl+C to stop the servers"
echo "----------------------------------------"

# Launch Voice Saver API (Gradio) on 7861 in background, log to file
echo "▶️  Starting Voice Saver API on 7861..."
source /home/ubuntu/F5-TTS/pytorch_venv/bin/activate
nohup python /home/ubuntu/voice_api.py > /home/ubuntu/voice_api_stdout.log 2>&1 &
VOICE_API_PID=$!
deactivate

# Launch F5-TTS inference with web interface (foreground)
f5-tts_infer-gradio --host 0.0.0.0 --port 7860