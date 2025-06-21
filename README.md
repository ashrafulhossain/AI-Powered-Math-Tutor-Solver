# 🧮 AI Math Problem Solver with Voice, Text, and Image Input

A smart math assistant that helps solve math problems using OpenAI and Deepgram. You can provide math questions by:
- Typing them
- Speaking into your mic
- Uploading an image of handwritten or printed math

---

## 🚀 Features

- 🔤 **Text-based math queries** support
- 🗣️ **Voice input** with speech-to-text using Deepgram
- 🖼️ **Image input** using GPT-4o for image-based math extraction
- 🤖 Intelligent math reasoning with step-by-step answers (in plain English)
- 🔄 Follow-up question support with context
- 🛠️ Built-in vague input handling
- 🔒 .env file support for API keys

---

## 🧠 Tech Stack

- Python
- OpenAI GPT-4o (for math solving + image processing)
- Deepgram (for speech recognition)
- Pillow (image handling)
- PyAudio, Wave (audio recording)
- dotenv (for environment configuration)

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

```bash
git clone https://github.com/your-username/math-problem-solver.git
cd math-problem-solver
2. Install dependencies
Use a virtual environment if possible.

bash
Copy
Edit
pip install -r requirements.txt
3. Set up .env file
Create a .env file in the root folder and add your API keys:

env
Copy
Edit
OPENAI_API_KEY=your_openai_key_here
DEEPGRAM_API_KEY=your_deepgram_key_here
🎮 Usage
Run the program:

bash
Copy
Edit
python main.py
You will be asked how you want to input your math problem:

Type it

Speak it

Upload an image

The AI will then return a step-by-step solution.

🧪 Dependencies
Add this to your requirements.txt:

txt
Copy
Edit
openai
deepgram-sdk
pyaudio
Pillow
python-dotenv
keyboard
Note: On Windows, you might need to install pyaudio via .whl if pip install fails.

🤖 AI Prompt Format
The assistant uses a Thetawise format to provide:

Problem overview

Step-by-step explanation (in plain text)

Final answer clearly stated

🛑 Limitations
Only supports .jpg, .jpeg, and .png for image input

Voice input uses Enter to stop recording

Requires internet access to access OpenAI & Deepgram APIs

🧩 Future Improvements
GUI interface with Gradio or Tkinter

Error logging and retry mechanism

Support for LaTeX output (optional)

📝 License
MIT License

🙋‍♂️ Author
Created by Your Name.
Feel free to open issues or suggestions!

yaml
Copy
Edit

---

### ✅ Extra Tip:

To create a quick `requirements.txt`, run:

```bash
pip freeze > requirements.txt
