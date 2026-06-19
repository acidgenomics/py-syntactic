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

    def test_kebab_case_non_recursive_r_fixture(self) -> None:
        """Port of R test-rename.R kebabCase (non-recursive): files + dirs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            real_tmpdir = os.path.realpath(tmpdir)
            # Create directories
            for d in ["aaa_bbb", "ccc_ddd"]:
                os.makedirs(os.path.join(real_tmpdir, d))
            # Create files
            file_names = [
                "1_sample_A.fastq.gz",
                "2.sample.B.fastq.gz",
                "hello_world.txt",
                "loadSingleCell.R",
                "quality_control.Rmd",
                "_test.txt",
                "~$excel-temp.xlsx",
                "mikes notes.txt",
                "[PROJ-123] ticket description.txt",
            ]
            for name in file_names:
                open(os.path.join(real_tmpdir, name), "w").close()
            # Build explicit path list (files + dirs) — mirrors R's `input <- c(files, dirs)`
            input_paths = [os.path.join(real_tmpdir, n) for n in file_names] + [
                os.path.join(real_tmpdir, d) for d in ["aaa_bbb", "ccc_ddd"]
            ]
            result = syntactic_rename(input_paths, fun="kebab_case", quiet=True)
            to_basenames = [os.path.basename(p) for p in result["to"]]
            assert to_basenames == [
                "1-sample-a.fastq.gz",
                "2-sample-b.fastq.gz",
                "hello-world.txt",
                "load-single-cell.R",
                "quality-control.Rmd",
                "_test.txt",
                "~$excel-temp.xlsx",
                "mikes-notes.txt",
                "proj-123-ticket-description.txt",
                "aaa-bbb",
                "ccc-ddd",
            ]

    def test_snake_case_non_recursive_r_fixture(self) -> None:
        """Port of R test-rename.R snakeCase (non-recursive)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            real_tmpdir = os.path.realpath(tmpdir)
            for d in ["aaa-bbb", "ccc-ddd"]:
                os.makedirs(os.path.join(real_tmpdir, d))
            for name in ["1-sample-A.fastq.gz", "hello-world.txt"]:
                open(os.path.join(real_tmpdir, name), "w").close()
            input_paths = [
                os.path.join(real_tmpdir, "1-sample-A.fastq.gz"),
                os.path.join(real_tmpdir, "hello-world.txt"),
                os.path.join(real_tmpdir, "aaa-bbb"),
                os.path.join(real_tmpdir, "ccc-ddd"),
            ]
            result = syntactic_rename(input_paths, fun="snake_case", quiet=True)
            to_basenames = [os.path.basename(p) for p in result["to"]]
            assert to_basenames == [
                "1_sample_a.fastq.gz",
                "hello_world.txt",
                "aaa_bbb",
                "ccc_ddd",
            ]

    def test_lowercase_ext(self) -> None:
        """Port of R test-rename.R lowerExt: extension is lowercased."""
        with tempfile.TemporaryDirectory() as tmpdir:
            real_tmpdir = os.path.realpath(tmpdir)
            for name in ["hello_world.TXT", "data.CSV"]:
                open(os.path.join(real_tmpdir, name), "w").close()
            input_paths = [os.path.join(real_tmpdir, n) for n in ["hello_world.TXT", "data.CSV"]]
            result = syntactic_rename(input_paths, fun="kebab_case", lowercase_ext=True, quiet=True)
            to_basenames = [os.path.basename(p) for p in result["to"]]
            assert to_basenames == ["hello-world.txt", "data.csv"]

    def test_camel_case_non_recursive_r_fixture(self) -> None:
        """Port of R test-rename.R camelCase (non-recursive)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            real_tmpdir = os.path.realpath(tmpdir)
            for d in ["aaa-bbb", "ccc-ddd"]:
                os.makedirs(os.path.join(real_tmpdir, d))
            for name in ["1-sample-A.fastq.gz", "hello-world.txt", "helloWORLD.R"]:
                open(os.path.join(real_tmpdir, name), "w").close()
            input_paths = [
                os.path.join(real_tmpdir, "1-sample-A.fastq.gz"),
                os.path.join(real_tmpdir, "hello-world.txt"),
                os.path.join(real_tmpdir, "helloWORLD.R"),
                os.path.join(real_tmpdir, "aaa-bbb"),
                os.path.join(real_tmpdir, "ccc-ddd"),
            ]
            result = syntactic_rename(input_paths, fun="camel_case", quiet=True)
            to_basenames = [os.path.basename(p) for p in result["to"]]
            assert to_basenames == [
                "1SampleA.fastq.gz",
                "helloWorld.txt",
                "helloWorld.R",
                "aaaBbb",
                "cccDdd",
            ]

    def test_upper_camel_case_non_recursive_r_fixture(self) -> None:
        """Port of R test-rename.R upperCamelCase (non-recursive)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            real_tmpdir = os.path.realpath(tmpdir)
            for d in ["aaa-bbb", "ccc-ddd"]:
                os.makedirs(os.path.join(real_tmpdir, d))
            for name in ["1-sample-A.fastq.gz", "hello-world.txt"]:
                open(os.path.join(real_tmpdir, name), "w").close()
            input_paths = [
                os.path.join(real_tmpdir, "1-sample-A.fastq.gz"),
                os.path.join(real_tmpdir, "hello-world.txt"),
                os.path.join(real_tmpdir, "aaa-bbb"),
                os.path.join(real_tmpdir, "ccc-ddd"),
            ]
            result = syntactic_rename(input_paths, fun="upper_camel_case", quiet=True)
            to_basenames = [os.path.basename(p) for p in result["to"]]
            assert to_basenames == [
                "1SampleA.fastq.gz",
                "HelloWorld.txt",
                "AaaBbb",
                "CccDdd",
            ]

    def test_recursive(self) -> None:
        """Port of R test-rename.R kebabCase (recursive): nested directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            real_path = os.path.realpath(tmpdir)
            # Build: root/level_1/level_2/ with files at each level.
            os.makedirs(os.path.join(real_path, "level_1", "level_2"))
            open(os.path.join(real_path, "file_x.TXT"), "w").close()
            open(os.path.join(real_path, "level_1", "file_x.txt"), "w").close()
            open(os.path.join(real_path, "level_1", "level_2", "file_x.txt"), "w").close()
            result = syntactic_rename(real_path, recursive=True, fun="kebab_case", quiet=True)
            # Verify the computed to-paths by basename (order: deepest first).
            to_basenames = [os.path.basename(p) for p in result["to"]]
            assert to_basenames == [
                "file-x.txt",  # level_1/level_2/file_x.txt
                "file-x.txt",  # level_1/file_x.txt
                "file-x.TXT",  # file_x.TXT (extension preserved)
                "level-2",  # level_1/level_2 (dir)
                "level-1",  # level_1 (dir)
                os.path.basename(real_path),  # root unchanged
            ]
