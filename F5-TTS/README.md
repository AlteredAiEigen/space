Below is the requested Markdown content for the `README.md` file, which has been cleaned and streamlined.

-----

### README.md Content

````markdown
# F5-TTS API Testing & Performance Suite

A testing suite for evaluating F5-TTS API performance, inference, and finetuning capabilities.

## 🚀 Quick Start

### 1. Start the F5-TTS Inference Server
```bash
bash start_inference.sh
````

### 2\. Start the F5-TTS Finetuning Server

```bash
bash start_finetune.sh
```

### 3\. Test API Performance

```bash
# Test with longer texts (initial mode)
python test_response_time.py --mode initial

# Test with shorter texts (cont mode)
python test_response_time.py --mode cont
```

-----

## 📊 Performance Testing

### Response Time Testing

The `test_response_time.py` script tests API performance:

**Features:**

  - Modes: `initial` (longer texts) and `cont` (shorter texts)
  - Saves generated audio files
  - CSV reports with performance metrics
  - Uses a saved voice ("fm") to avoid re-cloning

**Usage:**

```bash
python test_response_time.py --mode initial
python test_response_time.py --mode cont
```

**Output:**

  - Audio: `benchOutput/audio_<mode>_<id>.wav`
  - Text: `benchOutput/text_<mode>_<id>.txt`
  - CSV: `benchOutput/performance_results_<mode>.csv`

**CSV Format:**
| Column | Description |
|--------|-------------|
| `id` | Test call number |
| `mode` | Test mode (initial/cont) |
| `path` | Path to generated audio file |
| `text` | Input text used |
| `response_time` | API response time (seconds) |
| `avg_response_time` | Average response time for mode |

-----

## 🎯 API Endpoints

### Basic TTS Endpoint

  - **URL**: `http://127.0.0.1:7860`
  - **Method**: POST
  - **API Name**: `/basic_tts`

**Parameters:**

  - `saved_voices`: Voice ID (e.g., "fm")
  - `ref_audio_input`: Reference audio (None for a saved voice)
  - `ref_text_input`: Reference text (empty string)
  - `gen_text_input`: Text to synthesize
  - `remove_silence`: False
  - `randomize_seed`: True
  - `seed_input`: 0
  - `cross_fade_duration_slider`: 0.15
  - `nfe_slider`: 32
  - `speed_slider`: 1.0

-----

## 🎵 Voice Management

### Saved Voices

  - **Location**: `/home/ubuntu/voices/`
  - **Format**: `canonical.wav` + metadata
  - **Usage**: Select via web interface or API voice ID

### Voice Saving

1.  Upload reference audio in the web interface
2.  Click "Save Current Ref as Voice"
3.  Enter a voice ID (e.g., "fm")

-----

## 🔧 Finetuning

### Quick Start

```bash
f5-tts_finetune-gradio
```

### Training Configuration

  - **Model**: F5TTS\_v1\_Base
  - **Dataset**: Custom audio dataset
  - **Output**: Finetuned model weights

-----

## 📈 Performance Benchmarks

### Typical Response Times

  - **Initial mode**: \~12.5s average
  - **Cont mode**: \~6.1s average
  - **Voice cloning**: \~4.3s (with saved voices)

### Optimization Tips

1.  Use **saved voices** to avoid re-cloning.
2.  Adjust **NFE steps**: lower for speed, higher for quality.
3.  Process texts **in sequence**.
4.  Ensure sufficient **GPU memory**.

-----

## 🛠️ Installation

### Prerequisites

A pre-configured virtual environment (`pytorch_venv`) is included.

### Setup

```bash
git clone git@github.com:username/TTS.git
cd TTS
source pytorch_venv/bin/activate
```

### Manual Installation (if needed)

```bash
python -m venv pytorch_venv
source pytorch_venv/bin/activate
pip install torch==2.4.0+cu124 torchaudio==2.4.0+cu124 --extra-index-url [https://download.pytorch.org/whl/cu124](https://download.pytorch.org/whl/cu124)
pip install f5-tts gradio gradio_client librosa soundfile numpy
```

-----

## 📁 Project Structure

```
TTS/
├── start_inference.sh             # Inference server script
├── start_finetune.sh             # Finetuning server script
├── test_response_time.py          # Performance testing script
├── pytorch_venv/                  # Virtual environment (8GB)
├── benchOutput/                   # Test results and audio
│   ├── audio_<mode>_<id>.wav     # Generated audio
│   ├── text_<mode>_<id>.txt      # Input text
│   └── performance_results_*.csv # Performance metrics
└── README.md                     # This file
```

-----

## 📦 GitHub Publishing

### Virtual Environment

The `pytorch_venv` directory (8GB) contains all dependencies.

#### Option 1: Create ZIP

```bash
cd /home/ubuntu/TTS
zip -r pytorch_venv.zip pytorch_venv
echo "pytorch_venv/" >> .gitignore
echo "pytorch_venv.zip" >> .gitignore
# Upload pytorch_venv.zip as a GitHub release asset
```

#### Option 2: Use Git LFS

```bash
git lfs install
git lfs track "*.zip"
git add .gitattributes pytorch_venv.zip
git commit -m "Add pytorch_venv.zip with Git LFS"
git push origin main
```

-----

## 🚨 Troubleshooting

### Common Issues

1.  **Connection refused**: Verify the server runs on port 7860.
2.  **InvalidPathError**: Use a saved voice.
3.  **Memory issues**: Reduce batch size or NFE steps.
4.  **Slow performance**: Check GPU utilization.

### Debug Mode

```bash
python test_response_time.py --mode initial --verbose
```

-----

## 📝 License

MIT License - See the original F5-TTS repository for details.

-----

## 🤝 Contributing

1.  Fork the repository
2.  Create a feature branch
3.  Add improvements
4.  Submit a pull request

<!-- end list -->

````

***

### Commands to Create the Zip and Handle Git LFS

To create a zip of the virtual environment and manage it with Git LFS on your Ubuntu EC2 instance, follow these commands.

1.  **Create the Zip file**:
    ```bash
    cd /home/ubuntu/TTS
    zip -r pytorch_venv.zip pytorch_venv
    ```
    This command will create a zipped file named `pytorch_venv.zip` in your `~/TTS` directory.

2.  **Add the Zip to Git LFS**:
    ```bash
    git lfs install
    git lfs track "*.zip"
    git add .gitattributes pytorch_venv.zip
    git commit -m "Add pytorch_venv.zip with Git LFS"
    git push origin main
    ```
    These commands initialize Git LFS, tell Git to track all `.zip` files, add the necessary files for tracking to your repository, and then push the changes to GitHub.
````