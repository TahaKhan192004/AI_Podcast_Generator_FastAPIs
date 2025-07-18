AI Podcast Generator
This project allows you to generate a short podcast episode using AI. It creates a script where a host and a guest discuss a topic, and then converts the script into speech using ElevenLabs. The result is a ready-to-play podcast audio file.

Setup Instructions
To get started, first make sure you have Python installed and then set up a virtual environment for the project. Install all required dependencies listed in the project’s requirements file.

Next, create a file named .env in the root directory of the project. In this file, you’ll need to add two API keys: one for Groq and one for ElevenLabs. These keys are necessary for generating the podcast script and converting text to speech.

Running the Application
Once everything is set up, you can run the FastAPI application. The server will start locally and provide a web interface for interacting with the API.

Testing the API
Open your browser and go to the /docs page. This will load the Swagger UI, which gives you an easy way to test the podcast generator. Use the POST endpoint called generate_podcast. Click “Try it out,” enter a topic for your podcast, and submit the request. The API will return the filenames for the generated script and audio.
