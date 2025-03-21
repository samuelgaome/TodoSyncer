#!/usr/bin/env python3
import argparse, pathlib, re
import yaml

TODO_PATTERNS = [re.compile(r"\bTODO\b[: -]?(.*)", re.I)]
CHECKBOX = re.compile(r"^- \[( |x)\] (.*)")


class Todo:
    def __init__(self, path, line_no, text, done=False):
        self.path = str(path)
        self.line_no = line_no
        self.text = text.strip()
        self.done = done

    def as_dict(self):
        return dict(path=self.path, line=self.line_no, text=self.text, done=self.done)


def extract_from_text(path, text):
    items = []
    for i, line in enumerate(text.splitlines(), 1):
        m = CHECKBOX.match(line.strip())
        if m:
            done = (m.group(1).lower() == 'x')
            txt = m.group(2)
            items.append(Todo(path, i, txt, done))
            continue
        for pat in TODO_PATTERNS:
            m = pat.search(line)
            if m:
                items.append(Todo(path, i, m.group(1) or line.strip()))
                break
    return items


def scan(paths):
    todos = []
    for p in paths:
        p = pathlib.Path(p)
        if p.is_file():
            try:
                todos.extend(extract_from_text(p, p.read_text(errors='ignore')))
            except Exception:
                pass
        else:
            for fp in p.rglob('*'):
                if fp.is_file():
                    try:
                        todos.extend(extract_from_text(fp, fp.read_text(errors='ignore')))
                    except Exception:
                        pass
    return todos


def write_yaml(todos, out):
    data = [t.as_dict() for t in todos]
    out_path = pathlib.Path(out)
    out_path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))


def main(argv=None):
    ap = argparse.ArgumentParser(prog='todosyncer')
    ap.add_argument('paths', nargs='+', help='files or directories to scan')
    ap.add_argument('-o', '--out', default='todo.yaml')
    args = ap.parse_args(argv)
    todos = scan(args.paths)
    write_yaml(todos, args.out)
    print(f"Found {len(todos)} todos -> {args.out}")


if __name__ == '__main__':
    main()

