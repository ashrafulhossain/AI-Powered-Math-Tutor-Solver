# import os
# import base64
# import tempfile
# from pathlib import Path
# from PIL import Image
# from openai import OpenAI
# from pdf2image import convert_from_path  # For converting PDF to images
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Initialize OpenAI API client
# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))  # Set your API key here
# math_messages = []

# def encode_image(image_path):
#     """Encode image to base64 format"""
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# def validate_image_format(image_path):
#     """Check if the file is a valid image or PDF format"""
#     valid_extensions = {'.jpg', '.jpeg', '.png', '.pdf'}  # PDF added
#     file_extension = os.path.splitext(image_path)[1].lower()
#     if file_extension not in valid_extensions:
#         raise ValueError(f"Unsupported file format! Please upload one of these formats: {', '.join(valid_extensions)}")
#     return file_extension

# def process_image(image_path, file_extension):
#     """Extract math content from image or PDF using GPT-4V"""
#     global math_messages
#     math_messages = []  # Reset

#     # Check if file exists
#     if not os.path.exists(image_path):
#         raise FileNotFoundError("Image or PDF file not found! Please provide a valid file path.")

#     # Create temp directory for processing
#     uploaded_file_dir = os.environ.get("GRADIO_TEMP_DIR") or str(
#         Path(tempfile.gettempdir()) / "gradio"
#     )
#     os.makedirs(uploaded_file_dir, exist_ok=True)

#     # If the file is a PDF, convert the first page to image
#     if file_extension == '.pdf':
#         # Convert PDF to images (only first page for simplicity)
#         images = convert_from_path(image_path, first_page=1, last_page=1)
#         if not images:
#             raise ValueError("Failed to convert PDF to image!")

#         # Save the first page as a temporary image
#         temp_image_path = os.path.join(uploaded_file_dir, f"tmp{os.urandom(16).hex()}.jpg")
#         images[0].save(temp_image_path, 'JPEG')
#     else:
#         # For other image formats, open directly
#         image = Image.open(image_path)
#         temp_image_path = os.path.join(uploaded_file_dir, f"tmp{os.urandom(16).hex()}.jpg")
#         image.save(temp_image_path)

#     # Encode image to base64
#     base64_image = encode_image(temp_image_path)

#     # Process image with GPT-4V
#     response = client.chat.completions.create(
#         model="gpt-4-vision-preview",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant."
#             },
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{base64_image}"
#                         }
#                     },
#                     {
#                         "type": "text",
#                         "text": "Please describe the math-related content in this image, ensuring that any LaTeX formulas are correctly transcribed."
#                     }
#                 ]
#             }
#         ],
#         max_tokens=1000
#     )

#     # Delete temp file
#     os.remove(temp_image_path)
    
#     return response.choices[0].message.content

# def get_math_response(image_description, user_question):
#     """Answer math question using GPT-4 Turbo"""
#     global math_messages
#     if not math_messages:
#         math_messages.append({"role": "system", "content": "You are a helpful math assistant with code interpretation abilities."})
#     math_messages = math_messages[:1]

#     if image_description is not None:
#         content = f"Image description: {image_description}\n\n"
#     else:
#         content = ""
#     query = f"{content}User question: {user_question}"
#     math_messages.append({"role": "user", "content": query})

#     # Generate response with GPT-4 Turbo
#     response = client.chat.completions.create(
#         model="gpt-4-turbo-preview",
#         messages=math_messages,
#         max_tokens=1000
#     )

#     answer = response.choices[0].message.content
#     math_messages.append({"role": "assistant", "content": answer})
#     return answer

# def main():
#     print("Welcome to Math Problem Solver!")
    
#     # Take image path input
#     image_path = input("Provide the path to the image or PDF file (Supported formats: JPEG, PNG, PDF; press Enter if none): ").strip()
#     image_description = None
#     if image_path:
#         try:
#             # Validate format and get the file extension
#             file_extension = validate_image_format(image_path)
#             image_description = process_image(image_path, file_extension)
#             print("Math content extracted from image/PDF:", image_description)
#         except ValueError as ve:
#             print("Error:", ve)
#             return
#         except FileNotFoundError as fnfe:
#             print("Error:", fnfe)
#             return
#         except Exception as e:
#             print("Error processing image/PDF:", e)
#             return

#     # Take user's question
#     user_question = input("Write your math question: ").strip()
#     if not user_question:
#         print("Error: Please provide a valid math question.")
#         return
    
#     # Generate response
#     try:
#         answer = get_math_response(image_description, user_question)
#         print("Answer:", answer)
#     except Exception as e:
#         print("Error getting answer:", e)

# if __name__ == "__main__":
#     main()



# import os
# import base64
# import tempfile
# from pathlib import Path
# from PIL import Image
# from openai import OpenAI
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Initialize OpenAI API client
# client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# math_messages = []

# def encode_image(image_path):
#     """Encode image to base64 format"""
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

# def validate_image_format(image_path):
#     """Check if the file is a valid image format"""
#     valid_extensions = {'.jpg', '.jpeg', '.png'}
#     file_extension = os.path.splitext(image_path)[1].lower()
#     if file_extension not in valid_extensions:
#         raise ValueError(f"Unsupported file format! Please upload one of these formats: {', '.join(valid_extensions)}")
#     return file_extension

# def process_image(image_path, file_extension):
#     """Extract math content from image using GPT-4o"""
#     global math_messages
#     math_messages = []  # Reset message history

#     if not os.path.exists(image_path):
#         raise FileNotFoundError("Image file not found! Please provide a valid file path.")

#     # Create temporary directory for processing
#     uploaded_file_dir = os.environ.get("GRADIO_TEMP_DIR") or str(
#         Path(tempfile.gettempdir()) / "gradio"
#     )
#     os.makedirs(uploaded_file_dir, exist_ok=True)

#     # Open the image
#     image = Image.open(image_path)
#     # Convert RGBA to RGB if needed (for PNG with transparency)
#     if image.mode == 'RGBA':
#         image = image.convert('RGB')
#     temp_image_path = os.path.join(uploaded_file_dir, f"tmp{os.urandom(16).hex()}.jpg")
#     image.save(temp_image_path)

#     base64_image = encode_image(temp_image_path)

#     # Updated prompt to be more specific about extracting math content
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a helpful assistant that extracts math problems from images, including handwritten or typed equations, and formats them as questions in plain text."
#             },
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{base64_image}"
#                         }
#                     },
#                     {
#                         "type": "text",
#                         "text": "Extract any math-related content (equations, expressions, or problems) from this image and format it as a question in plain text (no LaTeX). If the content is an equation, assume the question is to solve it. If no math content is found, say 'No math content found in the image.'"
#                     }
#                 ]
#             }
#         ],
#         max_tokens=1000
#     )

#     # Clean up temporary file
#     os.remove(temp_image_path)
    
#     return response.choices[0].message.content

# def get_math_response(image_description, user_question):
#     """Answer math question using GPT-4o in Thetawise format without LaTeX"""
#     global math_messages
#     if not math_messages:
#         math_messages.append({
#             "role": "system",
#             "content": "You are a helpful math assistant with code interpretation abilities."
#         })
#     math_messages = math_messages[:1]

#     # Instruction to use Thetawise format in plain text (no LaTeX)
#     formatting_instruction = (
#         "Solve the math problem using the following format:\n\n"
#         "Thetawise\n"
#         "To solve for x in the equation, follow these steps:\n"
#         "Each step should begin with a short explanation, followed by a math expression using plain text only (do not use LaTeX or special characters).\n"
#         "Use clear spacing and line breaks.\n"
#         "End the response with: 'So, the solution is x = ...' or a suitable conclusion if x is not the variable."
#     )

#     if image_description is not None:
#         content = f"{formatting_instruction}\n\nImage description: {image_description}\n"
#     else:
#         content = formatting_instruction
#     query = f"{content}\n\nUser question: {user_question}"
#     math_messages.append({"role": "user", "content": query})

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=math_messages,
#         max_tokens=1000
#     )

#     answer = response.choices[0].message.content
#     math_messages.append({"role": "assistant", "content": answer})
#     return answer

# def main():
#     print("Welcome to Math Problem Solver!")

#     # Take input and handle quotes and backslashes
#     image_path = input("Provide the path to the image file (Supported formats: JPEG, PNG; press Enter if none): ").strip()
#     # Remove surrounding quotes if they exist
#     image_path = image_path.strip('"').strip("'")
#     # Replace backslashes with forward slashes for consistency
#     image_path = image_path.replace('\\', '/')

#     image_description = None

#     if image_path:
#         try:
#             file_extension = validate_image_format(image_path)
#             image_description = process_image(image_path, file_extension)
#             print("\nMath content extracted from image:\n")
#             print(image_description)
#         except Exception as e:
#             print("Error processing image:", e)
#             return

#     user_question = input("\nWrite your math question (press Enter to solve the problem in the image): ").strip()
#     if not user_question and image_description:
#         user_question = "Solve the math problem extracted from the image."
#     elif not user_question and not image_description:
#         print("Error: Please provide a valid math question or an image with a math problem.")
#         return

#     try:
#         answer = get_math_response(image_description, user_question)
#         print("\nAnswer:\n")
#         print(answer)
#     except Exception as e:
#         print("Error getting answer:", e)

# if __name__ == "__main__":
#     main()

