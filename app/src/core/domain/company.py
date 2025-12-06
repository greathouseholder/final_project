from pydantic import BaseModel


class Company(BaseModel):
    name: str

# TO-DO: переписать, т.к. нельзя в domain использовать pydantic
