# pythonrc-manager (wip)
Python REPL RC manager that records reloadable imports

# Features
* scoped RC files (write a custom Python RC file per project)
* RCE guards (initially based on `git check-ignore`, which is an imperfect heuristic for many reasons)
* `reloadable():` context manager
* `reload()` REPL function based on diffs of `sys.modules` snapshots from imports in `reloadable()` sections

## Maybe also worth adding
* backported REPL idioms (new REPL `clear`, `exit`) for tail-developed projects
