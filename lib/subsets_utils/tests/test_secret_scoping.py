"""Tests for the supervisor's secret scoping.

The cloud workflow hands ALL Actions secrets to the trusted supervisor as one
HARNESS_SECRETS blob; the connector subprocess must only ever see the R2
storage credential plus its OWN CONN_<SLUG>_* secrets, de-prefixed. Runs under
plain python from any connector venv (subsets-utils editable):

    cd src/aaa && uv run python ../../lib/subsets_utils/tests/test_secret_scoping.py
"""
import json
import os
import sys
import traceback

PASS: list[str] = []


def check(name: str, fn):
    try:
        fn()
        PASS.append(name)
        print(f"  ok: {name}")
    except Exception:
        print(f"  FAIL: {name}")
        traceback.print_exc()
        sys.exit(1)


BLOB = {
    "R2_ACCOUNT_ID": "acct",
    "R2_ACCESS_KEY_ID": "key",
    "R2_SECRET_ACCESS_KEY": "r2-secret",
    "R2_BUCKET_NAME": "connectors",
    "GH_RETRIGGER_PAT": "ghp_secret",
    "github_token": "ghs_workflow",
    "CONN_MY_SOURCE_API_KEY": "mine",
    "CONN_OTHER_SOURCE_API_KEY": "theirs",
}


def _expanded():
    from subsets_utils.runner import _expand_bundled_secrets

    for key in BLOB:
        os.environ.pop(key, None)
    os.environ["HARNESS_SECRETS"] = json.dumps(BLOB)
    return _expand_bundled_secrets()


def test_blob_expands_into_supervisor_env():
    names = _expanded()
    assert names == set(BLOB), names
    assert os.environ["GH_RETRIGGER_PAT"] == "ghp_secret"
    assert os.environ["R2_SECRET_ACCESS_KEY"] == "r2-secret"
    assert "HARNESS_SECRETS" not in os.environ


def test_child_env_scoped_to_own_secrets():
    from subsets_utils.runner import _scoped_child_env

    names = _expanded()
    child = _scoped_child_env(os.environ.copy(), "my-source", names)

    # Storage credential crosses (connectors write straight to R2)...
    for name in ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET_NAME"):
        assert child[name] == BLOB[name], name
    # ...its own secret arrives under the bare name...
    assert child["API_KEY"] == "mine"
    # ...and nothing else from the blob survives.
    assert "GH_RETRIGGER_PAT" not in child
    assert "github_token" not in child
    assert "CONN_MY_SOURCE_API_KEY" not in child
    assert "CONN_OTHER_SOURCE_API_KEY" not in child
    assert not any(k.startswith("CONN_") for k in child)


def test_other_connector_never_sees_foreign_secret():
    from subsets_utils.runner import _scoped_child_env

    names = _expanded()
    child = _scoped_child_env(os.environ.copy(), "other-source", names)
    assert child["API_KEY"] == "theirs"
    assert "mine" not in child.values()


def test_explicit_env_var_beats_blob_scrub():
    from subsets_utils.runner import _scoped_child_env

    names = _expanded()
    env = os.environ.copy()
    env["API_KEY"] = "explicitly-set"
    child = _scoped_child_env(env, "my-source", names)
    # setdefault semantics: a var already present in the env wins.
    assert child["API_KEY"] == "explicitly-set"


def test_local_run_without_blob_is_untouched():
    from subsets_utils.runner import _scoped_child_env

    env = {"PATH": "/usr/bin", "BEA_API_KEY": "local-dev"}
    assert _scoped_child_env(dict(env), "my-source", set()) == env


def main():
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            check(name, fn)
    print(f"\n{len(PASS)} checks passed")


if __name__ == "__main__":
    main()
