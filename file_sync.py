import os
import shutil
from typing import List

from business_logic import get_sync_actions, FileInfo, FileAction


def file_sync(source_dir: str, target_dir: str) -> None:
    target_file_info = _get_file_info(target_dir)
    source_file_info = _get_file_info(source_dir)
    actions = get_sync_actions(source_files=source_file_info, target_files=target_file_info)
    _execute_actions(source_dir=source_dir, target_dir=target_dir, actions=actions)


def _get_file_info(directory: str) -> List[FileInfo]:
    (_, _, files) = next(os.walk(directory))
    return [_file_to_file_info(directory, file) for file in files]


def _file_to_file_info(directory: str, file_name: str) -> FileInfo:
    with open(os.path.join(directory, file_name), "r") as file:
        content_hash = hash(file.read())
        return FileInfo(name=file_name, content_hash=content_hash)


def _execute_actions(source_dir: str, target_dir: str, actions: List[FileAction]) -> None:
    for action in actions:
        if action.type == FileAction.ActionType.COPY:
            shutil.copy(src=os.path.join(source_dir, action.source), dst=os.path.join(target_dir, action.target))
        elif action.type == FileAction.ActionType.DELETE:
            os.remove(os.path.join(target_dir, action.to_delete))