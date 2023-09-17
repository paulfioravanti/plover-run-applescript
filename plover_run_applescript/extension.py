"""
Plover entry point extension module for Plover Run AppleScript.

    - https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
    - https://plover.readthedocs.io/en/latest/plugin-dev/commands.html
"""
from plover.engine import StenoEngine
from plover.machine.base import STATE_RUNNING
from plover.registry import registry

from .applescript import load, run_code, run_script
from .path import expand_path


_APPLESCRIPT_FILE_EXTENSION = ".scpt"

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
        registry.register_plugin(
            "command",
            "applescript",
            self._run_applescript
        )
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

    def _run_applescript(self, _engine: StenoEngine, argument: str) -> None:
        """
        Loads an external AppleScript and stores it in memory for faster
        execution on subsequent calls.
        """
        if not argument:
            raise ValueError("No AppleScript code/filepath provided")

        if not argument.endswith(_APPLESCRIPT_FILE_EXTENSION):
            return run_code(argument)

        try:
            script = self._applescripts[argument]
        except KeyError:
            filepath = expand_path(argument)
            script = load(filepath)
            self._applescripts[argument] = script

        return run_script(script)

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
