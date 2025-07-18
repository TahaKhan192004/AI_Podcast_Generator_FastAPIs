AI Podcast Generator
This project generates a short podcast episode using AI. It creates a dialogue-based script between a host and a guest using a Large Language Model (via Groq), then converts it to audio using ElevenLabs.

✅ Features
Generates a short, conversational podcast script

Converts script to audio using realistic AI voices

Fully automated using FastAPI, LangChain, and ElevenLabs

API-ready for integration and testing via Swagger UI

🔧 Setup Instructions

1. Clone the repository
git clone https://github.com/your-username/ai-podcast-generator.git
cd ai-podcast-generator

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Create a .env file
In the project root, create a .env file with the following content:
GROQ_API_KEY=your_groq_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
Replace the placeholders with your actual API keys from Groq and ElevenLabs.

🚀 Run the FastAPI App
Start the server using Uvicorn:
uvicorn main_api:app --reload
Once the server is running, open your browser and visit:
http://127.0.0.1:8000/docs
This opens Swagger UI where you can test the API.

🧪 How to Use the API
In Swagger UI, go to the POST /generate_podcast endpoint.

Click "Try it out".

Fill in the JSON fields. For example:

{
  "topic": "The rise of AI in education"
}
Click Execute.

The API will return a response like:
{
  "success": true,
  "audio_file": "podcast.mp3",
  "script_file": "podcast_script.txt",
  "message": "Podcast successfully generated."
}
The script and audio files will be saved in your working directory.
