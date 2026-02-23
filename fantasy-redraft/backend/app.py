import uuid
from typing import List, Optional, Any, Dict
from fastapi import FastAPI                     #web framework we're using to create the backend API
from pydantic import BaseModel, Field                  #
from typing import List, Optional
from backend.lambda_ranker.app import handler as ranker_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI                     #another framework for building APIs
from backend.lambda_ranker.scoring import rank_players
from scoring_rules import RULESETS

app = FastAPI()                                 #function we call to do the ranking, "app" is my FF server

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"api": "fantasy-coach", "version": "0.1.0"}


class RankRequest(BaseModel):
    top_n: int = Field(default=50, ge=1, le=500)
    settings: Dict[str, Any] = Field(default_factory=dict)
    players: List[Dict[str, Any]] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=list)

class RankResponse(BaseModel):
    count: int
    players: List[Dict[str, Any]]



@app.post("/rank", response_model=RankResponse)
def rank(req: RankRequest):
    ranked = rank_players(req.players, req.settings, top_n=req.top_n, context=re)
    return {"count": len(ranked), "players": ranked}
                                                   #creates postAPI endpoint


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#class Player(BaseModel):
 #   name: str
  #  position: str
   # projected_points: float

class RankedPlayers(BaseModel):
    ranked: List[Dict[str, Any]]

class RankEvent(BaseModel):
    top_n: int=50
    request_id: Optional[str] = None
    settings: Dict[str, float] = {}
    players: List[Dict[str, Any]] = []

@app.post("/rank_lambda")
def rank_endpoint(event: RankEvent):
    event_dict = event.model_dump()
    if not event_dict.get("request_id"):
        event_dict["request_id"] = str(uuid.uuid4())

    result = ranker_handler(event_dict, context={})
    return result

