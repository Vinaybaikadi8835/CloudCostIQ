from fastapi import FastAPI
from app.api import resources, costs, users

app = FastAPI(
    title="CloudCostIQ",
    description="Cloud Cost Analytics Platform",
    version="1.0.0"
)

# Register all routers with URL prefixes
app.include_router(users.router,     prefix="/users",     tags=["Users"])
app.include_router(resources.router, prefix="/resources", tags=["Resources"])
app.include_router(costs.router,     prefix="/costs",     tags=["Costs"])

@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to CloudCostIQ API"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}