import asyncio
from contextlib import asynccontextmanager
from fastapi import *
from .schemas.player import *
from .schemas.queue import *
from .db.database import *
from .db.models import *

Base.metadata.create_all(bind=dbEngine) #criando o banco xd kk rs tetrick vai ser hype dimaizi

async def persistencia():
    while True:
        with sessaoLocal() as sessao:
            print(sessao.query(Queue).count())
        await asyncio.sleep(10)

@asynccontextmanager
async def tempoDeVida(app: FastAPI):
    task = asyncio.create_task(persistencia())
    yield 
    task.cancel()
    try:
        await task
    except asyncio.exceptions.CancelledError:
        return 

app = FastAPI(lifespan=tempoDeVida)

def sessionHandler(obj, ses):
    ses.add(obj)
    ses.commit()
    ses.refresh(obj)

@app.post("/createUser")
async def createUser(player : playerCreate):
    sessao = sessaoLocal()
    newPlayer = Player(user=player.user, hash_password="placeholder")
    sessionHandler(newPlayer,sessao)
    return newPlayer

@app.get("/showUser/{player_id}", response_model=playerResponse)
async def showUser(player_id : int):
    sessao = sessaoLocal()
    jogador = sessao.get(Player,player_id)
    return jogador

@app.post("/queueUp", response_model=queueResponse)
async def queueUp(data : queueCreate):
    sessao = sessaoLocal()
    jogador = sessao.get(Player,data.player_id)
    if not jogador:
        raise HTTPException(status_code=404, detail="nem tem player com esse nick")
    if sessao.scalars(select(Queue).filter_by(player_id=data.player_id)).first():
        raise HTTPException(status_code=400, detail="vai entrar na fila dnv paizao?")
    queuePlace = Queue(player_id=data.player_id)
    sessionHandler(queuePlace,sessao)
    return queuePlace
