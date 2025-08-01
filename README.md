# pythonrc-manager (wip)
Python REPL RC manager that records reloadable imports

# Features
* global Python RC with common setup and delegation to scoped RC scripts (see next point)
  * your common setup can for example patch `sys.displayhook` to a function that `pprint`s non-`None` values and records `builtins._`
* project-scoped RC scripts (write a custom Python RC file per project)
* RCE guards (initially based on `git check-ignore`, which is an imperfect heuristic for many reasons)
* `reloadable():` context manager and context decorator
* `reload()`: takes module names recorded in `reloadable` sections, pops them from `sys.modules` and reexecutes your RC file

## Maybe also worth adding
* backported new REPL idioms (`clear`, `exit`) for tail-developed projects
