import os
import sys

# Add F5-TTS to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "F5-TTS"))

# Create voices directory
voices_dir = os.path.join(os.path.dirname(__file__), "voices")
os.makedirs(voices_dir, exist_ok=True)

# Import and patch the infer_gradio module
import f5_tts.infer.infer_gradio

# Set the voices directory
f5_tts.infer.infer_gradio.VOICES_ROOT_DIR = voices_dir

# Original infer function
original_infer = f5_tts.infer.infer_gradio.infer

# Patched infer function
def patched_infer(*args, **kwargs):
    result = original_infer(*args, **kwargs)
    # Check if the result has 3 or 4 values and handle accordingly
    if isinstance(result, tuple) and len(result) == 3:
        # Add a default seed value (0) as the fourth return value
        return result[0], result[1], result[2], 0
    return result

# Replace the original function with our patched version
f5_tts.infer.infer_gradio.infer = patched_infer

# For Hugging Face Spaces, we need to set USING_SPACES
f5_tts.infer.infer_gradio.USING_SPACES = True

# Call _ensure_dir on the voices directory
f5_tts.infer.infer_gradio._ensure_dir(voices_dir)

# Import the app after all patches are applied
from f5_tts.infer.infer_gradio import app

if __name__ == "__main__":
    print(f"Voices directory: {voices_dir}")
    print(f"Using voices directory in infer_gradio: {f5_tts.infer.infer_gradio.VOICES_ROOT_DIR}")
    # Launch the app with Gradio's queue
    app.queue().launch()