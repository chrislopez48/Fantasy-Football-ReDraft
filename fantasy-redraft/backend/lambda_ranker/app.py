#AWS lambda function invoked by fastapi
from backend.lambda_ranker.scoring import rank_players    #"." =from the same folder, import function from scoring.py
import logging
from typing import Any
logger=logging.getLogger()
logger.setLevel(logging.INFO)

# adjust the import depending on your file name/location:
# from lambda_ranker.scoring import compute_fantasy_points
# or: from scoring import compute_fantasy_points



def handler(event, context):                     #when someone calls the ranker, start here
    
    top_n=int(event.get("top_n", 50))

    request_id = event.get("request_id", "no-request-id")

    logger.info(f"[{request_id}] Ranker invoked")
    logger.info(f"[{request_id}] Incoming event: {event}")

    players = event.get("players", [])
    settings=event.get("settings", {})
    logger.info(f"[{request_id}] Players received: {len(players)}")

    ranked = rank_players(players,settings, top_n=top_n)
    logger.info(f"[{request_id}] Players ranked: {len(ranked)}")

    return {"ranked": ranked}
