from dotenv import load_dotenv
import os
import json
import io
from typing import List, Dict
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from elevenlabs import ElevenLabs
from pydub import AudioSegment

load_dotenv()

#LLM SCRIPT GENERATION
def generate_podcast_script_text(topic: str, llm_model: str) -> str:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ api key is not found in environment variables.")

    prompt = PromptTemplate.from_template("""
    Generate a podcast script (strictly mentioning just dialogues no title, summary or extra text) 
    between a host and a guest about {topic} of strictly only three dialogues for guest and 
    exactly three dialogues for host. Return it as JSON with a list of "dialogue" entries, each having:
    - "speaker": "Host" or "Guest"
    - "text": what they say
    """)

    model = ChatGroq(
        temperature=0.7,
        model_name=llm_model,
        api_key=groq_api_key
    )

    formatted_prompt = prompt.format(topic=topic)
    response = model.invoke(formatted_prompt)

    return response.content

# parsing the json script
def parse_script_to_segments(script_text: str) -> List[Dict[str, str]]:
    cleaned = script_text.strip("```json").strip("```").strip()
    try:
        data = json.loads(cleaned)
        if not isinstance(data, list):
            raise ValueError("Parsed script is not a list of dialogue entries.")
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in script: {e}")

# --- AUDIO GENERATION + COMBINATION ---
def generate_and_combine_audio_from_segments(
    dialogue_segments: List[Dict[str, str]],
    host_voice_id: str,
    guest_voice_id: str,
    output_audio_path: str
) -> None:
    eleven_api_key = os.getenv("ELEVENLABS_API_KEY")
    if not eleven_api_key:
        raise ValueError("ELEVENLABS_API_KEY is not set in environment variables.")

    client = ElevenLabs(api_key=eleven_api_key)
    final_audio = AudioSegment.silent(duration=500)

    for turn in dialogue_segments:
        speaker = turn["speaker"].lower()
        voice_id = host_voice_id if speaker == "host" else guest_voice_id

        response = client.text_to_speech.convert(
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            text=turn["text"],
            output_format="mp3_44100"
        )

        audio_bytes = b"".join(response)
        segment = AudioSegment.from_mp3(io.BytesIO(audio_bytes))
        final_audio += segment + AudioSegment.silent(duration=300)

    final_audio.export(output_audio_path, format="mp3")
