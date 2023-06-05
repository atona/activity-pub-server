from urllib.parse import urlparse

import requests

from src import crud, schemas


def follow_from_actor_service(
    user: schemas.User, actor: str, db: requests.Session
) -> schemas.Follower:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(f"{actor}.json", headers=headers)
    if response.status_code >= 400 and response.status_code < 600:
        raise Exception("actor json request error")

    jsn = response.json()
    if "id" not in jsn or "preferredUsername" not in jsn or "inbox" not in jsn:
        raise Exception("json error")
    domain = urlparse(actor).netloc
    return follow_service(
        user,
        schemas.FollowerCreate(
            ap_id=jsn["id"],
            domain=domain,
            name=jsn["preferredUsername"],
            inbox=jsn["inbox"],
        ),
        db,
    )


def follow_service(
    user: schemas.User,
    follower: schemas.FollowerCreate,
    db: requests.Session,
):
    db_follower = crud.get_or_create_follower(db, follower)
    crud.get_or_create_user_follower(
        db, schemas.UserFollowerCreate(user_id=user.id, follower_id=db_follower.id)
    )
    return db_follower
