# syntactic

Make syntactically valid names out of strings.

## Installation

This is a Python package.

```sh
uv pip install syntactic
```

## Usage

```python
from syntactic import (
    camel_case,
    snake_case,
    kebab_case,
    dotted_case,
    upper_camel_case,
    make_names,
    make_words,
    make_title,
    make_label,
    capitalize,
    sentence_case,
    autopad_zeros,
    syntactic_rename,
)

# Case conversion
snake_case(["human genomeVersion", "sampleID"])
# ['human_genome_version', 'sample_id']

camel_case(["human_genome_version", "sample_id"])
# ['humanGenomeVersion', 'sampleId']

upper_camel_case(["human_genome_version", "sample_id"])
# ['HumanGenomeVersion', 'SampleId']

kebab_case(["human genomeVersion", "sampleID"])
# ['human-genome-version', 'sample-id']

dotted_case(["human genomeVersion", "sampleID"])
# ['human.genome.version', 'sample.id']

# Make syntactically valid names
make_names(["%GC", "1st sample", "hello world"])
# ['GC', 'X1st_sample', 'hello_world']

# Human-readable conversions
make_words(["nGene", "log10GenesPerUMI"])
# ['n gene', 'log10 genes per UMI']

make_title(["nGene", "log10GenesPerUMI"])
# ['N gene', 'Log10 genes per UMI']

# Zero padding
autopad_zeros([1, 10, 100])
# ['001', '010', '100']

# File renaming
syntactic_rename("/path/to/dir", fun="snake_case")
```

## Function Reference

| Python Function    | R Equivalent     | Description                         |
|-------------------|------------------|-------------------------------------|
| `camel_case`      | `camelCase`      | Convert to lowerCamelCase           |
| `upper_camel_case`| `upperCamelCase` | Convert to UpperCamelCase           |
| `snake_case`      | `snakeCase`      | Convert to snake_case               |
| `kebab_case`      | `kebabCase`      | Convert to kebab-case               |
| `dotted_case`     | `dottedCase`     | Convert to dotted.case              |
| `make_names`      | `makeNames`      | Make syntactically valid names      |
| `make_words`      | `makeWords`      | Convert to human-readable words     |
| `make_title`      | `makeTitle`      | Convert to title case               |
| `make_label`      | `makeLabel`      | Convert to label (sentence) case    |
| `capitalize`      | `capitalize`     | Capitalize first letter             |
| `sentence_case`   | `sentenceCase`   | Convert to sentence case            |
| `autopad_zeros`   | `autopadZeros`   | Zero-pad integers/strings           |
| `syntactic_rename`| `syntacticRename`| Rename files with syntactic naming  |
