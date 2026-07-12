"""Wikipedia AQS monthly aggregate downloads."""

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, save_raw_parquet
from utils import BASE, START, collect_per_project, get_json, now_end, parse_nested, to_date


def fetch_bytes_difference_absolute(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("abs_bytes_diff", pa.int64()),
    ])

    def path_for(project: str) -> str:
        return (
            f"{BASE}/bytes-difference/absolute/aggregate/{project}/"
            f"all-editor-types/all-page-types/monthly/{START}/{end}"
        )

    collect_per_project(node_id, path_for, parse_nested("abs_bytes_diff"), schema)


def fetch_bytes_difference_net(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("net_bytes_diff", pa.int64()),
    ])

    def path_for(project: str) -> str:
        return (
            f"{BASE}/bytes-difference/net/aggregate/{project}/"
            f"all-editor-types/all-page-types/monthly/{START}/{end}"
        )

    collect_per_project(node_id, path_for, parse_nested("net_bytes_diff"), schema)


def fetch_edited_pages(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("edited_pages", pa.int64()),
    ])

    def path_for(project: str) -> str:
        return (
            f"{BASE}/edited-pages/aggregate/{project}/all-editor-types/"
            f"all-page-types/all-activity-levels/monthly/{START}/{end}"
        )

    collect_per_project(node_id, path_for, parse_nested("edited_pages"), schema)


def fetch_editors(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("editors", pa.int64()),
    ])

    def path_for(project: str) -> str:
        return (
            f"{BASE}/editors/aggregate/{project}/all-editor-types/"
            f"all-page-types/all-activity-levels/monthly/{START}/{end}"
        )

    collect_per_project(node_id, path_for, parse_nested("editors"), schema)


def fetch_edits(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("edits", pa.int64()),
    ])

    def path_for(project: str) -> str:
        return (
            f"{BASE}/edits/aggregate/{project}/all-editor-types/"
            f"all-page-types/monthly/{START}/{end}"
        )

    collect_per_project(node_id, path_for, parse_nested("edits"), schema)


def fetch_mediarequests(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("media_type", pa.string()),
        ("date", pa.string()),
        ("requests", pa.int64()),
    ])
    media_types = ["all-media-types", "image", "audio", "video", "document", "other"]
    rows: list[dict] = []
    ok = 0
    for media_type in media_types:
        url = (
            f"{BASE}/mediarequests/aggregate/all-referers/{media_type}/"
            f"all-agents/monthly/2015010100/{end}"
        )
        try:
            data = get_json(url)
        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            if code != 429 and 400 <= code < 500:
                continue
            raise
        before = len(rows)
        for item in data.get("items", []):
            rows.append({
                "media_type": item["media_type"],
                "date": to_date(item["timestamp"]),
                "requests": item.get("requests"),
            })
        if len(rows) > before:
            ok += 1
    if ok == 0:
        raise RuntimeError(f"{node_id}: no media-request data returned")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=schema), node_id)


def fetch_pageviews(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("views", pa.int64()),
    ])

    def path_for(project: str) -> str:
        return f"{BASE}/pageviews/aggregate/{project}/all-access/all-agents/monthly/{START}/{end}"

    def parse_into(data, rows: list[dict]) -> None:
        for item in data.get("items", []):
            rows.append({
                "project": item["project"],
                "date": to_date(item["timestamp"]),
                "views": item.get("views"),
            })

    collect_per_project(node_id, path_for, parse_into, schema)


def fetch_registered_users_new(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("new_registered_users", pa.int64()),
    ])

    def path_for(project: str) -> str:
        return f"{BASE}/registered-users/new/{project}/monthly/{START}/{end}"

    collect_per_project(node_id, path_for, parse_nested("new_registered_users"), schema)


def fetch_unique_devices(node_id: str) -> None:
    end = now_end()
    schema = pa.schema([
        ("project", pa.string()),
        ("date", pa.string()),
        ("devices", pa.int64()),
        ("offset", pa.int64()),
        ("underestimate", pa.int64()),
    ])

    def path_for(project: str) -> str:
        return f"{BASE}/unique-devices/{project}/all-sites/monthly/{START}/{end}"

    def parse_into(data, rows: list[dict]) -> None:
        for item in data.get("items", []):
            rows.append({
                "project": item["project"],
                "date": to_date(item["timestamp"]),
                "devices": item.get("devices"),
                "offset": item.get("offset"),
                "underestimate": item.get("underestimate"),
            })

    collect_per_project(node_id, path_for, parse_into, schema)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="wikipedia-bytes-difference-absolute",
        fn=fetch_bytes_difference_absolute,
        kind="download",
    ),
    NodeSpec(
        id="wikipedia-bytes-difference-net",
        fn=fetch_bytes_difference_net,
        kind="download",
    ),
    NodeSpec(id="wikipedia-edited-pages", fn=fetch_edited_pages, kind="download"),
    NodeSpec(id="wikipedia-editors", fn=fetch_editors, kind="download"),
    NodeSpec(id="wikipedia-edits", fn=fetch_edits, kind="download"),
    NodeSpec(id="wikipedia-mediarequests", fn=fetch_mediarequests, kind="download"),
    NodeSpec(id="wikipedia-pageviews", fn=fetch_pageviews, kind="download"),
    NodeSpec(
        id="wikipedia-registered-users-new",
        fn=fetch_registered_users_new,
        kind="download",
    ),
    NodeSpec(id="wikipedia-unique-devices", fn=fetch_unique_devices, kind="download"),
]
