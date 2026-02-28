from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model yükleme
with open("synthetic_football_stats_2025.pkl", "rb") as f:
    saved_data = pickle.load(f)

model = saved_data["model"]
scaler = saved_data["scaler"]
preprocessor = saved_data["preprocessor"]

# Takım ve pozisyon listelerini preprocessor'dan çıkar (yoksa varsayılan)
def _get_options():
    teams, positions = [], []
    try:
        ct = preprocessor
        if hasattr(ct, "transformers_"):
            for _name, trans, cols in ct.transformers_:
                if not hasattr(trans, "categories_") or trans.categories_ is None:
                    continue
                col_list = list(cols) if hasattr(cols, "__iter__") and not isinstance(cols, str) else [cols]
                for i, cat in enumerate(trans.categories_):
                    vals = list(cat.astype(str))
                    if i < len(col_list):
                        c = str(col_list[i]).lower()
                        if "team" in c:
                            teams = vals
                        elif "position" in c:
                            positions = vals
            if not teams and hasattr(ct, "transformers_"):
                for _name, trans, _cols in ct.transformers_:
                    if hasattr(trans, "categories_") and trans.categories_ and not teams:
                        teams = list(trans.categories_[0].astype(str))
                        break
            if not positions and hasattr(ct, "transformers_"):
                for _name, trans, _cols in ct.transformers_:
                    if hasattr(trans, "categories_") and len(trans.categories_) >= 2:
                        positions = list(trans.categories_[1].astype(str))
                        break
                if not positions and hasattr(ct, "transformers_"):
                    for _name, trans, _cols in ct.transformers_:
                        if hasattr(trans, "categories_") and trans.categories_:
                            positions = list(trans.categories_[0].astype(str))
                            break
    except Exception:
        pass
    if not teams:
        teams = ["Real Madrid", "Barcelona", "Manchester City", "Bayern Munich", "Liverpool", "PSG", "Juventus", "Chelsea", "Atletico Madrid", "Inter"]
    if not positions:
        positions = ["Forward", "Midfielder", "Defender", "Goalkeeper"]
    return {"teams": teams, "positions": positions}

OPTIONS_CACHE = _get_options()

# Input şeması (futbolcu değeri tahmini)
class PlayerFeatures(BaseModel):
    Team: str
    Position: str
    Age: int
    Matches: int
    Goals: int
    Assists: int
    Pass_Accuracy: float



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/options")
async def get_options():
    return OPTIONS_CACHE

@app.post("/predict")
async def predict(features: PlayerFeatures):
    input_data = pd.DataFrame([features.model_dump()])
    input_encode = preprocessor.transform(input_data)
    input_scaled = scaler.transform(input_encode)
    prediction = model.predict(input_scaled)
    return {"prediction": float(prediction[0])}