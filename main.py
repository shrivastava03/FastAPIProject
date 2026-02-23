from fastapi import FastAPI, Path, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated , Literal
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]


@computed_field
@property
def bmi(self) -> float:
    bmi = round(self.weight / (self.height ** 2), 2)
    return bmi


@computed_field
@property
def verdict(self) -> str:
    if self.bmi < 18.5:
        return 'Underweight'
    elif self.bmi < 25:
        return 'Normal'
    elif self.bmi < 30:
        return 'Normal'
    else:
        return 'Obese'


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()

    return data
@app.get("/patients")
async def root():
    return load_data()


@app.get("/patients/{patient_id}" )
async def about_patient(patient_id : str = Path(...,description="patient id")):
    return {"patient_id": patient_id}


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'),
                  order: str = Query('asc', description='sort in asc or desc order')):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')

    data = load_data()

    sort_order = True if order == 'desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data
@app.post("/create")
async def create_patient(patient : Patient):
    #loading data
    data = load_data()

    #check uf patient already exists or not
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude = ['id'])

    save_data(data)

    return JSONResponse(status_code=201,content= "Patient created successfully")



