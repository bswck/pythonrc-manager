# pythonrc-manager (wip)

> [!warning]
> Don't use this yet, I'm getting the alpha version ready

Python REPL RC manager that records reloadable imports

# Features

- patch `sys.displayhook` to `pprint` (wrapped to preserve other display hook functionality)
- project-scoped RC scripts (write a custom Python RC file per project) detected with git
- RCE guards (initially based on `git check-ignore`, which is an imperfect heuristic for many reasons)
- `allow_reload()` a context manager and a context decorator that records module names that can be reloaded in the REPL
- `reload()` takes module names recorded in `allow_reload` sections, pops them from `sys.modules` and reexecutes your RC file

## Maybe also worth adding

- backported new REPL idioms (`clear`, `exit`) for tail-developed projects
- autoreloading based on a stat watcher in the background thread?

## Authors

MIT License<br>
(C) Bartosz Sławecki 2025
