import os
import uuid

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from src.pipeline.inference import run_full_pipeline

os.makedirs("data", exist_ok=True)

app = FastAPI(
    title="Customer Support QA Evaluator",
    version="1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return "Hello, I am alive!"


@app.get("/")
def health_check():
    return {"message": "QA Evaluator API is running fine!!"}


@app.post("/evaluate")
async def evaluate_file(file: UploadFile = File(...)):
    allowed_extensions = [".csv", ".xlsx"]

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        return {"error": "Invalid file format. Only CSV and Excel files are allowed."}

    input_path = f"data/{uuid.uuid4()}{file_extension}"
    output_path = f"data/output_{uuid.uuid4()}.xlsx"

    # Save Uploaded File
    with open(input_path, "wb") as f:
        content = await file.read()
        f.write(content)

    if file_extension == ".csv":
        df = pd.read_csv(input_path)
    elif file_extension == ".xlsx":
        df = pd.read_excel(input_path)
    else:
        return {"error": "Invalid file format. Only CSV and Excel files are allowed."}

    output_df = run_full_pipeline(df, output_path)
    output_df.to_excel(output_path, index=False)

    return FileResponse(
        output_path,
        filename="qa_output.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
