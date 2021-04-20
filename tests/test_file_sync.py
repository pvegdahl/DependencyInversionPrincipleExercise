import os
import shutil
import unittest
from typing import Dict, List

from file_sync import file_sync, FileInfo, get_sync_actions, FileAction


class TestFileSync(unittest.TestCase):
    def setUp(self) -> None:
        self.source_dir_name = "source_dir"
        self.target_dir_name = "target_dir"

        os.mkdir(self.source_dir_name)
        os.mkdir(self.target_dir_name)

    def tearDown(self) -> None:
        shutil.rmtree(self.source_dir_name)
        shutil.rmtree(self.target_dir_name)

    def test_copy_one_file(self):
        file_name = "file_1.txt"
        file_contents = "file contents"
        with open(f"{self.source_dir_name}/{file_name}", "w") as source_file:
            source_file.write(file_contents)

        file_sync(source_dir=self.source_dir_name, target_dir=self.target_dir_name)
        self.assertTrue(os.path.isfile(os.path.join(self.target_dir_name, file_name)))

        with open(os.path.join(self.target_dir_name, file_name), "r") as target_file:
            target_file_contents = target_file.read()
            self.assertEqual(file_contents, target_file_contents)

    def test_delete_one_file(self):
        file_name = "file_1.txt"
        with open(f"{self.target_dir_name}/{file_name}", "w") as target_file:
            target_file.write("whatever")

        file_sync(source_dir=self.source_dir_name, target_dir=self.target_dir_name)
        self.assertFalse(os.path.exists(os.path.join(self.target_dir_name, file_name)))


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
                del target[action.target]
        self.assertEqual(source, target)

