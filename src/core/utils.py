import json
from datetime import datetime
from typing import Literal, Union
from urllib.parse import urlparse

import httpsig
import requests
from Crypto import Random
from Crypto.PublicKey import RSA

from src import schemas

from .settings import settings


def get_ap_id(name: str):
    return f"{settings.app_base_url()}/users/{name}"


def create_key_pair():
    rsa = RSA.generate(2048, Random.new().read)
    return [
        rsa.exportKey().decode("utf-8"),
        rsa.publickey().exportKey().decode("utf-8"),
    ]


def sign_headers(
    account: schemas.UserSecret, method: Literal["POST", "GET"], path: str
):
    sign = httpsig.HeaderSigner(
        get_ap_id(account.name),
        account.private_key,
        algorithm="rsa-sha256",
        headers=["(request-target)", "date"],
    ).sign({"Date": datetime.now().isoformat()}, method=method, path=path)
    auth = sign.pop("authorization")
    sign["Signature"] = (
        auth[len("Signature ") :] if auth.startswith("Signature ") else ""
    )
    sign["User-Agent"] = "Mozilla/5.0"
    return sign


def post_accept(account: schemas.UserSecret, target: schemas.Follower, activity):
    to = target.inbox
    jsn = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Accept",
        "actor": get_ap_id(account.name),
        "object": activity,
    }
    headers = sign_headers(account, "POST", urlparse(to).path)
    response = requests.post(to, json=jsn, headers=headers)
    if response.status_code >= 400 and response.status_code < 600:
        raise Exception("accept post error")
