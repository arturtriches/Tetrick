from pydantic import BaseModel, Field

class queueCreate(BaseModel):
    player_id : int

class queueResponse(BaseModel):
    id : int
    player_id : int
    message : str = Field(default="Matchmaking...")