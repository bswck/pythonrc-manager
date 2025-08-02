# ruff: noqa: S603, PTH118
from __future__ import annotations

import builtins
import os
import runpy
import shutil
import subprocess
import sys
from collections.abc import Callable, Generator
from contextlib import contextmanager
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from _typeshed import StrPath

PYTHONRC_BASENAME = os.environ.get("PYTHONRC_SCRIPT_BASENAME") or ".repl.py"

_git_bin = shutil.which("git")
if _git_bin is None:
    msg = "git is not installed or not found in PATH."
    raise RuntimeError(msg)
GIT_BIN_PATH = _git_bin


def git_check_ignore(rc_path: StrPath) -> None:
    rc_path = os.fspath(rc_path)
    subprocess.check_output([GIT_BIN_PATH, "-C", git_root(), "check-ignore", rc_path])


def git_root() -> str:
    return subprocess.check_output(
        [GIT_BIN_PATH, "rev-parse", "--show-toplevel"],
        encoding="UTF-8",
    ).strip()


def project_rc_path(basename: str = PYTHONRC_BASENAME) -> str:
    return os.path.relpath(os.path.join(git_root(), basename))


@contextmanager
def allow_reload() -> Generator[None]:
    before = set(sys.modules)
    try:
        yield
    finally:
        # If an exception happened, we still track the modules that were loaded
        # before the exception.
        after = set(sys.modules)
        MODULES_TO_RELOAD.update(after - before)
        MODULES_TO_RELOAD.difference_update(
            sys.builtin_module_names,
            sys.stdlib_module_names,
        )


MODULES_TO_RELOAD: set[str] = set()


def reload_function(
    rc_path: StrPath,
    new_globals: dict[str, object],
) -> Callable[[], None]:
    def reload() -> None:
        clean_module_cache()
        set_last_value(None)
        execute_rc_script(rc_path, new_globals)

    return reload


def execute_rc_script(
    rc_path: StrPath,
    global_ns: dict[str, object],
) -> None:
    rc_path = os.fspath(rc_path)
    # security: lock the file between check-ignore and run_path?
    git_check_ignore(rc_path)
    global_ns.update(
        runpy.run_path(
            rc_path,
            init_globals=global_ns,
            run_name="__main__",
        )
    )


def init_rc_script(
    rc_path: StrPath,
    global_ns: dict[str, object],
) -> None:
    execute_rc_script(rc_path, global_ns)
    global_ns["reload"] = reload_function(rc_path, global_ns)


def clean_module_cache() -> None:
    """Remove modules that were loaded by the REPL script."""
    for module_name in MODULES_TO_RELOAD:
        sys.modules.pop(module_name, None)


def set_last_value(value: object) -> None:
    """Set the last value in the REPL to the given value."""
    builtins._ = value  # type: ignore[attr-defined]


class DisplayHookPatcher:
    original_hook: Callable[[object], None]

    def __init__(self, printer: Callable[[object], None]) -> None:
        self.printer = printer
        self.active = True

    @classmethod
    def pprinting(cls) -> Self:
        import pprint  # noqa: PLC0415

        return cls(pprint.pprint)

    def start(self) -> None:
        """Set up the display hook patcher."""
        set_last_value(None)
        self.original_hook = sys.displayhook
        sys.displayhook = self

    def __call__(self, obj: object) -> None:
        if not hasattr(self, "original_hook"):
            msg = "DisplayHookPatcher is not started. Call start() first."
            raise RuntimeError(msg)
        if self.active:
            if obj is not None:
                self.printer(obj)
                set_last_value(obj)
        else:
            self.original_hook(obj)
