# TodoSyncer

A tiny solo project: a local-first CLI to aggregate TODOs from multiple folders into a single YAML file, and sync back status.

- No services, just files
- Parse // TODO, # TODO, and Markdown checkboxes
- Write summary to `todo.yaml`

## Usage

Run:

python -m src.todosyncer.cli . -o todo.yaml

## Notes

Future: edit todo.yaml and push status back to files.

