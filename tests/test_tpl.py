# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
from subprocess import run


def helper(dest):
    run(
        [
            "copier",
            "copy",
            "--trust",
            "-l",
            "-d",
            "author_name=tester",
            "-d",
            "repository=dummy",
            "https://github.com/jupyterlab/extension-template",
            dest,
        ],
        cwd=dest,
        check=True,
    )


def test_files_build(tmp_path):
    extension_folder = tmp_path / "ext"
    extension_folder.mkdir()
    helper(str(extension_folder))

    run(["jlpm", "install"], cwd=extension_folder, check=True)
    run(["jlpm", "run", "build:prod"], cwd=extension_folder, check=True)

    run(["jupyter-builder", "build", str(extension_folder)], cwd=extension_folder, check=True)

    folder_path = extension_folder / "myextension/labextension"

    expected_files = ["static/style.js", "package.json"]

    for filename in expected_files:
        filepath = os.path.join(folder_path, filename)
        assert os.path.exists(filepath), f"File {filename} does not exist in {folder_path}!"


def test_files_build_development(tmp_path):
    extension_folder = tmp_path / "ext"
    extension_folder.mkdir()
    helper(str(extension_folder))

    run(["jlpm", "install"], cwd=extension_folder, check=True)
    run(["jlpm", "run", "build:prod"], cwd=extension_folder, check=True)

    run(
        ["jupyter-builder", "build", "--development", "true", str(extension_folder)],
        cwd=extension_folder,
        check=True,
    )

    folder_path = extension_folder / "myextension/labextension"

    expected_files = ["static/style.js", "package.json", "build_log.json"]

    for filename in expected_files:
        filepath = os.path.join(folder_path, filename)
        assert os.path.exists(filepath), f"File {filename} does not exist in {folder_path}!"
