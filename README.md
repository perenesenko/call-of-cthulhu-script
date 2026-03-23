# call-of-cthulhu-script

A minimal Python project for building markdown Call of Cthulhu scenarios from structured source files.

## Usage

```bash
python build.py
```

The script reads scenario source files from `sources/scenarios/` and writes assembled markdown files to `dist/`.

## Project structure

```
build.py                          # build script
sources/
  scenarios/
    haunted-house/
      outline.md                  # scenario overview
      characters/
        detective-raymond.md      # character sheet
      scenes/
        01-intro.md               # scene description
dist/                             # generated output (do not edit manually)
.github/workflows/build.yml       # CI workflow
```

## Contributing

See [AGENTS.md](AGENTS.md) for editing guidelines.