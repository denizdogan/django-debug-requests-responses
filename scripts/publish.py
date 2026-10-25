import argparse
import getpass
import os
import subprocess
import tomllib
import warnings
from pathlib import Path


def publish(root: Path) -> int:
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    version = project["version"]
    name = project["name"].replace("-", "_")
    directory = root / "dist" / version
    artifacts = [
        directory / f"{name}-{version}-py3-none-any.whl",
        directory / f"{name}-{version}.tar.gz",
    ]
    missing = [path.name for path in artifacts if not path.is_file()]
    if missing:
        raise SystemExit(
            f"Missing release artifacts: {', '.join(missing)}. "
            f"Build with: uv build --out-dir dist/{version}"
        )

    token = os.environ.get("UV_PUBLISH_TOKEN")
    if not token:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", getpass.GetPassWarning)
                token = getpass.getpass("PyPI API token: ")
        except (EOFError, getpass.GetPassWarning):
            raise SystemExit(
                "Set UV_PUBLISH_TOKEN when no secure terminal is available."
            ) from None
    token = token.strip()
    if not token:
        raise SystemExit("A PyPI API token is required.")

    env = os.environ.copy()
    env.pop("UV_PUBLISH_USERNAME", None)
    env.pop("UV_PUBLISH_PASSWORD", None)
    env["UV_PUBLISH_TOKEN"] = token
    return subprocess.run(
        [
            "uv",
            "publish",
            "--trusted-publishing",
            "never",
            "--publish-url",
            "https://upload.pypi.org/legacy/",
            "--check-url",
            "https://pypi.org/simple/",
            *(str(path) for path in artifacts),
        ],
        env=env,
        check=False,
    ).returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish the current version to PyPI.")
    parser.parse_args()
    raise SystemExit(publish(Path(__file__).resolve().parents[1]))
