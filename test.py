
import os
import base64
import tempfile
from pathlib import Path
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv
import pyaudio
import wave
from deepgram import Deepgram
import asyncio
import keyboard
import re

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
deepgram = Deepgram(os.getenv('DEEPGRAM_API_KEY'))
math_messages = []

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording... Speak your math question. Press Enter to stop recording.")
    frames = []
    while not keyboard.is_pressed('enter'):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    temp_audio_path = os.path.join(tempfile.gettempdir(), "temp_audio.wav")
    wf = wave.open(temp_audio_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return temp_audio_path

async def speech_to_text(audio_path):
    try:
        with open(audio_path, 'rb') as audio_file:
            buffer_data = audio_file.read()
        source = {"buffer": buffer_data, "mimetype": "audio/wav"}
        options = {"model": "nova", "language": "en", "punctuate": True}
        response = await deepgram.transcription.prerecorded(source, options)

        if (response and
            "results" in response and
            "channels" in response["results"] and
            len(response["results"]["channels"]) > 0 and
            "alternatives" in response["results"]["channels"][0] and
            len(response["results"]["channels"][0]["alternatives"]) > 0):

            transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
            return transcript if transcript.strip() else None
        else:
            print("Warning: No transcript found in response.")
            return None

    except Exception as e:
        print(f"Error in speech-to-text conversion: {e}")
        return None

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def validate_image_format(image_path):
    valid_extensions = {'.jpg', '.jpeg', '.png'}
    file_extension = os.path.splitext(image_path)[1].lower()
    if file_extension not in valid_extensions:
        raise ValueError(f"Unsupported file format! Please upload one of these formats: {', '.join(valid_extensions)}")
    return file_extension

def process_image(image_path, file_extension):
    global math_messages
    math_messages = []

    if not os.path.exists(image_path):
        raise FileNotFoundError("Image file not found! Please provide a valid file path.")

    uploaded_file_dir = os.environ.get("GRADIO_TEMP_DIR") or str(Path(tempfile.gettempdir()) / "gradio")
    os.makedirs(uploaded_file_dir, exist_ok=True)

    image = Image.open(image_path)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    temp_image_path = os.path.join(uploaded_file_dir, f"tmp{os.urandom(16).hex()}.jpg")
    image.save(temp_image_path)

    base64_image = encode_image(temp_image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that extracts math problems from images, including handwritten or typed equations, and formats them as questions in plain text."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Extract any math-related content (equations, expressions, or problems) from this image and format it as a question in plain text (no LaTeX). If the content is an equation, assume the question is to solve it. If no math content is found, say 'No math content found in the image.'"
                    }
                ]
            }
        ],
        max_tokens=1000
    )

    os.remove(temp_image_path)
    return response.choices[0].message.content

def is_vague_math_request(text):
    vague_phrases = [
        "solve it", "do the math",
        "help me", "solve the math", "can you help me", "what's the answer",
        "calculate this", "what's the solution", "explain this"
    ]
    return any(phrase in text.lower() for phrase in vague_phrases)

def get_response(user_input, image_description=None):
    global math_messages
    if not math_messages:
        math_messages.append({
            "role": "system",
            "content": (
                "You are a helpful math assistant. Your expertise is strictly limited to math-related questions. "
                "If the user asks a math-related question, solve it step-by-step using the Thetawise format (plain text, no LaTeX). "
                "If the user provides a vague input like 'solve the math' or 'what is the math?', assume they want to solve the math problem extracted from the image. "
                "If no math problem is provided, respond with: 'Please provide a specific math-related question or upload an image with a math problem.'\n"
                "Thetawise format for math problems:\n"
                "1. Start with a brief explanation of the problem.\n"
                "2. Clearly explain each step of the solution using plain text.\n"
                "3. Use clear spacing and line breaks.\n"
                "4. End with the final answer in plain text (e.g., 'So, the solution is x = ...')."
            )
        })

    if is_vague_math_request(user_input) and image_description:
        user_input = f"Solve the following math problem: {image_description}"

    if user_input and image_description:
        user_input = f"{image_description}\n\n{user_input}"

    math_messages.append({"role": "user", "content": user_input})

    if len(math_messages) > 10:
        math_messages = math_messages[-10:]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=math_messages,
        max_tokens=1000
    )

    answer = response.choices[0].message.content

    lines = answer.splitlines()
    deduped_lines = []
    prev_line = ""
    for line in lines:
        if line.strip() != prev_line.strip():
            deduped_lines.append(line)
            prev_line = line

    final_answer = "\n".join(deduped_lines)
    math_messages.append({"role": "assistant", "content": final_answer})
    return final_answer

def main():
    print("Welcome to Math Problem Solver!")
    print("You can: (1) Upload an image with a math problem, (2) Type a math question, or (3) Speak your math question.")
    print("Type 'exit' or 'quit' to close the program.\n")

    global math_messages
    math_messages = []

    loop = asyncio.get_event_loop()

    while True:
        print("How would you like to provide your math question?")
        print("(1) Upload an image")
        print("(2) Type a question")
        print("(3) Speak your question")
        choice = input("Enter your choice (1/2/3, or 'exit' to quit): ").strip()

        if choice.lower() in ['exit', 'quit']:
            print("Exiting the program. Goodbye!")
            break

        image_description = None
        user_input = None

        if choice == '1':
            image_path = input("Provide the path to the image file (Supported formats: JPEG, PNG; press Enter if none): ").strip()
            image_path = image_path.strip('"').strip("'").replace('\\', '/')
            if not image_path:
                print("No image path provided. Please try again.")
                continue

            try:
                file_extension = validate_image_format(image_path)
                image_description = process_image(image_path, file_extension)
                print("\nMath content extracted from image:\n")
                print(image_description)
            except Exception as e:
                print("Error processing image:", e)
                continue

        elif choice == '2':
            user_input = input("\nWrite your math question: ").strip()
            if not user_input:
                print("Error: Please provide a valid math question.")
                continue

        elif choice == '3':
            input("Press Enter to start recording...")
            audio_path = record_audio()
            transcript = loop.run_until_complete(speech_to_text(audio_path))
            os.remove(audio_path)

            if transcript:
                print(f"\nI understood: '{transcript}'")
                user_input = transcript
            else:
                print("Error: Could not understand your speech. Please try again.")
                continue
        else:
            print("Invalid choice! Please select 1, 2, or 3.")
            continue

        if not user_input and not image_description:
            print("Error: Please provide a valid math question or an image with a math problem.")
            continue

        try:
            if user_input:
                answer = get_response(user_input, image_description)
                print("\nAI:\n")
                print(answer)
        except Exception as e:
            print("Error getting answer:", e)

        while True:
            print("\nWould you like to ask a follow-up question?")
            print("Enter:")
            print("(1) to type a question")
            print("(2) to speak a question")
            print("(3) to upload a new image")
            print("(4) to go back to main menu")
            follow_up_choice = input("Your choice: ").strip()

            if follow_up_choice == '1':
                follow_up = input("\nType your follow-up question: ").strip()
                if follow_up.lower() in ['exit', 'quit']:
                    print("Exiting the program. Goodbye!")
                    return
                elif follow_up:
                    try:
                        answer = get_response(follow_up, image_description)
                        print("\nAI:\n")
                        print(answer)
                    except Exception as e:
                        print("Error getting answer:", e)

            elif follow_up_choice == '2':
                input("Press Enter to start recording...")
                audio_path = record_audio()
                transcript = loop.run_until_complete(speech_to_text(audio_path))
                os.remove(audio_path)
                if transcript:
                    print(f"\nI understood: '{transcript}'")
                    follow_up = transcript
                    try:
                        answer = get_response(follow_up, image_description)
                        print("\nAI:\n")
                        print(answer)
                    except Exception as e:
                        print("Error getting answer:", e)
                else:
                    print("Error: Could not understand your speech. Please try again.")

            elif follow_up_choice == '3':
                image_path = input("Provide the path to the new image file: ").strip()
                image_path = image_path.strip('"').strip("'").replace('\\', '/')
                if not image_path:
                    print("No image path provided. Please try again.")
                    continue
                try:
                    file_extension = validate_image_format(image_path)
                    image_description = process_image(image_path, file_extension)
                    print("\nMath content extracted from the image:\n")
                    print(image_description)
                except Exception as e:
                    print("Error processing image:", e)

            elif follow_up_choice == '4':
                break
            else:
                print("Invalid choice! Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()




