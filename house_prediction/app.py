from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pickle
import pandas as pd
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Model yükleme
with open("House_price_regression.pkl", "rb") as f:
    saved_data = pickle.load(f)

model = saved_data["model"]
scaler = saved_data["scaler"]


# Input şeması
class HousePrice(BaseModel):
    square_footage: int
    bedrooms: int
    bathrooms: int
    lot_size: float
    garage: int
    neighborhood_score: int
    house_age: int

@app.get("/",response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})


@app.post("/predict")
async def predict(features: HousePrice):

    input_data = pd.DataFrame([features.model_dump()])

    # Scale
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction = model.predict(input_scaled)

    return {"prediction": float(prediction[0])}