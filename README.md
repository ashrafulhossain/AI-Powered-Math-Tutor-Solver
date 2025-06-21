# 🧮 AI Math Problem Solver with Voice, Text, and Image Input

A smart math assistant that helps solve math problems using OpenAI and Deepgram. You can provide math questions by:
- Typing them
- Speaking into your mic
- Uploading an image of handwritten or printed math

---

## Project Description 📌

**AI Math Problem Solver** is a Python-based smart assistant that helps users solve math problems using natural language and visual input. It leverages the power of OpenAI’s GPT-4o for problem-solving and Deepgram for real-time speech recognition.

Users can input math questions in three flexible ways:
- 📝 Typing directly into the console
- 🗣️ Speaking their question using a microphone
- 🖼️ Uploading an image (handwritten or printed) of a math problem

The system understands vague prompts, extracts and interprets math content from images, and responds with clear, step-by-step solutions in plain English.

This tool is ideal for:
- Students needing quick solutions or explanations
- Educators creating learning materials
- Anyone wanting to check their math work

---

## 🚀 Features

- Text-based math queries support  
- Voice input with speech-to-text using Deepgram  
- Image input using GPT-4o for image-based math extraction  
- Intelligent math reasoning with step-by-step answers (in plain English)  
- Follow-up question support with context  
- Built-in vague input handling  
- `.env` file support for API keys  

---

## 🧠 Tech Stack

- Python  
- OpenAI GPT-4o (for math solving + image processing)  
- Deepgram (for speech recognition)  
- Pillow (image handling)  
- PyAudio, Wave (audio recording)  
- python-dotenv (for environment configuration)  

---

## 📁 Folder Structure

math-problem-solver/
├── main.py # Main logic for input and AI interaction
├── .env # Environment variables (not committed)
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## ⚙️ Installation

### 1. Clone the repository


git clone https://github.com/your-username/math-problem-solver.git
cd math-problem-solver
### 2. Install dependencies
💡 Use a virtual environment if possible.


pip install -r requirements.txt
### 3. Set up .env file
Create a .env file in the root directory and add your API keys:


OPENAI_API_KEY=your_openai_key_here

DEEPGRAM_API_KEY=your_deepgram_key_here
### 🎮 Usage
Run the program:


python main.py
You will be prompted to input your math problem by:

Typing it

Speaking it

Uploading an image

The AI will return a clear, step-by-step solution.

### Dependencies 🧪
Make sure the following packages are in your requirements.txt:


openai

deepgram-sdk

pyaudio

Pillow

python-dotenv

keyboard

⚠️ On Windows, you may need to install pyaudio manually via a .whl file if the regular install fails.

### AI Prompt Format 🤖
The assistant follows the Thetawise format:

A short explanation of the problem

Step-by-step breakdown in plain English

A clear final answer (e.g., “So, the solution is x = 5”)

### Limitations 🛑
Only supports .jpg, .jpeg, and .png for image input

Voice input ends when you press Enter

Requires internet access for OpenAI & Deepgram APIs

### Future Improvements 🧩
GUI using Gradio or Tkinter

Error logging and retry system

Optional LaTeX output support

### License 📝
MIT License

### Author 🙋‍♂️
Created by Ashraful Hossain
Feel free to open issues or suggestions!

### Extra Tip ✅
To quickly generate a requirements.txt, run:

pip freeze > requirements.txt
