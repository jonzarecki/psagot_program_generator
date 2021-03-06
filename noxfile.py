"""Nox sessions."""
import os
from pathlib import Path
from typing import List

import nox
import toml
from nox import Session

package = "psagot_program_generator"
python_versions = ["3.8"]
nox.needs_version = ">= 2021.6.6"
nox.options.sessions = ("tests",)  # , "pre-commit"
pyproject_data = toml.loads(Path("pyproject.toml").read_text())
submodule_paths = []
if os.path.exists(".gitmodules"):
    with open(".gitmodules") as f:
        lines = [s.strip() for s in f.readlines()]
    if "path = common" in lines:  # common is not a submodule of a different repo
        submodule_paths.append("common")


@nox.session(name="pre-commit", python=python_versions)
def pre_commit(sess: Session) -> None:
    """Run pre-commit on all files."""
    sess.install("pre-commit")
    sess.run(*"pre-commit install --install-hooks -t pre-commit -t commit-msg -t post-commit -t pre-push".split(" "))
    sess.run(*"pre-commit run --all-files".split(" "))


@nox.session(python=False)
def tests(sess: Session) -> None:
    """Run the test suite."""
    sess.install("coverage[toml]", "pytest", "pygments")

    def add_quotes_and_join(lst: List[str]) -> str:
        return ",".join([f"{s}" for s in lst])

    omit_paths = ["--omit"] + [
        add_quotes_and_join(pyproject_data["tool"]["coverage"]["run"]["omit"] + [f"{p}/**" for p in submodule_paths])
    ]
    run_paths = [p for p in pyproject_data["tool"]["coverage"]["run"]["source"] if p not in submodule_paths]

    try:
        sess.run("coverage", "run", "--parallel", *omit_paths, "-m", "pytest", *run_paths, *sess.posargs)
    finally:
        sess.notify("coverage", posargs=[])


@nox.session(python=python_versions)
def coverage(sess: Session) -> None:
    """Produce the coverage report."""
    args = sess.posargs or ["report"]

    sess.install("coverage[toml]")

    if not sess.posargs and any(Path().glob(".cache/.coverage.*")):
        # keep .coverage.* files if not interactive (i.e. CI)
        sess.run(*(["coverage", "combine"] + (["--keep"] if not sess.interactive else [])))
    sess.run("coverage", *args)
