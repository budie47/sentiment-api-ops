import time
import mlflow
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Production Sentiment API", version="1.0")

print("Loading HuggingFace Model into memory...")
sentiment_model = pipeline("sentiment-analysis")

# --- NEW: Set up the MLflow Tracking "Database" ---
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("Sentiment_API_Tracking")

class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze_text(request: TextRequest):
    start_time = time.time() # Start the stopwatch
    
    # 1. Run the AI Engine
    prediction = sentiment_model(request.text)[0]
    
    end_time = time.time()
    execution_time = round(end_time - start_time, 4) # Calculate duration

    # --- NEW: Log the data to MLflow ---
    with mlflow.start_run():
        # Log parameters (inputs)
        mlflow.log_param("input_length", len(request.text))
        
        # Log metrics (numbers we want to graph later)
        mlflow.log_metric("confidence_score", prediction["score"])
        mlflow.log_metric("execution_time_sec", execution_time)
        
        # Log tags (labels we can use for filtering)
        mlflow.set_tag("prediction_label", prediction["label"])

    return {
        "status": "success",
        "input_text": request.text,
        "result": prediction,
        "execution_time_sec": execution_time
    }