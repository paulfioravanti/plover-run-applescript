# Plover Run AppleScript

[![Build Status][Build Status image]][Build Status url] [![PyPI - Version][PyPI version image]][PyPI url] [![PyPI - Downloads][PyPI downloads image]][PyPI url] [![linting: pylint][linting image]][linting url]

This [Plover][] [extension][] [plugin][] contains a [command][] that can run
[AppleScript][] code, as well as load in and run external AppleScript files.

## Install

1. In the Plover application, open the Plugins Manager (either click the Plugins
   Manager icon, or from the `Tools` menu, select `Plugins Manager`).
2. From the list of plugins, find `plover-run-applescript`
3. Click "Install/Update"
4. When it finishes installing, restart Plover
5. After re-opening Plover, open the Configuration screen (either click the
   Configuration icon, or from the main Plover application menu, select
   `Preferences...`)
6. Open the Plugins tab
7. Check the box next to `plover_run_applescript` to activate the plugin

## How To Use

### One-Liners

If your AppleScript is one line long, then you can use the code directly in your
steno dictionary entry in the following way:

```json
"KR-PL": "{:COMMAND:APPLESCRIPT:activate application \"Google Chrome\"}"
```

### AppleScript Files

To run code in AppleScript files, create steno dictionary entry values that look
like the following:

```json
"KPH-PBD": "{:COMMAND:APPLESCRIPT:/path/to/your/applescript-file.scpt}"
```

> [!NOTE]
> You can compile your `.applescript` files into [`.scpt`][] files using the
> [`osacompile`][] tool:
>
> ```console
> osacompile -o my-file.scpt my-file.applescript
> ```

The path to your AppleScript file can contain a local `$ENVIRONMENT_VARIABLE`,
which will get expanded. For example, if you have a line like the following in
your `.zshrc` file:

```sh
export STENO_DICTIONARIES="$HOME/steno/steno-dictionaries"
```

You can use it in the command:

```json
"KPH-PBD": "{:COMMAND:APPLESCRIPT:$STENO_DICTIONARIES/path/to/applescript-file.scpt}"
```

### Sending Commands

If you want to test out a command before adding a steno dictionary entry
containing it, you can use Plover's [`plover_send_command`][] command-line tool.
For example:

```console
plover --script plover_send_command "APPLESCRIPT:activate application \"Google Chrome\""
plover --script plover_send_command "APPLESCRIPT:/path/to/your/applescript-file.scpt"
```

> Where `plover` in the command is a reference to your locally installed version
> of Plover. See the [Invoke Plover from the command line][] page for details on
> how to create that reference.

Pressing the "Disconnect and reconnect the machine" button on the Plover UI
resets the AppleScript script cache. If you make any changes to any AppleScript
files, make sure to press it so the file will be re-read in again.

> [!WARNING]
> Due to [this issue][] with [PyXA][], which this plugin relies on to talk to
> Apple's APIs, any AppleScript files that are referenced in a Plover outline
> cannot contain lists in the code (denoted by curly braces; e.g.
> `{"one", "two"}`).
>
> So, if you have code that looks like this:
>
> ```applescript
> keystroke "k" using {command down, shift down}
> ```
>
> You will have to re-write it out longhand to be able to use it with this
> plugin, like so:
>
> ```applescript
> key down command
> key down shift
> keystroke "k"
> key up shift
> key up command
> ```
>
> Or, extract the code you have that uses lists out into [script libraries][].
> I wrote about how I did this in _[Sharing AppleScript Handlers][]_.
>
> **Update**: The AppleScript-related issues have now been fixed, as can be seen
> in the issue. However, since those fixes are only in a version of PyXA that
> uses a Python version later than 3.9, we will have to wait until the Python
> version bundled in with Plover itself updates to at least 3.10 before this
> problem can be properly resolved.

## The Problem

The following is an example of how I used to run AppleScripts from [my Plover
dictionaries][] to perform some kind of automation task that could _only_ be
done on [macOS][] using AppleScript:

```json
"W-D": "{:COMMAND:SHELL:bash -ci 'osascript $STENO_DICTIONARIES/src/command/text/move-one-word-forward.scpt'}"
```

This solution does the following:

- uses the [Plover Run Shell][] plugin to run a shell command from Python
- calls `bash` in [interactive mode][] (`-i`) so that the command can see
  [environment variables][] (`$STENO_DICTIONARIES` in this case) outside of the
  Plover environment
- gets `bash` to use the [`osascript`][] command-line tool to load in and run
  the target compiled AppleScript ([`.scpt`][] file)

Running AppleScripts is generally _slow_, and constantly running one-off
commands that traverse a stack of `Python->Shell->osascript` made them _even
slower_.

So, this plugin leverages [PyXA][] to talk directly to Apple's APIs from Python,
and keeps a local cache of loaded scripts to avoid needing to re-read in
AppleScript files every time a command is run.

The above command now looks like this:

```json
"W-D": "{:COMMAND:APPLESCRIPT:$STENO_DICTIONARIES/src/command/text/move-one-word-forward.scpt}"
```

## Development

Clone from GitHub with [git][]:

```console
git clone git@github.com:paulfioravanti/plover-run-applescript.git
cd plover-run-applescript
python -m pip install --editable ".[test]"
```

If you are a [Tmuxinator][] user, you may find my [plover_run_applescript
project file][] of reference.

### Python Version

Plover's Python environment currently uses version 3.9 (see Plover's
[`workflow_context.yml`][] to confirm the current version).

So, in order to avoid unexpected issues, use your runtime version manager to
make sure your local development environment also uses Python 3.9.x.

### PyXA Version

This plugin depends on [PyXA][] for all Python-to-AppleScript interoperations.
The dependency is currently pinned at [version 0.0.9][] due to later versions
of PyXA using Python 3.10 syntax ([`match case`][] etc) that is too new for
Plover's Python version, and causes syntax errors.

### Testing

- [Pytest][] is used for testing in this plugin.
- [Coverage.py][] and [pytest-cov][] are used for test coverage, and to run
  coverage within Pytest
- [Pylint][] is used for code quality
- [Mypy][] is used for static type checking

Currently, the only parts able to be tested are ones that do not rely directly
on Plover or PyXA.

Run tests, coverage, and linting with the following commands:

```console
pytest --cov --cov-report=term-missing
pylint plover_run_applescript
mypy plover_run_applescript
```

To get a HTML test coverage report:

```console
coverage run --module pytest
coverage html
open htmlcov/index.html
```

If you are a [`just`][] user, you may find the [`justfile`][] useful during
development in running multiple test commands. You can run the following command
from the project root directory:

```console
just --working-directory . --justfile test/justfile
```

### Deploying Changes

After making any code changes, install the plugin into Plover with the following
command:

```console
plover --script plover_plugins install --editable .
```

> Where `plover` in the command is a reference to your locally installed version
> of Plover. See the [Invoke Plover from the command line][] page for details on
> how to create that reference.

When necessary, the plugin can be uninstalled via the command line with the
following command:

```console
plover --script plover_plugins uninstall plover-run-applescript
```

[AppleScript]: https://en.wikipedia.org/wiki/AppleScript
[Build Status image]: https://github.com/paulfioravanti/plover-run-applescript/actions/workflows/ci.yml/badge.svg
[Build Status url]: https://github.com/paulfioravanti/plover-run-applescript/actions/workflows/ci.yml
[command]: https://plover.readthedocs.io/en/latest/plugin-dev/commands.html
[Coverage.py]: https://github.com/nedbat/coveragepy
[environment variables]: https://en.wikipedia.org/wiki/Environment_variable
[extension]: https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
[git]: https://git-scm.com/
[interactive mode]: https://www.gnu.org/software/bash/manual/html_node/Interactive-Shell-Behavior.html
[Invoke Plover from the command line]: https://github.com/openstenoproject/plover/wiki/Invoke-Plover-from-the-command-line
[`just`]: https://github.com/casey/just
[`justfile`]: ./test/justfile
[linting image]: https://img.shields.io/badge/linting-pylint-yellowgreen
[linting url]: https://github.com/pylint-dev/pylint
[macOS]: https://en.wikipedia.org/wiki/MacOS
[`match case`]: https://peps.python.org/pep-0636/
[my Plover dictionaries]: https://github.com/paulfioravanti/steno-dictionaries/tree/main
[Mypy]: https://github.com/python/mypy
[`osacompile`]: https://ss64.com/osx/osacompile.html
[`osascript`]: https://ss64.com/osx/osascript.html
[Plover]: https://www.openstenoproject.org/
[plover_run_applescript project file]: https://github.com/paulfioravanti/dotfiles/blob/master/tmuxinator/plover_run_applescript.yml
[Plover Run Shell]: https://github.com/user202729/plover_run_shell
[`plover_send_command`]: https://plover.readthedocs.io/en/latest/cli_reference.html#sending-commands
[plugin]: https://plover.readthedocs.io/en/latest/plugins.html#types-of-plugins
[Pylint]: https://github.com/pylint-dev/pylint
[PyPI downloads image]:https://img.shields.io/pypi/dm/plover-run-applescript
[PyPI version image]: https://img.shields.io/pypi/v/plover-run-applescript
[PyPI url]: https://pypi.org/project/plover-run-applescript/
[Pytest]: https://pytest.org/
[pytest-cov]: https://github.com/pytest-dev/pytest-cov/
[PyXA]: https://github.com/SKaplanOfficial/PyXA
[`.scpt`]: https://fileinfo.com/extension/scpt
[script libraries]: https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/UseScriptLibraries.html
[Sharing AppleScript Handlers]: https://www.paulfioravanti.com/blog/sharing-applescript-handlers/
[this issue]: https://github.com/SKaplanOfficial/PyXA/issues/16
[Tmuxinator]: https://github.com/tmuxinator/tmuxinator
[version 0.0.9]: https://github.com/SKaplanOfficial/PyXA/tree/v0.0.9
[`workflow_context.yml`]: https://github.com/openstenoproject/plover/blob/master/.github/workflows/ci/workflow_context.yml
