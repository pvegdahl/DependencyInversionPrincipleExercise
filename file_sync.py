import os
import shutil
from enum import Enum
from typing import List, NamedTuple, Optional


class FileInfo(NamedTuple):
    name: str
    content_hash: int


class FileAction(NamedTuple):
    class ActionType(Enum):
        COPY = "COPY"
        DELETE = "DELETE"

    type: ActionType
    target: str
    source: Optional[str] = None


def file_sync(source_dir: str, target_dir: str) -> None:
    (_, _, target_files) = next(os.walk(target_dir))
    target_file_info = [_file_to_file_info(target_dir, file) for file in target_files]
    (_, _, source_files) = next(os.walk(source_dir))
    source_file_info = [_file_to_file_info(source_dir, file) for file in source_files]
    actions = get_sync_actions(source_files=source_file_info, target_files=target_file_info)

    for action in actions:
        if action.type == FileAction.ActionType.COPY:
            shutil.copy(src=os.path.join(source_dir, action.source), dst=os.path.join(target_dir, action.target))
        elif action.type == FileAction.ActionType.DELETE:
            os.remove(os.path.join(target_dir, action.target))


def _file_to_file_info(dir: str, file_name: str) -> FileInfo:
    with open(os.path.join(dir, file_name), "r") as file:
        content_hash = hash(file.read())
        return FileInfo(name=file_name, content_hash=content_hash)


def get_sync_actions(source_files: List[FileInfo], target_files: List[FileInfo]) -> List[FileAction]:
    actions = []
    for file in target_files:
        actions.append(FileAction(type=FileAction.ActionType.DELETE, target=file.name))

    for file in source_files:
        actions.append(FileAction(type=FileAction.ActionType.COPY, source=file.name, target=file.name))
    return actions
