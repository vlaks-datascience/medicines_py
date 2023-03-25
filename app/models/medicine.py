from pydantic import BaseModel

class Medicine(BaseModel):
    smcid: str
    date: str
    medicine: str
    submission: str
    indication: str
    link_to: str

class Price(BaseModel):
    smcid: str
    medicine: str
    price: float
    