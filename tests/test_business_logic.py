import unittest
from typing import Dict, List

from business_logic import get_sync_actions, FileInfo, FileAction


class TestGetSyncActions(unittest.TestCase):
    def test_copy_one_file(self):
        file_name = "file_1.txt"
        source = {file_name: "file contents"}
        target = {}

        actions = get_sync_actions(
            source_files=self._dir_dict_to_file_info(source),
            target_files=self._dir_dict_to_file_info(target))
        self._validate_actions(source=source, target=target, actions=actions)

    @staticmethod
    def _dir_dict_to_file_info(dir_dict: Dict[str, str]) -> List[FileInfo]:
        return [FileInfo(name=name, content_hash=hash(contents)) for name, contents in dir_dict.items()]

    def test_delete_one_file(self):
        file_name = "file_1.txt"
        source = {}
        target = {file_name: "file contents"}

        actions = get_sync_actions(
            source_files=self._dir_dict_to_file_info(source),
            target_files=self._dir_dict_to_file_info(target))
        self._validate_actions(source=source, target=target, actions=actions)

    def _validate_actions(self, source: Dict[str, str], target: Dict[str, str], actions: List[FileAction]):
        for action in actions:
            if action.type == FileAction.ActionType.COPY:
                target[action.target] = source[action.source]
            elif action.type == FileAction.ActionType.DELETE:
                del target[action.to_delete]
        self.assertEqual(source, target)