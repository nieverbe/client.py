"""Clean commands."""
from typing import Any

from deebot_client.authentication import Authenticator
from deebot_client.command import CommandResult
from deebot_client.event_bus import EventBus
from deebot_client.events import StateEvent
from deebot_client.logging_filter import get_logger
from deebot_client.message import HandlingResult, MessageBodyDataDict
from deebot_client.models import CleanAction, CleanMode, DeviceInfo, State

from .common import ExecuteCommand, JsonCommandWithMessageHandling

_LOGGER = get_logger(__name__)


class Clean_V2(ExecuteCommand):
    """Clean V2 command."""

    name = "clean_V2"

    def __init__(self, action: CleanAction) -> None:
        super().__init__(self.__get_args(action))

    async def _execute(
        self, authenticator: Authenticator, device_info: DeviceInfo, event_bus: EventBus
    ) -> CommandResult:
        """Execute command."""
        state = event_bus.get_last_event(StateEvent)
        if state and isinstance(self._args, dict):
            if (
                self._args["act"] == CleanAction.RESUME.value
                and state.state != State.PAUSED
            ):
                self._args = self.__get_args(CleanAction.START)
            elif (
                self._args["act"] == CleanAction.START.value
                and state.state == State.PAUSED
            ):
                self._args = self.__get_args(CleanAction.RESUME)

        return await super()._execute(authenticator, device_info, event_bus)

    @staticmethod
    def __get_args(action: CleanAction) -> dict[str, Any]:
        args = {"act": action.value,"content":{"type":"auto","cleanset":"1,0,2,0,1"}}
        if action == CleanAction.START:
            args["type"] = CleanMode.AUTO.value
        return args