from fastapi import FastAPI , Path
import json
from pydantic import BaseModel

app = FastAPI()

class Patient(BaseModel):
    name: str
    city : str
    age : int
    gender : str
    height : float
    weight : float

def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/patients")
async def root():
    return load_data()


@app.get("/patients/{patient_id}" )
async def about_patient(patient_id : str = Path(...,description="patient id")):
    return {"patient_id": patient_id}







