"""Runtime bridge to Factory's evidence-led state backend.

This module is internal.  Connector code keeps using load_state/save_state,
raw writers, Delta writers and DAG exactly as before.  With
SUBSETS_STATE_KERNEL_ENABLED=1 those APIs additionally commit immutable state
snapshots and node-operation events under a shared local/R2 root.

The JSON protocol intentionally matches hardened.state_kernel without making
the deployable connector runtime import the harness package.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from .config import get_bucket_name, get_connector_name, get_data_dir, get_fs, get_r2_prefix, is_cloud
from .storage import backend


PROTOCOL_VERSION = 1


class PointerConflict(RuntimeError):
    pass


def enabled() -> bool:
    return os.environ.get("SUBSETS_STATE_KERNEL_ENABLED", "0").strip().lower() in {
        "1", "true", "yes", "on",
    }


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def _canonical(doc: Any) -> bytes:
    return (json.dumps(doc, sort_keys=True, separators=(",", ":"), default=str) + "\n").encode()


def root() -> str:
    explicit = os.environ.get("SUBSETS_STATE_KERNEL_ROOT")
    if explicit:
        return explicit.rstrip("/")
    if is_cloud():
        prefix = get_r2_prefix()
        base = f"{prefix}/_state-v2" if prefix else "_state-v2"
        return f"s3://{get_bucket_name()}/{base}"
    return str(Path(get_data_dir()) / ".state-kernel")


def _join(*parts: str) -> str:
    first, *tail = parts
    result = first.rstrip("/")
    for part in tail:
        result += "/" + part.strip("/")
    return result


def _read(uri: str) -> bytes | None:
    return backend.read_bytes(uri)


def _write(uri: str, data: bytes) -> None:
    backend.write_bytes(uri, data)


def put_artifact(data: bytes, *, kind: str, metadata: dict[str, Any] | None = None) -> str:
    digest = hashlib.sha256(data).hexdigest()
    ref = f"artifact:sha256:{digest}"
    uri = _join(root(), "artifacts", "sha256", digest[:2], digest)
    existing = _read(uri)
    if existing is None:
        if uri.startswith("s3://"):
            # The key is content-derived; concurrent identical PUTs are safe.
            _write(uri, data)
        else:
            path = Path(uri)
            path.parent.mkdir(parents=True, exist_ok=True)
            try:
                with path.open("xb") as fh:
                    fh.write(data)
            except FileExistsError:
                existing = path.read_bytes()
    if existing is not None and hashlib.sha256(existing).hexdigest() != digest:
        raise RuntimeError(f"content-address collision at {uri}")
    meta_uri = uri + ".json"
    if _read(meta_uri) is None:
        _write(meta_uri, _canonical({
            "ref": ref, "sha256": digest, "size": len(data), "kind": kind,
            "media_type": "application/json", "metadata": metadata or {},
        }))
    return ref


def _artifact_uri(ref: str) -> str:
    prefix = "artifact:sha256:"
    if not ref.startswith(prefix):
        raise ValueError(f"not an artifact ref: {ref}")
    digest = ref[len(prefix):]
    return _join(root(), "artifacts", "sha256", digest[:2], digest)


def append_event(*, operation: str, outcome: str, entity: str | None = None,
                 stage: str | None = None, input_refs=(), output_refs=(),
                 detail: dict[str, Any] | None = None,
                 started_at: str | None = None) -> dict[str, Any]:
    connector = get_connector_name()
    stamp = _now().replace("-", "").replace(":", "").replace("+00:00", "Z").replace(".", "")
    event_id = f"evt_{stamp}_{uuid.uuid4().hex}"
    event = {
        "protocol_version": PROTOCOL_VERSION,
        "event_id": event_id,
        "connector": connector,
        "operation": operation,
        "outcome": outcome,
        "stage": stage,
        "entity": entity,
        "started_at": started_at or _now(),
        "finished_at": _now(),
        "input_refs": list(input_refs),
        "output_refs": list(output_refs),
        "code_revision": os.environ.get("GITHUB_SHA"),
        "detail": detail or {},
    }
    uri = _join(root(), "events", connector, f"{event_id}.json")
    if uri.startswith("s3://"):
        # Event IDs are unguessable and collision-free; an event is never
        # rewritten. R2 receives a single PUT after all referenced outputs.
        _write(uri, _canonical(event))
    else:
        path = Path(uri)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as fh:
            fh.write(_canonical(event))
    return event


def _pointer_uri(name: str) -> str:
    return _join(root(), "pointers", get_connector_name(), f"{name.strip('/')}.json")


def read_pointer(name: str) -> dict[str, Any] | None:
    data = _read(_pointer_uri(name))
    if data is None:
        return None
    doc = json.loads(data)
    if not isinstance(doc, dict):
        raise RuntimeError(f"state pointer {name!r} is not an object")
    return doc


@contextmanager
def _local_lock(uri: str) -> Iterator[None]:
    import fcntl

    path = Path(uri + ".lock")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


def _s3_client():
    import boto3

    return boto3.client(
        "s3",
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        region_name="auto",
    )


def _split_s3(uri: str) -> tuple[str, str]:
    return tuple(uri[len("s3://"):].split("/", 1))  # type: ignore[return-value]


def advance_pointer(name: str, *, target_ref: str, event_id: str,
                    expected_revision: int | None = None) -> dict[str, Any]:
    uri = _pointer_uri(name)

    def make(current: dict[str, Any] | None) -> dict[str, Any]:
        revision = int((current or {}).get("revision", 0))
        if expected_revision is not None and revision != expected_revision:
            raise PointerConflict(f"{name}: expected revision {expected_revision}, found {revision}")
        return {
            "protocol_version": PROTOCOL_VERSION,
            "connector": get_connector_name(),
            "name": name,
            "revision": revision + 1,
            "target_ref": target_ref,
            "event_id": event_id,
            "advanced_at": _now(),
        }

    if not uri.startswith("s3://"):
        with _local_lock(uri):
            doc = make(read_pointer(name))
            _write(uri, _canonical(doc))
            return doc

    from botocore.exceptions import ClientError

    client = _s3_client()
    bucket, key = _split_s3(uri)
    for _ in range(6):
        try:
            response = client.get_object(Bucket=bucket, Key=key)
            current = json.loads(response["Body"].read())
            etag = response.get("ETag")
        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code")
            if code not in {"404", "NoSuchKey", "NotFound"}:
                raise
            current, etag = None, None
        doc = make(current)
        kwargs = {"IfMatch": etag} if etag else {"IfNoneMatch": "*"}
        try:
            client.put_object(Bucket=bucket, Key=key, Body=_canonical(doc), **kwargs)
            return doc
        except ClientError as exc:
            if exc.response.get("Error", {}).get("Code") not in {"412", "PreconditionFailed"}:
                raise
            if expected_revision is not None:
                raise PointerConflict(f"{name}: pointer changed during commit") from exc
    raise PointerConflict(f"{name}: lost six pointer races")


def record_state_snapshot(asset: str, payload: dict[str, Any]) -> str | None:
    if not enabled():
        return None
    data = _canonical(payload)
    ref = put_artifact(data, kind="runtime-state-snapshot",
                       metadata={"connector": get_connector_name(), "asset": asset})
    event = append_event(
        operation="state_snapshot",
        outcome="succeeded",
        entity=asset,
        output_refs=[ref],
        detail={"run_id": os.environ.get("RUN_ID"), "asset": asset},
    )
    advance_pointer(f"runtime-state/{asset}", target_ref=ref, event_id=event["event_id"])
    return ref


def projected_state(asset: str) -> dict[str, Any] | None:
    if not enabled():
        return None
    pointer = read_pointer(f"runtime-state/{asset}")
    if pointer is None:
        return None
    data = _read(_artifact_uri(pointer["target_ref"]))
    if data is None:
        raise RuntimeError(f"state pointer for {asset!r} references a missing artifact")
    doc = json.loads(data)
    if not isinstance(doc, dict):
        raise RuntimeError(f"state artifact for {asset!r} is not an object")
    return doc


def record_node_result(task_id: str, result: dict[str, Any], *, operation: str,
                       stage: str | None, outcome: str) -> dict[str, Any] | None:
    if not enabled():
        return None
    tracking = result.get("tracking") or {}
    evidence = {
        "task_id": task_id,
        "status": result.get("status"),
        "error": result.get("error"),
        "started_at": result.get("started_at"),
        "finished_at": result.get("finished_at"),
        "duration_s": result.get("duration_s"),
        "needs_continuation": bool(result.get("needs_continuation")),
        "tracking": tracking,
        "run_id": os.environ.get("RUN_ID"),
    }
    ref = put_artifact(_canonical(evidence), kind="runtime-node-result",
                       metadata={"connector": get_connector_name(), "task_id": task_id})
    physical_refs: list[str] = []
    versions = tracking.get("asset_versions") or {}
    for rec in tracking.get("io_records") or []:
        if rec.get("operation") != "write":
            continue
        path = rec.get("asset_path")
        if not isinstance(path, str):
            continue
        if path.startswith("subsets/"):
            version = (versions.get(path) or {}).get("version")
            physical_refs.append(f"delta:{path}@{version if version is not None else 'unknown'}")
        elif path.startswith("raw/"):
            physical_refs.append(f"raw:{path[len('raw/'):]}")
    event = append_event(
        operation=operation,
        outcome=outcome,
        entity=task_id,
        stage=stage,
        output_refs=[ref, *dict.fromkeys(physical_refs)],
        detail={"run_id": os.environ.get("RUN_ID"), "task_id": task_id,
                "needs_continuation": bool(result.get("needs_continuation"))},
        started_at=result.get("started_at"),
    )
    return event
