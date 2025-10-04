import time
import os
import shutil
import csv
import statistics
import argparse
from gradio_client import Client

# Text arrays for different modes
TEXTS_INITIAL = [
    "The sun was setting over the mountains, casting long shadows across the valley. Birds were returning to their nests after a long day of foraging. The evening breeze carried the scent of pine and wildflowers through the air. It was a peaceful moment that reminded everyone of nature's beauty.",
    
    "Technology has revolutionized the way we communicate and work in the modern world. Smartphones and computers have become essential tools for daily life. The internet connects people across continents in real-time. These advances have made information more accessible than ever before.",
    
    "Cooking is both an art and a science that brings people together around the table. Fresh ingredients and proper techniques can transform simple dishes into extraordinary meals. The kitchen becomes a laboratory where creativity meets tradition. Sharing a home-cooked meal creates lasting memories and strengthens relationships.",
    
    "Education opens doors to new opportunities and broadens our understanding of the world. Students learn not only facts and figures but also critical thinking skills. Teachers play a crucial role in shaping young minds and inspiring curiosity. Lifelong learning helps us adapt to an ever-changing world.",
    
    "Music has the power to evoke emotions and bring people together across cultures. Different genres and styles reflect the diversity of human expression. Musicians spend years perfecting their craft and developing their unique sound. Live performances create magical moments that audiences remember forever.",
    
    "Travel broadens our horizons and exposes us to new cultures and perspectives. Exploring different countries teaches us about history, geography, and human nature. Meeting people from various backgrounds enriches our understanding of the world. Every journey becomes a learning experience that shapes who we are.",
    
    "Books are windows into different worlds and minds, offering endless possibilities for exploration. Reading improves vocabulary, concentration, and analytical thinking skills. Authors share their knowledge, experiences, and imagination through written words. Libraries preserve knowledge and provide access to information for everyone.",
    
    "Exercise is essential for maintaining physical health and mental well-being throughout life. Regular physical activity strengthens muscles, improves cardiovascular health, and boosts energy levels. Sports and fitness activities also provide opportunities for social interaction and stress relief. A healthy lifestyle includes both physical activity and proper nutrition.",
    
    "Friendship is one of life's greatest treasures, providing support, laughter, and companionship through good times and bad. True friends accept us for who we are and encourage us to be our best selves. Building and maintaining friendships requires time, effort, and genuine care. These relationships enrich our lives and create lasting bonds.",
    
    "Nature provides us with clean air, fresh water, and beautiful landscapes that inspire and heal. Protecting the environment is crucial for future generations to enjoy the same natural wonders. Conservation efforts help preserve biodiversity and maintain ecological balance. We all have a responsibility to care for our planet."
]

# Shorter texts for "cont" mode (1.5 sentences each)
TEXTS_CONT = [
    "The morning sun rose over the quiet city, casting golden light on empty streets.",
    
    "Technology continues to evolve rapidly, changing how we work and communicate every day.",
    
    "Cooking brings families together around the dinner table, creating memories that last a lifetime.",
    
    "Learning never stops throughout our lives, opening new doors and opportunities.",
    
    "Music touches our souls in ways that words cannot express.",
    
    "Travel opens our minds to new cultures and ways of thinking.",
    
    "Books are treasures that contain the wisdom of generations past.",
    
    "Exercise keeps our bodies strong and our minds clear throughout life.",
    
    "Friendship provides support and joy through all of life's ups and downs.",
    
    "Nature offers peace and beauty that can heal our stressed minds."
]

VOICE_ID = "fm"
HOST = "http://127.0.0.1:7860"
OUTPUT_DIR = "benchOutput"
CALLS = 10

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def text_to_speech_with_save(text, call_number, mode):
    """Convert text to speech and save the audio file. Returns API response time."""
    client = Client(HOST)
    
    print(f"Call {call_number}: {text[:60]}...")
    
    # Measure ONLY the API response time (not file saving)
    start_time = time.time()
    result = client.predict(
        VOICE_ID,           # saved_voices
        None,               # ref_audio_input
        "",                # ref_text_input
        text,              # gen_text_input
        False,             # remove_silence
        True,              # randomize_seed
        0,                 # seed_input
        0.15,              # cross_fade_duration_slider
        32,                # nfe_slider
        1.0,               # speed_slider
        api_name="/basic_tts",
    )
    api_response_time = time.time() - start_time
    
    # The API returns: (audio_path, image_path, generated_text, seed)
    audio_path = result[0]  # First item is the audio file
    
    # Save the audio to our output directory (not included in timing)
    output_audio = os.path.join(OUTPUT_DIR, f"audio_{mode}_{call_number:02d}.wav")
    shutil.copy2(audio_path, output_audio)
    
    # Save the text used
    output_text = os.path.join(OUTPUT_DIR, f"text_{mode}_{call_number:02d}.txt")
    with open(output_text, 'w') as f:
        f.write(text)
    
    print(f"  ✓ API Time: {api_response_time:.2f}s - Saved: {output_audio}")
    return api_response_time, output_audio

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='F5-TTS Performance Test')
    parser.add_argument('--mode', choices=['initial', 'cont'], required=True,
                       help='Test mode: "initial" for longer texts, "cont" for shorter texts')
    args = parser.parse_args()
    
    # Select text array based on mode
    if args.mode == 'initial':
        texts = TEXTS_INITIAL
        mode_desc = "longer texts (3-4 sentences each)"
    else:  # cont mode
        texts = TEXTS_CONT
        mode_desc = "shorter texts (1.5 sentences each)"
    
    print("F5-TTS Text-to-Speech Performance Test")
    print("=" * 50)
    print(f"Mode: {args.mode}")
    print(f"Making {CALLS} calls with {mode_desc}")
    print()
    
    response_times = []
    results = []
    
    for i in range(CALLS):
        text = texts[i % len(texts)]  # Cycle through texts if we need more than 10
        api_time, audio_file = text_to_speech_with_save(text, i + 1, args.mode)
        response_times.append(api_time)
        results.append({
            'id': i + 1,
            'mode': args.mode,
            'path': audio_file,
            'text': text,
            'response_time': api_time
        })
        print()
    
    # Calculate statistics
    avg_time = statistics.mean(response_times)
    min_time = min(response_times)
    max_time = max(response_times)
    median_time = statistics.median(response_times)
    
    # Create CSV file with requested format
    csv_file = os.path.join(OUTPUT_DIR, f"performance_results_{args.mode}.csv")
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'mode', 'path', 'text', 'response_time', 'avg_response_time'])
        for result in results:
            writer.writerow([
                result['id'],
                result['mode'],
                result['path'],
                result['text'],
                f"{result['response_time']:.3f}",
                f"{avg_time:.3f}"
            ])
    
    print("=" * 50)
    print("PERFORMANCE SUMMARY")
    print(f"Mode: {args.mode}")
    print(f"Average API Response Time: {avg_time:.3f}s")
    print(f"Min Response Time: {min_time:.3f}s")
    print(f"Max Response Time: {max_time:.3f}s")
    print(f"Median Response Time: {median_time:.3f}s")
    print()
    print(f"Results saved to: {csv_file}")
    print(f"Audio files saved in: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
