import time

import requests

from . import config


class PublishError(Exception):
    def __init__(self, message: str, container_id: str | None = None):
        super().__init__(message)
        self.container_id = container_id


def _raise_for_graph_error(response: requests.Response) -> None:
    if response.ok:
        return
    try:
        message = response.json().get("error", {}).get("message", response.text)
    except ValueError:
        message = response.text
    raise PublishError(f"Graph API error ({response.status_code}): {message}")


def _check_image_reachable(image_url: str, retries: int = 3, delay: int = 2) -> None:
    last_status = None
    for _ in range(retries):
        try:
            resp = requests.head(image_url, timeout=15, allow_redirects=True)
            if resp.ok:
                return
            last_status = resp.status_code
        except requests.RequestException as exc:
            last_status = str(exc)
        time.sleep(delay)
    raise PublishError(f"Image URL not reachable after {retries} attempts (last: {last_status}): {image_url}")


def create_container(image_url: str, caption: str) -> str:
    resp = requests.post(
        f"{config.GRAPH_API_BASE}/{config.IG_USER_ID}/media",
        data={"image_url": image_url, "caption": caption, "access_token": config.META_ACCESS_TOKEN},
        timeout=15,
    )
    _raise_for_graph_error(resp)
    return resp.json()["id"]


def poll_container_status(container_id: str, interval: int | None = None, timeout: int | None = None) -> str:
    interval = interval or config.CONTAINER_POLL_INTERVAL_SECONDS
    timeout = timeout or config.CONTAINER_POLL_TIMEOUT_SECONDS
    elapsed = 0
    while elapsed <= timeout:
        resp = requests.get(
            f"{config.GRAPH_API_BASE}/{container_id}",
            params={"fields": "status_code", "access_token": config.META_ACCESS_TOKEN},
            timeout=15,
        )
        _raise_for_graph_error(resp)
        status = resp.json().get("status_code")
        if status == "FINISHED":
            return status
        if status == "ERROR":
            raise PublishError(f"Container {container_id} failed to process.", container_id=container_id)
        time.sleep(interval)
        elapsed += interval
    raise PublishError(
        f"Container {container_id} still IN_PROGRESS after {timeout}s. "
        "It may still finish server-side — retry publish later against the same entry.",
        container_id=container_id,
    )


def publish_container(container_id: str) -> str:
    resp = requests.post(
        f"{config.GRAPH_API_BASE}/{config.IG_USER_ID}/media_publish",
        data={"creation_id": container_id, "access_token": config.META_ACCESS_TOKEN},
        timeout=15,
    )
    _raise_for_graph_error(resp)
    return resp.json()["id"]


def publish_entry(image_url: str, caption: str, dry_run: bool = False) -> dict:
    if not config.META_ACCESS_TOKEN or not config.IG_USER_ID:
        raise PublishError("META_ACCESS_TOKEN / IG_USER_ID are not set. Copy .env.example to .env and fill it in.")

    _check_image_reachable(image_url)
    container_id = create_container(image_url, caption)
    poll_container_status(container_id)

    if dry_run:
        return {"container_id": container_id, "ig_media_id": None, "dry_run": True}

    ig_media_id = publish_container(container_id)
    return {"container_id": container_id, "ig_media_id": ig_media_id, "dry_run": False}
