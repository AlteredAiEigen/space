import os
import sys

# Add F5-TTS to Python path
# sys.path.append(os.path.join(os.path.dirname(__file__), "F5-TTS"))
current_dir = os.path.dirname(os.path.abspath(__file__))
f5_tts_path = os.path.join(current_dir, "F5-TTS")
if f5_tts_path not in sys.path:
    sys.path.insert(0, f5_tts_path)

# Path to 'src' folder inside F5-TTS
src_path = os.path.join(current_dir, "F5-TTS", "src")

# Add src_path to sys.path if not already added
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Create voices directory
voices_dir = os.path.join(os.path.dirname(__file__), "voices")
os.makedirs(voices_dir, exist_ok=True)

# Import and patch the infer_gradio module
import f5_tts.infer.infer_gradio

# Set the voices directory
f5_tts.infer.infer_gradio.VOICES_ROOT_DIR = voices_dir

# For CI, we set USING_SPACES to False to avoid loading the chat model
f5_tts.infer.infer_gradio.USING_SPACES = False

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

# Call _ensure_dir on the voices directory
f5_tts.infer.infer_gradio._ensure_dir(voices_dir)

# Import the app after all patches are applied
from f5_tts.infer.infer_gradio import app

if __name__ == "__main__":
    print(f"Voices directory: {voices_dir}")
    print(f"Using voices directory in infer_gradio: {f5_tts.infer.infer_gradio.VOICES_ROOT_DIR}")
    print(f"CI mode: USING_SPACES = {f5_tts.infer.infer_gradio.USING_SPACES}")
    # Launch the app with Gradio's queue
    app.queue().launch()
