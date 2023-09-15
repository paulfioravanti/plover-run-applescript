"""
Plover entry point extension module for Plover Run AppleScript.

    - https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
    - https://plover.readthedocs.io/en/latest/plugin-dev/commands.html
"""
import os
import re

from plover.engine import StenoEngine
from plover.machine.base import STATE_RUNNING
from plover.registry import registry

from PyXA import AppleScript


_ENV_VAR = re.compile(r"(\$[A-Za-z_][A-Za-z_0-9]*)")

class RunAppleScript:
    """
    Extension class that also registers a command plugin.
    The command deals with loading, storing, and running external AppleScript
    files.
    """
    def __init__(self, engine: StenoEngine) -> None:
        self._engine = engine
        self._applescripts = {}

    def start(self) -> None:
        """
        Sets up the command plugin and steno engine hooks
        """
        registry.register_plugin("command", "applescript", self._applescript)
        self._engine.hook_connect(
            "machine_state_changed",
            self._machine_state_changed
        )

    def stop(self) -> None:
        """
        Tears down the steno engine hooks
        """
        self._engine.hook_disconnect(
            "machine_state_changed",
            self._machine_state_changed
        )

    def _applescript(self, _engine: StenoEngine, argument: str) -> None:
        """
        Loads an external AppleScript and stores it in memory for faster
        execution on subsequent calls.
        """
        if not argument:
            raise ValueError("No AppleScript filepath provided")

        try:
            script = self._applescripts[argument]
        except KeyError:
            filepath = RunAppleScript._expand_path(argument)

            try:
                script = AppleScript.load(filepath)
                self._applescripts[argument] = script
            except AttributeError as exc:
                raise ValueError(
                    f"Unable to load file from: {filepath}"
                ) from exc

        script.run()

    def _machine_state_changed(
        self,
        _machine_type: str,
        machine_state: str
    ) -> None:
        """
        This hook will be called when when the Plover UI "Reconnect" button is
        pressed. Resetting the `_applescripts` dictionary allows for changes
        made to external AppleScripts to be re-read in.
        """
        if machine_state == STATE_RUNNING:
            self._applescripts = {}

    @staticmethod
    def _expand_path(path):
        parts = re.split(_ENV_VAR, path)
        expanded_parts = []

        for part in parts:
            if part.startswith("$"):
                # NOTE: Using os.popen with an interactive mode bash command
                # (bash -ci) seemed to be the only way to access a user's env
                # vars on their Mac outside Plover's environment.
                expanded = os.popen(f"bash -ci 'echo {part}'").read().strip()

                if not expanded:
                    raise ValueError(f"No value found for env var: {part}")

                expanded_parts.append(expanded)
            else:
                expanded_parts.append(part)

        return "".join(expanded_parts)
