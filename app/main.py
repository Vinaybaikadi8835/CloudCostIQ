from fastapi import FastAPI

app = FastAPI(
    title="CloudCostIQ",
    description="Cloud Cost Analytics Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to CloudCostIQ API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}