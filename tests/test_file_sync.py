import os
import shutil
import unittest

from file_sync import file_sync


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
