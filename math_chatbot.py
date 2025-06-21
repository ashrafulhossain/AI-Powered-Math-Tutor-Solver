
# import os
# import base64
# import tempfile
# from pathlib import Path
# from PIL import Image
# from openai import OpenAI
# from dotenv import load_dotenv
# import re

# # Load environment variables
# load_dotenv()

# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# math_messages = []

# def validate_image_format(image_path):
#     valid_extensions = {'.jpg', '.jpeg', '.png'}
#     file_extension = os.path.splitext(image_path)[1].lower()
#     if file_extension not in valid_extensions:
#         raise ValueError(f"Unsupported file format! Please upload one of these formats: {', '.join(valid_extensions)}")
#     return file_extension

# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# def process_image(image_path, file_extension):
#     global math_messages
#     math_messages = []

#     if not os.path.exists(image_path):
#         raise FileNotFoundError("Image file not found! Please provide a valid file path.")

#     uploaded_file_dir = os.environ.get("GRADIO_TEMP_DIR") or str(Path(tempfile.gettempdir()) / "gradio")
#     os.makedirs(uploaded_file_dir, exist_ok=True)

#     image = Image.open(image_path)
#     if image.mode == 'RGBA':
#         image = image.convert('RGB')
#     temp_image_path = os.path.join(uploaded_file_dir, f"tmp{os.urandom(16).hex()}.jpg")
#     image.save(temp_image_path)

#     base64_image = encode_image(temp_image_path)

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[{
#             "role": "system",
#             "content": "You are a helpful assistant that extracts math problems from images, including handwritten or typed equations, and formats them as questions in plain text."
#         },{
#             "role": "user",
#             "content": [
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{base64_image}"
#                     }
#                 },
#                 {
#                     "type": "text",
#                     "text": "Extract any math-related content (equations, expressions, or problems) from this image and format it as a question in plain text (no LaTeX). If the content is an equation, assume the question is to solve it. If no math content is found, say 'No math content found in the image.'"
#                 }
#             ]
#         }],
#         max_tokens=1000
#     )

#     os.remove(temp_image_path)
#     return response.choices[0].message.content

# def is_vague_math_request(text):
#     vague_phrases = [
#         "solve it", "do the math",
#         "help me", "solve the math", "can you help me", "what's the answer",
#         "calculate this", "what's the solution", "explain this"
#     ]
#     return any(phrase in text.lower() for phrase in vague_phrases)

# def get_response(user_input, image_description=None):
#     global math_messages
#     if not math_messages:
#         math_messages.append({
#             "role": "system",
#             "content": (
#                 "You are a helpful math assistant. Your expertise is strictly limited to math-related questions. "
#                 "If the user asks a math-related question, solve it step-by-step using the Thetawise format (plain text, no LaTeX). "
#                 "If the user provides a vague input like 'solve the math' or 'what is the math?', assume they want to solve the math problem extracted from the image. "
#                 "If no math problem is provided, respond with: 'Please provide a specific math-related question or upload an image with a math problem.'\n"
#                 "Thetawise format for math problems:\n"
#                 "1. Start with a brief explanation of the problem.\n"
#                 "2. Clearly explain each step of the solution using plain text.\n"
#                 "3. Use clear spacing and line breaks.\n"
#                 "4. End with the final answer in plain text (e.g., 'So, the solution is x = ...')."
#             )
#         })

#     if is_vague_math_request(user_input) and image_description:
#         user_input = f"Solve the following math problem: {image_description}"

#     if user_input and image_description:
#         user_input = f"{image_description}\n\n{user_input}"

#     math_messages.append({"role": "user", "content": user_input})

#     if len(math_messages) > 10:
#         math_messages = math_messages[-10:]

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=math_messages,
#         max_tokens=1000
#     )

#     answer = response.choices[0].message.content

#     lines = answer.splitlines()
#     deduped_lines = []
#     prev_line = ""
#     for line in lines:
#         if line.strip() != prev_line.strip():
#             deduped_lines.append(line)
#             prev_line = line

#     final_answer = "\n".join(deduped_lines)
#     math_messages.append({"role": "assistant", "content": final_answer})
#     return final_answer

# def main():
#     print("Welcome to Math Problem Solver!")
#     print("You can: (1) Upload an image with a math problem, (2) Type a math question.")
#     print("Type 'exit' or 'quit' to close the program.\n")

#     global math_messages
#     math_messages = []

#     while True:
#         print("How would you like to provide your math question?")
#         print("(1) Upload an image")
#         print("(2) Type a question")
#         choice = input("Enter your choice (1/2, or 'exit' to quit): ").strip()

#         if choice.lower() in ['exit', 'quit']:
#             print("Exiting the program. Goodbye!")
#             break

#         image_description = None
#         user_input = None

#         if choice == '1':
#             image_path = input("Provide the path to the image file (Supported formats: JPEG, PNG; press Enter if none): ").strip()
#             image_path = image_path.strip('"').strip("'").replace('\\', '/')
#             if not image_path:
#                 print("No image path provided. Please try again.")
#                 continue

#             try:
#                 file_extension = validate_image_format(image_path)
#                 image_description = process_image(image_path, file_extension)
#                 print("\nMath content extracted from image:\n")
#                 print(image_description)
#             except Exception as e:
#                 print("Error processing image:", e)
#                 continue

#         elif choice == '2':
#             user_input = input("\nWrite your math question: ").strip()
#             if not user_input:
#                 print("Error: Please provide a valid math question.")
#                 continue

#         else:
#             print("Invalid choice! Please select 1 or 2.")
#             continue

#         if not user_input and not image_description:
#             print("Error: Please provide a valid math question or an image with a math problem.")
#             continue

#         try:
#             if user_input:
#                 answer = get_response(user_input, image_description)
#                 print("\nAI:\n")
#                 print(answer)
#         except Exception as e:
#             print("Error getting answer:", e)

# if __name__ == "__main__":
#     main()











# import os
# import base64
# import tempfile
# import aiohttp
# from pathlib import Path
# from openai import OpenAI
# from dotenv import load_dotenv
# from deepgram import Deepgram

# # Load environment variables
# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# deepgram = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

# math_messages = []  # Stores system, user, and assistant messages for context

# # --------------------------
# # 🟢 Image Processing
# # --------------------------

# def encode_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")

# def validate_image_format(image_path):
#     valid_extensions = {".jpg", ".jpeg", ".png"}
#     file_extension = os.path.splitext(image_path)[1].lower()
#     if file_extension not in valid_extensions:
#         raise ValueError(f"Unsupported file format! Please upload one of these formats: {', '.join(valid_extensions)}")
#     return file_extension

# def process_image(image):
#     global math_messages

#     uploaded_file_dir = os.environ.get("GRADIO_TEMP_DIR") or str(Path(tempfile.gettempdir()) / "gradio")
#     os.makedirs(uploaded_file_dir, exist_ok=True)

#     image_path = os.path.join(uploaded_file_dir, image.name)
#     with open(image_path, "wb") as f:
#         for chunk in image.chunks():
#             f.write(chunk)

#     base64_image = encode_image(image_path)

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "Extract math problems from images and format them as plain text questions."
#             },
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "image_url",
#                         "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
#                     },
#                     {
#                         "type": "text",
#                         "text": "Extract any math-related content from this image and format it as a question in plain text."
#                     }
#                 ]
#             }
#         ],
#         max_tokens=7000
#     )

#     os.remove(image_path)

#     if not response.choices or not response.choices[0].message.content:
#         return "Could not extract math question from the image."

#     extracted_question = response.choices[0].message.content.strip()
#     math_messages.append({"role": "user", "content": extracted_question})
#     return extracted_question

# # --------------------------
# # 🔵 Speech-to-Text (Deepgram)
# # --------------------------

# async def speech_to_text(audio_path):
#     async with aiohttp.ClientSession() as session:
#         try:
#             with open(audio_path, "rb") as audio_file:
#                 buffer_data = audio_file.read()

#             source = {
#                 "buffer": buffer_data,
#                 "mimetype": "audio/wav"
#             }
#             options = {
#                 "model": "nova",
#                 "language": "en",
#                 "punctuate": True
#             }

#             response = await deepgram.transcription.prerecorded(source, options)

#             transcript = response.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
#             return transcript.strip() if transcript else None

#         except Exception as e:
#             print("Deepgram API Error:", str(e))
#             return None

# # --------------------------
# # 🟠 AI Response (GPT-4o)
# # --------------------------

# def get_response(user_input, image_description=None):
#     global math_messages

#     # Insert system prompt if starting fresh
#     if not math_messages:
#         math_messages.append({
#             "role": "system",
#             "content": """You are a helpful and precise math assistant. Your expertise is strictly limited to math-related questions.

# If the user asks a math-related question, solve it step-by-step using the MathJax format (LaTeX inside HTML for proper rendering).

# If the user input is vague (e.g., 'solve it', 'what is the math?', or 'solve the problem'), do the following:
# - If an image is provided, extract the math problem from the image and solve it.
# - If no image is provided, use the most recent math-related problem in the conversation history.
# - If neither is available, respond with: 'Please provide a specific math-related question or upload an image with a math problem.'

# Formatting rules:
# - Use <p> tags for all explanations.
# - Use <ol> or <ul> with <li> tags for step-by-step solutions.
# - Use \\( ... \\) for inline math and \\[ ... \\] for display math.
# - Final answer must be in: <p>Final answer: \\( \\boxed{...} \\)</p>

# IMPORTANT: Do NOT wrap the HTML in backticks or code blocks."""
#         })

#     vague_inputs = {
#         "solve it", "solve this", "solve the math", "what is the math?",
#         "what is the answer?", "show solution", "solution please",
#         "show answer", "please solve", "answer it"
#     }

#     user_input_cleaned = user_input.strip().lower() if user_input else ""

#     # Fallback to previous question if vague
#     if user_input_cleaned in vague_inputs:
#         last_user_question = next(
#             (msg["content"] for msg in reversed(math_messages) if msg["role"] == "user"),
#             None
#         )
#         latest_input = last_user_question or "Please upload a math problem image or enter a question."
#     else:
#         latest_input = f"{image_description}\n\n{user_input}" if image_description and user_input else (
#             image_description or user_input
#         )

#     if not latest_input:
#         return "Please provide a math-related question or upload an image with a problem."

#     # Limit context history to system + 14 messages
#     if len(math_messages) >= 5:
#         math_messages = [math_messages[0]] + math_messages[-4:]

#     math_messages.append({"role": "user", "content": latest_input})

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=math_messages,
#         max_tokens=7000
#     )

#     assistant_reply = response.choices[0].message.content
#     math_messages.append({"role": "assistant", "content": assistant_reply})

#     if len(math_messages) > 5:
#         math_messages = [math_messages[0]] + math_messages[-4:]

#     return assistant_reply



import os
import base64
import tempfile
import aiohttp
import fitz  # pymupdf
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from deepgram import Deepgram

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
deepgram = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

# --------------------------
# 🔵 Image Processing
# --------------------------

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def process_image(image):
    uploaded_file_dir = os.environ.get("GRADIO_TEMP_DIR") or str(Path(tempfile.gettempdir()) / "gradio")
    os.makedirs(uploaded_file_dir, exist_ok=True)

    image_path = os.path.join(uploaded_file_dir, image.name)
    with open(image_path, "wb") as f:
        for chunk in image.chunks():
            f.write(chunk)

    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Extract math problems from images and format them as plain text questions."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    },
                    {
                        "type": "text",
                        "text": "Extract any math-related content from this image and format it as a question in plain text."
                    }
                ]
            }
        ],
        max_tokens=1000
    )

    os.remove(image_path)

    return response.choices[0].message.content.strip() if response.choices[0].message.content else "Could not extract math question from the image."

# --------------------------
# 📄 PDF Processing
# --------------------------

def extract_text_from_pdf(pdf_file):
    pdf_path = os.path.join(tempfile.gettempdir(), pdf_file.name)
    with open(pdf_path, "wb") as f:
        for chunk in pdf_file.chunks():
            f.write(chunk)

    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    doc.close()
    os.remove(pdf_path)
    return full_text.strip()

# --------------------------
# 🔵 Speech-to-Text (Deepgram)
# --------------------------

async def speech_to_text(audio_path):
    async with aiohttp.ClientSession() as session:
        try:
            with open(audio_path, "rb") as audio_file:
                buffer_data = audio_file.read()

            source = {"buffer": buffer_data, "mimetype": "audio/wav"}
            options = {"model": "nova", "language": "en", "punctuate": True}

            response = await deepgram.transcription.prerecorded(source, options)
            transcript = response.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0].get("transcript", "")
            return transcript.strip() if transcript else None

        except Exception as e:
            print("Deepgram API Error:", str(e))
            return None

# --------------------------
# 🧠 Chat Response Generator
# --------------------------

def convert_chat_history(chat_history):
    messages = []
    for chat in chat_history:
        if "prompt" in chat:
            messages.append({"role": "user", "content": chat["prompt"]})
        if "response" in chat:
            messages.append({"role": "assistant", "content": chat["response"]})
    return messages

def get_response(user_input, conversation_history, image_description=None, pdf_text=None):
    context = convert_chat_history(conversation_history)

    vague_inputs = {
        "solve it", "solve this", "solve the math", "what is the math?",
        "what is the answer?", "show solution", "solution please",
        "show answer", "please solve", "answer it"
    }

    user_input_cleaned = user_input.strip().lower() if user_input else ""

    if user_input_cleaned in vague_inputs:
        last_user_question = next(
            (msg["content"] for msg in reversed(context) if msg["role"] == "user"),
            None
        )
        latest_input = last_user_question or "Please upload a math problem image or enter a question."
    else:
        if pdf_text:
            latest_input = f"{pdf_text}\n\n{user_input or ''}".strip()
        elif image_description and user_input:
            latest_input = f"{image_description}\n\n{user_input}"
        else:
            latest_input = image_description or user_input

    if not latest_input:
        return "<p>Please provide a math-related question, image, or PDF.</p>"

    context.insert(0, {
        "role": "system",
        "content": r"""
You are an expert math tutor. Format all responses as valid HTML string for a MathJax-enabled frontend.

Instructions:
- Do NOT show the problem text, even if it is extracted from PDF/image or given directly by the user.
- ONLY return the clean, structured, step-by-step solution.
- Use semantic HTML:
  - Use <section class=\"math-section\"> for the full solution block
  - Use <h3>Solution</h3> to start the section
  - Use <ol> with <li> for steps
- Use MathJax-compatible LaTeX:
  - Inline math → <span>\( ... \)</span>
  - Display math → <div>\[ ... \]</div>
- If there are multiple problems, give only the solutions one after another without showing any problem statements.
- At the end of the response (if math-related), always include:
<button class=\"math-det-show-cal\">Show Calculation</button>
"""
    })

    context.append({"role": "user", "content": latest_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=context,
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()



