# F5-TTS Hugging Face Space

This is a Hugging Face Space for [F5-TTS](https://github.com/SWivid/F5-TTS), a zero-shot text-to-speech model that can clone voices from short audio samples.

## Features

- Zero-shot voice cloning from a short audio sample
- Support for English and Chinese text
- Multiple speech styles and emotions
- Voice chat capability

## How to Use

### Basic TTS

1. Upload a reference audio clip (keep it under 12 seconds for best results)
2. Enter the text you want to generate
3. Click "Synthesize" to generate speech in the reference voice

### Multi-Speech Generation

1. Add different reference audio clips for different speech types/emotions
2. Enter your text with speech type markers like `{Regular}` or `{Surprised}`
3. Click "Generate Multi-Style Speech" to create a combined audio output

### Voice Chat

1. Upload a reference audio clip
2. Load the chat model
3. Record your message or type it in
4. The AI will respond using the reference voice

## Tips for Best Results

- Keep reference audio clips short (5-12 seconds)
- Use clear, high-quality audio samples
- For non-English voices, provide a reference text if possible
- If you get undesired long silences, turn on the "Remove Silences" option

## Deployment Instructions

This Space uses a Python virtual environment to run F5-TTS. To deploy it to your own Hugging Face Space:

1. Fork this repository to your GitHub account
2. Create a new Space on Hugging Face:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose a name for your Space
   - Select "Python" as the Space SDK
   - Choose "GPU" as the hardware (A10G or T4 recommended)
   - Connect it to your GitHub repository

The Space will automatically install the required dependencies and run the application.

## Credits

- [SWivid](https://github.com/SWivid) for creating F5-TTS
- [mrfakename](https://github.com/fakerybakery) for the original online demo
- [RootingInLoad](https://github.com/RootingInLoad) for initial chunk generation
- [jpgallegoar](https://github.com/jpgallegoar) for multiple speech-type generation & voice chat