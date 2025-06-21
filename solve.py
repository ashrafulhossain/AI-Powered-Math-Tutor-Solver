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

# def get_response(user_input, image_description=None):
#     """Handle math-related questions only"""
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

#     # If the user provides a vague input, assume they want to solve the extracted math problem
#     if user_input.lower() in ["solve the math", "what is the math?"] and image_description:
#         user_input = f"Solve the following math problem: {image_description}"

#     # Add user's input to the conversation history
#     math_messages.append({"role": "user", "content": user_input})

#     # Limit conversation history to 10 messages
#     if len(math_messages) > 10:
#         math_messages = math_messages[-10:]

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
#     print("You can upload an image with a math problem or type a math question.")
#     print("Type 'exit' or 'quit' to close the program.\n")

#     global math_messages
#     math_messages = []  # Reset conversation history at the start

#     while True:
#         # Take input and handle quotes and backslashes
#         image_path = input("Provide the path to the image file (Supported formats: JPEG, PNG; press Enter if none): ").strip()
#         # Remove surrounding quotes if they exist
#         image_path = image_path.strip('"').strip("'")
#         # Replace backslashes with forward slashes for consistency
#         image_path = image_path.replace('\\', '/')

#         image_description = None

#         if image_path.lower() in ['exit', 'quit']:
#             print("Exiting the program. Goodbye!")
#             break

#         if image_path:
#             try:
#                 file_extension = validate_image_format(image_path)
#                 image_description = process_image(image_path, file_extension)
#                 print("\nMath content extracted from image:\n")
#                 print(image_description)
#             except Exception as e:
#                 print("Error processing image:", e)
#                 continue  # Skip to the next iteration

#         user_input = input("\nWrite your math question (press Enter to solve the problem in the image): ").strip()
#         if user_input.lower() in ['exit', 'quit']:
#             print("Exiting the program. Goodbye!")
#             break

#         if not user_input and image_description:
#             user_input = "Solve the math problem extracted from the image."
#         elif not user_input and not image_description:
#             print("Error: Please provide a valid math question or an image with a math problem.")
#             continue  # Skip to the next iteration

#         try:
#             answer = get_response(user_input, image_description)
#             print("\nAI:\n")
#             print(answer)
#         except Exception as e:
#             print("Error getting answer:", e)

#         # Allow the user to continue discussing the same problem or ask new questions
#         while True:
#             follow_up = input("\nYou: ").strip()
#             if follow_up.lower() in ['exit', 'quit']:
#                 print("Exiting the program. Goodbye!")
#                 return  # Exit the entire program
#             elif follow_up:
#                 try:
#                     answer = get_response(follow_up, image_description)
#                     print("\nAI:\n")
#                     print(answer)
#                 except Exception as e:
#                     print("Error getting answer:", e)
#             else:
#                 print("Please provide a valid input.")

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

# def get_response(user_input, image_description=None):
#     """Handle math-related questions only"""
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

#     # If the user provides a vague input, assume they want to solve the extracted math problem
#     if user_input.lower() in ["solve the math", "what is the math?"] and image_description:
#         user_input = f"Solve the following math problem: {image_description}"

#     # If image_description is provided, include it in the user's input for context
#     if image_description:
#         user_input = f"{image_description}\n\n{user_input}"

#     # Add user's input to the conversation history
#     math_messages.append({"role": "user", "content": user_input})

#     # Limit conversation history to 10 messages
#     if len(math_messages) > 10:
#         math_messages = math_messages[-10:]

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
#     print("You can upload an image with a math problem or type a math question.")
#     print("Type 'exit' or 'quit' to close the program.\n")

#     global math_messages
#     math_messages = []  # Reset conversation history at the start

#     while True:
#         # Take input and handle quotes and backslashes
#         image_path = input("Provide the path to the image file (Supported formats: JPEG, PNG; press Enter if none): ").strip()
#         # Remove surrounding quotes if they exist
#         image_path = image_path.strip('"').strip("'")
#         # Replace backslashes with forward slashes for consistency
#         image_path = image_path.replace('\\', '/')

#         image_description = None

#         if image_path.lower() in ['exit', 'quit']:
#             print("Exiting the program. Goodbye!")
#             break

#         if image_path:
#             try:
#                 file_extension = validate_image_format(image_path)
#                 image_description = process_image(image_path, file_extension)
#                 print("\nMath content extracted from image:\n")
#                 print(image_description)
#             except Exception as e:
#                 print("Error processing image:", e)
#                 continue  # Skip to the next iteration

#         user_input = input("\nWrite your math question (press Enter to solve the problem in the image): ").strip()
#         if user_input.lower() in ['exit', 'quit']:
#             print("Exiting the program. Goodbye!")
#             break

#         if not user_input and image_description:
#             user_input = "Solve the math problem extracted from the image."
#         elif not user_input and not image_description:
#             print("Error: Please provide a valid math question or an image with a math problem.")
#             continue  # Skip to the next iteration

#         try:
#             answer = get_response(user_input, image_description)
#             print("\nAI:\n")
#             print(answer)
#         except Exception as e:
#             print("Error getting answer:", e)

#         # Allow the user to continue discussing the same problem or ask new questions
#         while True:
#             follow_up = input("\nYou: ").strip()
#             if follow_up.lower() in ['exit', 'quit']:
#                 print("Exiting the program. Goodbye!")
#                 return  # Exit the entire program
#             elif follow_up:
#                 try:
#                     answer = get_response(follow_up, image_description)
#                     print("\nAI:\n")
#                     print(answer)
#                 except Exception as e:
#                     print("Error getting answer:", e)
#             else:
#                 print("Please provide a valid input.")

# if __name__ == "__main__":
#     main()