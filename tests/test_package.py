# ruff: noqa: F401,PLC0415


def test_importable() -> None:
    from pythonrc_manager import (
        DisplayHookPatcher,
        allow_reload,
        clean_module_cache,
        init_rc_script,
        reload_function,
    )
