import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image

port = int(os.environ.get("PORT", 8000))

app = FastAPI()

# Allow both your Vercel frontend and mobile access
origins = [
    "https://vjezba-front.vercel.app",
    "http://localhost:3000",
    "http://localhost:8000",
    # Add any other origins you need
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello from backend"}

@app.post("/upload/")
async def upload(img: UploadFile = File(...)):
    try:
        # Read the file into memory
        input_bytes = await img.read()

        # Remove background
        output_bytes = remove(input_bytes)

        # Wrap bytes in a BytesIO buffer
        output_buffer = BytesIO(output_bytes)

        # Return as image response (PNG by default from rembg)
        return StreamingResponse(
            output_buffer, 
            media_type="image/png",
            headers={
                "Access-Control-Allow-Origin": "*",
                "Content-Disposition": "attachment; filename=processed.png"
            }
        )
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)