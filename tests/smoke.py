from src.todosyncer.cli import extract_from_text

SAMPLE='''
// TODO: clean this up
- [ ] write docs
- [x] wire parser
'''

items = extract_from_text('x', SAMPLE)
assert any('clean this up' in i.text for i in items)
assert any(i.done for i in items)
print('ok')

