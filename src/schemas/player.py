from pydantic import BaseModel, Field, ConfigDict

class playerCreate(BaseModel):
    user : str = Field(min_length = 3, max_length = 25)
    password : str
     
class playerResponse(BaseModel):
    id : int
    user : str = Field(min_length = 3, max_length = 25)
    elo : int
    matches : int
    model_config = ConfigDict(from_attributes=True)