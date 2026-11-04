"""One page per regexes.json folder, written at build time by mkdocs-gen-files."""

import json
from pathlib import Path

import mkdocs_gen_files

ROOT = Path(__file__).parent.parent / 'regular_regexes'
# The folder's name on the site; a country not listed shows its code.
NAMES = {
    'intl': 'International', 'be': 'Belgium', 'de': 'Germany', 'es': 'Spain', 'fr': 'France', 'gb': 'United Kingdom',
    'it': 'Italy', 'lu': 'Luxembourg', 'nl': 'Netherlands', 'pl': 'Poland', 'ro': 'Romania',
}

folders = sorted(f for f in ROOT.iterdir() if (f / 'regexes.json').exists())
# International first, then the countries by code.
folders.sort(key=lambda f: f.name != 'intl')
for folder in folders:
    code = folder.name
    title = NAMES.get(code, code.upper())
    prefix = 'rre' if code == 'intl' else f'rre.{code}'
    regexes = json.loads((folder / 'regexes.json').read_text(encoding='utf-8'))
    lines = [
        f'# {title}',
        '',
        f'{len(regexes)} regexes, from `regular_regexes/{code}/regexes.json`, called as `{prefix}.<name>(text)`.',
        '',
        '| function | checksum validator |',
        '|---|---|',
    ]
    entries = {name: e if isinstance(e, dict) else {'regex': e} for name, e in regexes.items()}
    for name, entry in entries.items():
        validator = entry.get('validator')
        check = f'[`{validator}`](../validators.md#{validator})' if validator else ''
        lines.append(f'| [`{prefix}.{name}`](#{name}) | {check} |')
    for name, entry in entries.items():
        lines += ['', f'## {name}', '', f'`{prefix}.{name}(text)`', '', '```text', entry['regex'], '```']
        if 'validator' in entry:
            v = entry['validator']
            args = ', '.join(f'{k} `{a}`' for k, a in entry.items() if k not in ('regex', 'validator'))
            args = f' ({args})' if args else ''
            lines += ['', f'Matches are checked with [`{v}`](../validators.md#{v}){args}; one that fails it is dropped.']
    # the nav sorts pages by file name, with a folder's index first: that is how International stays on top
    with mkdocs_gen_files.open(f"regexes/{'index' if code == 'intl' else code}.md", 'w') as page:
        page.write('\n'.join(lines) + '\n')
