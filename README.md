# Plover Run AppleScript

This [Plover][] [extension][] [plugin][] contains a [command][] that can load in
and run external [AppleScript][] files.

## The Problem

The reason this plugin exists is because of pain. The following is an example of
how I used to run AppleScripts from [my Plover dictionaries][] to perform some
kind of automation task that could _only_ be done on [macOS][] using
AppleScript:

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

The result is that commands at least _feel_ like they run significantly faster,
and I'm pretty sure it's because they actually are (but I don't have any hard
benchmarks to objectively prove this).

## Install

Until this plugin is added to the Plover registry, download from GitHub or clone
using [git][]:

```sh
git clone git@github.com:paulfioravanti/plover-run-applescript.git
cd plover-run-applescript
plover -s plover_plugins install .
```

> Where `plover` in the command is a reference to your locally installed version
> of Plover. See the [Invoke Plover from the command line][] page for details on
> how to create that reference.

- Restart Plover, open the Configuration screen (either click the Configuration
  icon, or from the main Plover application menu, select `Preferences...`)
- Open the Plugins tab
- Check the box next to `plover_run_applescript` to activate the plugin

\[Future\] Once this plugin is added to the Plover registry:

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

## Development

Clone from GitHub with [git][]:

```sh
git clone git@github.com:paulfioravanti/plover-run-applescript.git
cd plover-run-applescript
```

### Python Version

Plover's Python environment currently uses version 3.9 (see Plover's
[`workflow_context.yml`][] to confirm the current version).

So, in order to avoid unexpected issues, use your runtime version manager to
make sure your local development environment also uses Python 3.9.x.

### PyXA Version

This plugin depends on [PyXA][] for all Python`<->`AppleScript interoperations.
The dependency is currently pinned at [version 0.0.9][] due to later versions
of PyXA using Python 3.10 syntax ([`match case`][] etc) that is too new for
Plover's Python version.

### Testing

Currently, all parts of this extension rely directly on Plover's environment,
which makes testing difficult. So, as of now, no automated tests exist, and all
testing has been done manually.

### Linting

Attempts have been made to have at least some kind of code quality baseline with
[Pylint][]. Run the linter over the codebase with the following command:

```sh
pylint plover_run_applescript
```

### Testing Changes

After making any code changes, install the plugin into Plover with the following
command:

```sh
plover -s plover_plugins install .
```

> Where `plover` in the command is a reference to your locally installed version
> of Plover. See the [Invoke Plover from the command line][] page for details on
> how to create that reference.

[AppleScript]: https://en.wikipedia.org/wiki/AppleScript
[Build Status image]: https://github.com/paulfioravanti/plover-run-applescript/actions/workflows/ci.yml/badge.svg
[Build Status url]: https://github.com/paulfioravanti/plover-run-applescript/actions/workflows/ci.yml
[command]: https://plover.readthedocs.io/en/latest/plugin-dev/commands.html
[environment variables]: https://en.wikipedia.org/wiki/Environment_variable
[extension]: https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
[git]: https://git-scm.com/
[interactive mode]: https://www.gnu.org/software/bash/manual/html_node/Interactive-Shell-Behavior.html
[Invoke Plover from the command line]: https://github.com/openstenoproject/plover/wiki/Invoke-Plover-from-the-command-line
[linting image]: https://img.shields.io/badge/linting-pylint-yellowgreen
[linting url]: https://github.com/pylint-dev/pylint
[macOS]: https://en.wikipedia.org/wiki/MacOS
[`match case`]: https://peps.python.org/pep-0636/
[my Plover dictionaries]: https://github.com/paulfioravanti/steno-dictionaries/tree/main
[`osascript`]: https://ss64.com/osx/osascript.html
[Plover]: https://www.openstenoproject.org/
[Plover Run Shell]: https://github.com/user202729/plover_run_shell
[plugin]: https://plover.readthedocs.io/en/latest/plugins.html#types-of-plugins
[Pylint]: https://github.com/pylint-dev/pylint
[PyXA]: https://github.com/SKaplanOfficial/PyXA
[`.scpt`]: https://fileinfo.com/extension/scpt
[version 0.0.9]: https://github.com/SKaplanOfficial/PyXA/tree/v0.0.9
[`workflow_context.yml`]: https://github.com/openstenoproject/plover/blob/master/.github/workflows/ci/workflow_context.yml
