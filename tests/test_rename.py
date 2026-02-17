"""Tests for syntactic_rename."""

import os
import tempfile

from syntactic import syntactic_rename


class TestRename:
    def test_snake_case_rename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            for name in ["Hello World.txt", "FOO BAR.txt"]:
                open(os.path.join(tmpdir, name), "w").close()
            syntactic_rename(tmpdir, fun="snake_case", quiet=True)
            files = sorted(os.listdir(tmpdir))
            assert files == ["foo_bar.txt", "hello_world.txt"]

    def test_kebab_case_rename(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            for name in ["Hello World.txt", "FOO BAR.txt"]:
                open(os.path.join(tmpdir, name), "w").close()
            syntactic_rename(tmpdir, fun="kebab_case", quiet=True)
            files = sorted(os.listdir(tmpdir))
            assert files == ["foo-bar.txt", "hello-world.txt"]

    def test_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            for name in ["Hello World.txt"]:
                open(os.path.join(tmpdir, name), "w").close()
            syntactic_rename(tmpdir, fun="snake_case", dry_run=True, quiet=True)
            files = os.listdir(tmpdir)
            assert files == ["Hello World.txt"]  # unchanged

    def test_specific_file_paths(self) -> None:
        """R-style: pass specific file paths to rename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = []
            for name in ["helloWorld.txt", "fooBar.R"]:
                p = os.path.join(tmpdir, name)
                open(p, "w").close()
                paths.append(p)
            syntactic_rename(paths, fun="kebab_case", quiet=True)
            files = sorted(os.listdir(tmpdir))
            assert files == ["foo-bar.R", "hello-world.txt"]
