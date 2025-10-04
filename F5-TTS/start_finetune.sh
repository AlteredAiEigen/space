#!/bin/bash

# F5-TTS Finetuning Web Server Launcher
echo "🔧 Starting F5-TTS Finetuning Web Server..."

# Activate the pytorch conda environment
source ~/miniconda/etc/profile.d/conda.sh
conda activate pytorch

# Check if conda environment is activated
if [[ "$CONDA_DEFAULT_ENV" != "pytorch" ]]; then
    echo "❌ Error: Failed to activate pytorch environment"
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
if ! command -v f5-tts_finetune-gradio &> /dev/null; then
    echo "❌ Error: f5-tts_finetune-gradio command not found"
    echo "Please ensure F5-TTS is properly installed"
    exit 1
fi

echo "✅ Environment: $CONDA_DEFAULT_ENV"
echo "✅ Directory: $(pwd)"
echo "✅ Starting F5-TTS Finetuning Web Interface..."
echo ""
echo "🌐 Web Interface will be available at:"
echo "   - Local: http://localhost:7860"
echo "   - Network: http://0.0.0.0:7860"
echo ""
echo "⚠️  Note: Finetuning requires significant GPU memory and training data"
echo "Press Ctrl+C to stop the server"
echo "----------------------------------------"

# Launch F5-TTS finetuning with web interface
f5-tts_finetune-gradio 