from pydantic import BaseModel


class PersonalInfoModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    gender: str
    city: str
    country: str

    class Config:
        orm_mode = True


class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: str
    city: str
    country: str
