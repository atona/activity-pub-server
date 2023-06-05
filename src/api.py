from typing import TypedDict, Union
from xml.dom.minidom import parseString

from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from requests import Session

from . import crud, interfaces, service
from .core.settings import settings
from .main import app, get_db
from .schemas import Follower


@app.get("/@{name}")
@app.get("/users/{name}")
def person(name: str):
    content = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
        ],
        "id": f"{settings.app_base_url()}/users/{name}",  # Fediverseで一意
        "type": "Person",
        "url": f"{settings.app_base_url()}/users/{name}",  # プロフィールページのURL
        "summary": "my simple activitypub",  # 概要
        "preferredUsername": f"{name}",  # ユーザID
        "name": "actor river dragon this help",  # 表示名
        "inbox": f"{settings.app_base_url()}/users/{name}/inbox",  # このユーザへの宛先
        "outbox": f"{settings.app_base_url()}/users/{name}/outbox",  # このユーザの発信元
        "publicKey": {
            "id": f"{settings.app_base_url()}/users/{name}#main-key",
            "owner": f"{settings.app_base_url()}/users/{name}",
            "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyPEg43747qkgIW2vbyZi\nkFmct7co1IiWXXBAoL3JzOPtHLJQGCE7+JogmmGQ3Rl3CdOjcm+0M2/xl9w0oyCU\nyx4STZ9at1Mem1Dq07e/KLMN0w/hXiR4zTeIMuVWx4/jYxjwKT1sp4ermEGmDPRD\nb2HlbN3CzHGJUlsIHSjOP9GtPy24JNItnEff0LoKMwHt6VUo8UEPmuFoxLmgmxD0\nqyryiViw0CGB4nTdy378KWTOFdLADM1LWOkmt/Ao4n0Ho0COABuhWhgPR9ymJa73\nwKbynjpj8wFU7KLuXHOlY0Bl/6mBMb2RjmpFnhJVQgqJAmMCozMw/Mp3Y4JYWsSy\nUwIDAQAB\n-----END PUBLIC KEY-----\n",
        },
    }
    headers = {"Content-Type": "application/activity+json"}
    return JSONResponse(content=content, headers=headers)


@app.get("/users/{name}/note")
def note(name: str):
    content = {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/v1",
        ],
        "id": f"{settings.app_base_url()}/users/{name}/1",  # Fediverseで一意
        "type": "Note",
        "attributedTo": f"{settings.app_base_url()}/users/{name}",  # 投稿者のPerson#id
        "content": "<p>投稿内容</p>",  # XHTMLで記述された投稿内容
        "published": "2018-06-18T12:00:00+09:00",  # ISO形式の投稿日
        "to": [  # 公開範囲
            "https://www.w3.org/ns/activitystreams#Public",  # 公開（連合？）
            f"{settings().app_base_url()}/users/{name}/follower",  # フォロワー
        ],
    }
    headers = {"Content-Type": "application/activity+json"}
    return JSONResponse(content=content, headers=headers)


# InboxModel = TypedDict(
#     "InboxModel",
#     {
#         "@context": str,
#         "type": str,
#         "actor": str,
#         "object": Union[str, TypedDict("Object", {"type": str, "actor": str})],
#     },
# )


class InboxModel(BaseModel):
    type: str
    actor: str
    object: Union[str, interfaces.Object]


@app.post("/users/{name}/inbox")
def inbox(name: str, body: InboxModel, request: Request, db: Session = Depends(get_db)):
    if request.headers["Content-Type"] != "application/activity+json":
        raise HTTPException(status_code=400, detail=f"Not Found.")

    user = crud.get_user_by_name(db, name)
    jsn = body.dict()
    if type(jsn) != dict or "type" not in jsn:
        raise HTTPException(status_code=400, detail=f"Not Found.")
    elif jsn["type"] == "Follow":
        # Follow処理を書く
        follower: Follower = service.follow_from_actor_service(user, jsn["actor"], db)

        # Acceptを返す処理を書く

        return JSONResponse(status_code=200, content={"detaile": "success Follow"})
    elif jsn["type"] == "Undo":
        obj = jsn["object"]
        if type(obj) != dict or "type" not in obj:
            raise HTTPException(status_code=400, detail=f"Not Found.")
        elif obj["type"] == "Follow":
            # Unfollow処理を書く

            # Acceptを返す処理を書く

            return JSONResponse(status_code=200, content={"detaile": "success Undo"})

    raise HTTPException(status_code=501, detail=f"Not Found.")
