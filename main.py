import os
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image

port = int(os.environ.get("PORT", 8000))


app = FastAPI()
origins = ["*",]

letters = []

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Message(BaseModel):
    mess: str
    
    
@app.get("/")
async def root():
    return {"message":"Hello from backend"}


@app.get("/reset/")
async def reset():
    letters.clear()
    return{"status":"ok", "word": letters}


@app.post("/text/")
async def text(word:Message):
    letters.append(word.mess)
    return {"status": "ok", "word": letters}


@app.post("/upload/")
async def upload(img: UploadFile = File(...)):
    # Read the file into memory
    input_bytes = await img.read()

    # Remove background
    output_bytes = remove(input_bytes)

    # Wrap bytes in a BytesIO buffer
    output_buffer = BytesIO(output_bytes)

    # Return as image response (PNG by default from rembg)
    return StreamingResponse(output_buffer, media_type="image/png")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)