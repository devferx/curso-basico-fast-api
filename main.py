# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FasAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, Query, Path, Form

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blode = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="New York",
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="New York",
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="United States",
    )

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Juan"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Perez"
    )
    email: EmailStr = Field(
        ...,
        title="Email",
        description="Email address of the person",
        example="juan@gmail.com"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=21
    )
    hair_color: Optional[HairColor] = Field(default=None, example="black")
    is_married: Optional[bool] = Field(default=None, example=True)
class Person(PersonBase):
    password: str = Field(..., min_length=8)
    # class Config:
    #     schema_extra = {
    #         "example" : {
    #             "first_name": "Fernando",
    #             "last_name": "Quinteros",
    #             "email": "fer@gmail.com",
    #             "age": 20,
    #             "hair_color": "brown",
    #             "is_married": False
    #         }
    #     }

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="devferx")
    message: str = Field(default="Login Successfully!")

@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello": "World"}

# Request and Response Body
@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length = 1,
        max_length = 50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocio"
        ),
    age: str = Query(
        ...,
        title = "Person Age",
        description="This is the person age. It's required",
        example=25
        )
):
    return {"name": name, "age": age}

# Validaciones: Path Parameters
@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the person id. It's required",
        example=123
        )
):
    return {person_id: "It exists!"}

# Validaciones: Request Body
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    # location: Location = Body(...),
):
    # results = person.dict()
    # results.update(location.dict())
    return person

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)