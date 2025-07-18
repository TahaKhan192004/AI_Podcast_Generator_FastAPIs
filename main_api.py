from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

# Request Model
class PodcastRequest(BaseModel):
    topic: str = Field(..., example="Area 51")
    llm_model: Optional[str] = Field(default="llama-3.1-8b-instant", example="llama-3.1-8b-instant")
    llm_provider: Optional[str] = Field(default="groq", example="groq")
    host_voice: Optional[str] = Field(default="1SM7GgM6IMuvQlz2BwM3", example="1SM7GgM6IMuvQlz2BwM3")
    guest_voice: Optional[str] = Field(default="Dslrhjl3ZpzrctukrQSN", example="Dslrhjl3ZpzrctukrQSN")
    output_audio_filename: Optional[str] = Field(default="podcast.mp3", example="podcast.mp3")
    output_script_filename: Optional[str] = Field(default="podcast_script.txt", example="podcast_script.txt")

# Response Model
class PodcastResponse(BaseModel):
    success: bool
    audio_file: str
    script_file: str
    message: Optional[str] = None

from main import (
    generate_podcast_script_text,
    parse_script_to_segments,
    generate_and_combine_audio_from_segments
)
app = FastAPI()

#api 
@app.post("/generate_podcast", response_model=PodcastResponse)
async def generate_podcast(data: PodcastRequest):
    try:
        #generating podcast script
        try:
            script_text = generate_podcast_script_text(
                topic=data.topic,
                llm_model=data.llm_model
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM script generation failed: {e}")

        #saving it in txt file
        try:
            with open(data.output_script_filename, "w", encoding="utf-8") as f:
                f.write(script_text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save script: {e}")

        #parsing it into segments
        try:
            dialogue_segments = parse_script_to_segments(script_text)
            if not dialogue_segments:
                raise ValueError("No valid dialogue segments parsed.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid dialogue format: {e}")

        #generating audio
        try:
            generate_and_combine_audio_from_segments(
                dialogue_segments=dialogue_segments,
                host_voice_id=data.host_voice,
                guest_voice_id=data.guest_voice,
                output_audio_path=data.output_audio_filename
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Audio generation failed: {e}")

        #final output
        return PodcastResponse(
            success=True,
            audio_file=data.output_audio_filename,
            script_file=data.output_script_filename,
            message="Podcast successfully generated."
        )

    except HTTPException as http_ex:
        raise http_ex
    except Exception as general_ex:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {general_ex}")