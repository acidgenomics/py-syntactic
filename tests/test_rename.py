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

    def test_jira_style_filename(self) -> None:
        """Files starting with non-alphanumeric (but not ._~$) should rename."""
        with tempfile.TemporaryDirectory() as tmpdir:
            name = "[PROJ-123] ticket description.txt"
            p = os.path.join(tmpdir, name)
            open(p, "w").close()
            result = syntactic_rename([p], fun="kebab_case", quiet=True)
            assert os.path.basename(result["to"][0]) == "proj-123-ticket-description.txt"

    def test_skip_guard_hidden_files(self) -> None:
        """Files starting with . _ ~ $ should be skipped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            skip_names = ["_test.txt", ".hidden.txt"]
            for name in skip_names:
                open(os.path.join(tmpdir, name), "w").close()
            result = syntactic_rename(
                [os.path.join(tmpdir, n) for n in skip_names],
                fun="kebab_case",
                quiet=True,
            )
            assert result["from"] == result["to"]

    def test_dry_run_returns_mapping(self) -> None:
        """dry_run=True should return the computed from/to mapping."""
        with tempfile.TemporaryDirectory() as tmpdir:
            real_tmpdir = os.path.realpath(tmpdir)
            paths = []
            for name in ["hello_world.txt", "foo_bar.R"]:
                p = os.path.join(real_tmpdir, name)
                open(p, "w").close()
                paths.append(p)
            result = syntactic_rename(paths, fun="kebab_case", dry_run=True, quiet=True)
            assert result["from"] == paths
            assert result["to"] == [
                os.path.join(real_tmpdir, "hello-world.txt"),
                os.path.join(real_tmpdir, "foo-bar.R"),
            ]
            # Files must be unchanged on disk
            assert sorted(os.listdir(real_tmpdir)) == ["foo_bar.R", "hello_world.txt"]
