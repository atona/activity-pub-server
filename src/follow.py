from urllib.parse import urlparse

import requests


def follower_from_actor(actor):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(f"{actor}.json", headers=headers)
    if response.status_code >= 400 and response.status_code < 600:
        raise Exception("actor json request error")
    jsn = response.json()
    if "id" not in jsn or "preferredUsername" not in jsn or "inbox" not in jsn:
        raise Exception("json error")
    domain = urlparse(actor).netloc
    # return Follower.objects.get_or_create(
    #     ap_id=jsn["id"],
    #     domain=domain,
    #     name=jsn["preferredUsername"],
    #     inbox=jsn["inbox"],
    # )[0]
