from bcrypt import *
from sqlalchemy import *
from ..db.database import sessaoLocal

def hashOut(crudePass : str):
    encoded = crudePass.encode('utf-8')
    hashed = hashpw(encoded, gensalt())
    return hashed

def hashIn(crudePass : str, player_id : int):
    sessao = sessaoLocal()
    playerCheck = sessao.query(Player).filter_by(id=player_id).first()
    if not player:
        return false
    hashStock = player.hash_password
    encoded = crudePass.encode('utf-8')
    return checkpw(encoded,hashStock)
