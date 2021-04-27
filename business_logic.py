from enum import Enum
from typing import List, NamedTuple, Optional


class FileInfo(NamedTuple):
    name: str
    content_hash: int


class FileAction(NamedTuple):
    class ActionType(Enum):
        COPY = "COPY"
        MOVE = "MOVE"
        DELETE = "DELETE"

    type: ActionType
    source: Optional[str] = None
    target: Optional[str] = None
    to_delete: Optional[str] = None


def get_sync_actions(source_files: List[FileInfo], target_files: List[FileInfo]) -> List[FileAction]:
    actions = []
    for file in target_files:
        actions.append(FileAction(type=FileAction.ActionType.DELETE, to_delete=file.name))

    for file in source_files:
        actions.append(FileAction(type=FileAction.ActionType.COPY, source=file.name, target=file.name))
    return actions