from pydantic import BaseModel

from typing import Optional
from typing import List
from typing import Dict

class Patient(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: str
    allergies : Optional[List[str]] = None

def update_data(patient : Patient):
    print(patient.first_name + " " + patient.last_name)
    print(f"The age is : {patient.age}")
    print(patient.allergies)

patient_info = {
    "first_name": "John",
    "last_name": "Doe",
    "age": 21,
    "gender": "Male"
}
patient = Patient(**patient_info)
update_data(patient)