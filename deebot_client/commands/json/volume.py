"""Volume command module."""

from types import MappingProxyType
from typing import Any

from deebot_client.command import InitParam
from deebot_client.event_bus import EventBus
from deebot_client.events import VolumeEvent
from deebot_client.message import HandlingResult

from .common import JsonGetCommand, JsonSetCommand


class GetVolume(JsonGetCommand):
    """Get volume command."""

    name = "getVolume"

    @classmethod
    def _handle_body_data_dict(
        cls, event_bus: EventBus, data: dict[str, Any]
    ) -> HandlingResult:
        """Handle message->body->data and notify the correct event subscribers.

        :return: A message response
        """
        event_bus.notify(
            VolumeEvent(volume=data["volume"], maximum=data.get("total", None))
        )
        return HandlingResult.success()


class SetVolume(JsonSetCommand):
    """Set volume command."""

    name = "setVolume"
    get_command = GetVolume
    _mqtt_params = MappingProxyType(
        {
            "volume": InitParam(int),
            "total": None,  # Remove it as we don't can set it (App includes it)
        }
    )

    def __init__(self, volume: int) -> None:
        super().__init__({"volume": volume})
