from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        allow_population_by_field_name = True
