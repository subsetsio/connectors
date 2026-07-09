"""LEGACY no-op — the python health-test system was removed.

Connectors used to ship a `tests_download.py` whose `test_*` invariants ran
here post-DAG. That system was retired: the only tests are the declarative
per-node specs (`tests/<spec_id>.yaml`), executed by the harness's test
engine against a run's raw and gated by the model stage's published floor.

`run_health_tests` stays as a no-op so main.py files generated before the
removal keep importing and running unchanged; newly scaffolded connectors
don't call it. Delete any leftover `tests_download.py` — nothing reads it.
"""
from __future__ import annotations


def run_health_tests(connector_root) -> None:  # noqa: ARG001 — legacy signature
    """No-op (legacy). The python health-test system was removed; the
    declarative YAML test specs are the only test system."""
    return None
