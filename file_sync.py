import os
import shutil
from enum import Enum
from typing import List, NamedTuple


def file_sync(source_dir: str, target_dir: str) -> None:
    (_, _, target_files) = next(os.walk(target_dir))
    for file in target_files:
        os.remove(os.path.join(target_dir, file))

    (_, _, source_files) = next(os.walk(source_dir))
    for file in source_files:
        shutil.copy(src=os.path.join(source_dir, file), dst=os.path.join(target_dir, file))


class FileInfo(NamedTuple):
    name: str
    contents_hash: str


class FileAction(NamedTuple):
    class ActionType(Enum):
        COPY = "COPY"
        DELETE = "DELETE"

    type: ActionType
    source: str
    target: str


def get_sync_actions(source_files: List[FileInfo], target_files: List[FileInfo]) -> List[FileAction]:
    actions = []
    for file in source_files:
        actions.append(FileAction(type=FileAction.ActionType.COPY, source=file.name, target=file.name))
    return actions
