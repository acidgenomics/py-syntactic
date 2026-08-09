# syntactic

Make syntactically valid names out of strings.

The package improves upon Python's own name-sanitization idioms by adding smart
handling of mixed-case acronyms (e.g. mRNA, RNAi), decimals, and other conventions
commonly used in the life sciences.

The package works in two modes: string mode (default) and file rename mode. There
are five primary naming functions:

- `camel_case` (e.g. `"helloWorld"`).
- `dotted_case` (e.g. `"hello.world"`).
- `snake_case` (e.g. `"hello_world"`).
- `kebab_case` (e.g. `"hello-world"`).
- `upper_camel_case` (e.g. `"HelloWorld"`).

## Installation

### uv method

This package is hosted at [python.acidgenomics.com](https://python.acidgenomics.com/).
We recommend using [uv](https://docs.astral.sh/uv/) to install.

```sh
uv pip install \
    --index-url 'https://python.acidgenomics.com/simple/' \
    syntactic
```

Or add the index to your project's `pyproject.toml`:

```toml
[[tool.uv.index]]
url = "https://python.acidgenomics.com/simple/"
```

Then install:

```sh
uv add syntactic
```

### Conda method

Configure [Conda](https://docs.conda.io/) to use the
[Bioconda](https://bioconda.github.io/) channels.

```sh
# Don't install recipe into base environment.
name='syntactic'
conda create --name="$name" "$name"
conda activate "$name"
python -c 'import syntactic'
```

## String mode

In general, stick with `snake_case` or `camel_case` when sanitizing character
strings.

```pycon
>>> from syntactic import camel_case, make_names, snake_case
>>> object = ["human genomeVersion", "sampleID"]
```

Use snake case formatting inside of scripts:

```pycon
>>> snake_case(object)
['human_genome_version', 'sample_id']
```

Camel case is recommended inside of packages, for function and variable names. The
package offers two variants: relaxed (default) or strict mode. Relaxed mode
generally returns acronyms (e.g. ID) more legibly.

```pycon
>>> camel_case(object, strict=False)
['humanGenomeVersion', 'sampleID']
>>> camel_case(object, strict=True)
['humanGenomeVersion', 'sampleId']
```

`make_names` sanitizes arbitrary strings into valid Python identifiers,
underscore-separated:

```pycon
>>> make_names(["%GC", "1st sample", "hello world"])
['GC', 'X1st_sample', 'hello_world']
```

## Human-readable conversions

`make_words` and `make_title` go the other direction, converting a syntactic
variable name back into readable prose:

```pycon
>>> from syntactic import make_title, make_words
>>> make_words(["nGene", "log10GenesPerUMI"])
['n gene', 'log10 genes per UMI']
>>> make_title(["nGene", "log10GenesPerUMI"])
['N gene', 'Log10 genes per UMI']
```

## File rename mode

The package also supports file name sanitization via `syntactic_rename`. This
currently includes support for `kebab_case` (recommended), `snake_case`, and
`camel_case`, via the `fun` argument:

```pycon
>>> from syntactic import syntactic_rename
>>> syntactic_rename("/path/to/dir", fun="kebab_case")  # doctest: +SKIP
```

Recursion into subdirectories is supported using `recursive=True`, and `dry_run=True`
previews the renames without touching the filesystem.

## See also

If syntactic doesn't work quite right for your workflow, these popular packages
also provide sanitization support:

- [python-slugify](https://pypi.org/project/python-slugify/)
- [inflection](https://pypi.org/project/inflection/)

```{toctree}
:maxdepth: 1
:caption: Contents
:hidden:

reference/index
changelog
```
