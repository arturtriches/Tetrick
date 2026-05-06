import asyncio
from contextlib import asynccontextmanager
from fastapi import *
from .schemas.player import *
from .schemas.queue import *
from .db.database import *
from .db.models import *
from .core.security import *
from .api.routers import getCurrentUser

Base.metadata.create_all(bind=dbEngine) #criando o banco xd kk rs tetrick vai ser hype dimaizi

async def persistencia():
    while True:
        with sessaoLocal() as sessao:
            args = select(Queue,Player).join(Player, Player.id == Queue.player_id).order_by(Queue.joinedAt)
            resultados = sessao.execute(args).all()
            if len(resultados) >= 2:
                q1,p1 = resultados[0]
                q2,p2 = resultados[1]
                if abs(p1.elo - p2.elo) <= 100:
                    novaPartida = Match(player1_id=p1.id,player2_id=p2.id,matchStatus="Em Andamento...")
                    sessao.add(novaPartida)
                    sessao.delete(q1)
                    sessao.delete(q2)
                    sessao.commit()
                    print(f"GAME FOUND!!! {p1.user}, {p1.elo} ELO X {p2.user}, {p2.elo} ELO")
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
    senha = hashOut(player.password)
    newPlayer = Player(user=player.user, hash_password= senha)
    sessionHandler(newPlayer,sessao)
    return newPlayer

@app.get("/showUser/{player_id}", response_model=playerResponse)
async def showUser(player_id : int):
    sessao = sessaoLocal()
    jogador = sessao.get(Player,player_id)
    return jogador

@app.post("/queueUp", response_model=queueResponse)
async def queueUp(data : queueCreate = Depends(getCurrentUser)):
    sessao = sessaoLocal()
    jogador = sessao.get(Player,data.player_id)
    if not jogador:
        raise HTTPException(status_code=404, detail="nem tem player com esse nick")
    if sessao.select(Queue).filter_by(player_id=data.player_id).first():
        raise HTTPException(status_code=409, detail="vai entrar na fila dnv paizao?")
    queuePlace = Queue(player_id=data.player_id)
    sessionHandler(queuePlace,sessao)
    return queuePlace
