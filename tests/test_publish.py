import getpass
import os
import runpy
import warnings
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest


@pytest.fixture
def publishing(tmp_path, monkeypatch):
    script = Path(__file__).resolve().parents[1] / "scripts" / "publish.py"
    publish = runpy.run_path(str(script))["publish"]
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "ddrr"\nversion = "9.9.9"\n'
    )
    artifacts = tmp_path / "dist" / "9.9.9"
    artifacts.mkdir(parents=True)
    (artifacts / "ddrr-9.9.9-py3-none-any.whl").touch()
    (artifacts / "ddrr-9.9.9.tar.gz").touch()
    (tmp_path / "dist" / "ddrr-0.1.0.tar.gz").touch()
    monkeypatch.delenv("UV_PUBLISH_TOKEN", raising=False)
    prompt = Mock(return_value="pypi-prompt-token")
    upload = Mock(return_value=SimpleNamespace(returncode=0))
    monkeypatch.setattr("getpass.getpass", prompt)
    monkeypatch.setattr("subprocess.run", upload)
    return publish, tmp_path, prompt, upload


def test_publish_uses_environment_token(publishing, monkeypatch):
    publish, root, prompt, upload = publishing
    monkeypatch.setenv("UV_PUBLISH_TOKEN", "pypi-environment-token")
    monkeypatch.setenv("UV_PUBLISH_USERNAME", "stale-user")
    monkeypatch.setenv("UV_PUBLISH_PASSWORD", "stale-password")

    assert publish(root) == 0

    prompt.assert_not_called()
    command = upload.call_args.args[0]
    assert command == [
        "uv",
        "publish",
        "--trusted-publishing",
        "never",
        "--publish-url",
        "https://upload.pypi.org/legacy/",
        "--check-url",
        "https://pypi.org/simple/",
        str(root / "dist" / "9.9.9" / "ddrr-9.9.9-py3-none-any.whl"),
        str(root / "dist" / "9.9.9" / "ddrr-9.9.9.tar.gz"),
    ]
    assert "pypi-environment-token" not in repr(command)
    env = upload.call_args.kwargs["env"]
    assert env["UV_PUBLISH_TOKEN"] == "pypi-environment-token"
    assert "UV_PUBLISH_USERNAME" not in env
    assert "UV_PUBLISH_PASSWORD" not in env
    assert os.environ["UV_PUBLISH_USERNAME"] == "stale-user"


def test_publish_prompts_for_token(publishing):
    publish, root, prompt, upload = publishing
    prompt.return_value = " pypi-prompt-token\n"

    assert publish(root) == 0

    prompt.assert_called_once()
    assert upload.call_args.kwargs["env"]["UV_PUBLISH_TOKEN"] == "pypi-prompt-token"
    assert "UV_PUBLISH_TOKEN" not in os.environ


@pytest.mark.parametrize(
    "filename", ["ddrr-9.9.9-py3-none-any.whl", "ddrr-9.9.9.tar.gz"]
)
def test_publish_requires_both_artifacts(publishing, filename):
    publish, root, prompt, upload = publishing
    (root / "dist" / "9.9.9" / filename).unlink()

    with pytest.raises(SystemExit, match="uv build --out-dir dist/9.9.9"):
        publish(root)

    prompt.assert_not_called()
    upload.assert_not_called()


def test_publish_rejects_empty_token(publishing):
    publish, root, prompt, upload = publishing
    prompt.return_value = "  "

    with pytest.raises(SystemExit, match="token is required"):
        publish(root)

    upload.assert_not_called()


def test_publish_refuses_insecure_prompt(publishing):
    publish, root, prompt, upload = publishing

    def insecure_prompt(*args):
        warnings.warn("No secure terminal", getpass.GetPassWarning, stacklevel=2)
        return "pypi-echoed-token"

    prompt.side_effect = insecure_prompt

    with pytest.raises(SystemExit, match="UV_PUBLISH_TOKEN"):
        publish(root)

    upload.assert_not_called()


def test_publish_propagates_failure(publishing):
    publish, root, _, upload = publishing
    upload.return_value.returncode = 7

    assert publish(root) == 7


@pytest.mark.parametrize(("argument", "exit_code"), [("--dry-run", 2), ("--help", 0)])
def test_publish_cli_does_not_ignore_arguments(
    publishing, monkeypatch, argument, exit_code
):
    _, _, prompt, upload = publishing
    script = Path(__file__).resolve().parents[1] / "scripts" / "publish.py"
    monkeypatch.setattr("sys.argv", [str(script), argument])

    with pytest.raises(SystemExit) as error:
        runpy.run_path(str(script), run_name="__main__")

    assert error.value.code == exit_code
    prompt.assert_not_called()
    upload.assert_not_called()
