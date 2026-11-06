"""One page per regexes.json folder, written at build time by mkdocs-gen-files."""

import json
import logging
from pathlib import Path

import mkdocs_gen_files
from markdown.extensions.toc import slugify

# a warning fails the --strict build
log = logging.getLogger('mkdocs.plugins.gen_pages')

ROOT = Path(__file__).parent.parent / 'regular_regexes'
# The one-line description of each regex, shown under its heading: docs/descriptions/<folder>.json
DESCRIPTIONS = Path(__file__).parent / 'descriptions'
# The categories a page is split into, in this order. One list for every folder: the names are shared between countries.
CATEGORIES = json.loads((Path(__file__).parent / 'categories.json').read_text(encoding='utf-8'))
CATEGORY = {name: category for category, names in CATEGORIES.items() for name in names}
# Per folder: its name in the navigation, the page's heading, and for search engines the page's title and
# description (the local names of the identifiers are what people search for). A folder not listed shows its code.
PAGES = {
    'intl': ('International', 'International regexes', 'Regexes for email, IBAN, cards, crypto, seed phrases',
             'Python regexes for identifiers used everywhere: email, IBAN, payment cards, IMEI, crypto addresses '
             'and seed phrases, MRZ, VIN, parcels, API keys and hashes.'),
    'be': ('Belgium', 'Belgian regexes', 'Belgian regexes: national number, KBO, IBAN, VAT',
           'Python regexes for Belgian identifiers, with checksum validation: national and BIS number, enterprise '
           'and VAT number, IBAN, OGM, eID, plates and phones.'),
    'de': ('Germany', 'German regexes', 'German regexes: Steuer-ID, USt-IdNr, IBAN, Kennzeichen',
           'Python regexes for German identifiers, with checksum validation: Steuer-ID, USt-IdNr, '
           'Rentenversicherungsnummer, Personalausweis, IBAN, Kennzeichen and phones.'),
    'es': ('Spain', 'Spanish regexes', 'Spanish regexes: DNI, NIE, CIF, IBAN, matrícula',
           'Python regexes for Spanish identifiers, with checksum validation: DNI, NIE, CIF, NIF-IVA, Seguridad '
           'Social, IBAN, passport, matrícula and phone numbers.'),
    'fr': ('France', 'French regexes', 'French regexes: NIR, SIREN, SIRET, TVA, IBAN, RIB',
           'Python regexes for French identifiers, with checksum validation: NIR (sécurité sociale), SIREN, SIRET, '
           'TVA, numéro fiscal, IBAN, RIB, CNI, plates and phones.'),
    'gb': ('United Kingdom', 'UK regexes', 'UK regexes: NI number, NHS number, postcode, VAT',
           'Python regexes for UK identifiers, with checksum validation: National Insurance number, NHS number, UTR, '
           'VAT, sort code, postcode, plates and phones.'),
    'it': ('Italy', 'Italian regexes', 'Italian regexes: codice fiscale, partita IVA, IBAN',
           "Python regexes for Italian identifiers, with checksum validation: codice fiscale, partita IVA, IBAN, "
           "carta d'identità, passport, targa and phone numbers."),
    'lu': ('Luxembourg', 'Luxembourg regexes', 'Luxembourg regexes: matricule, TVA, RCS, IBAN',
           'Python regexes for Luxembourg identifiers, with checksum validation: national number (matricule), TVA, '
           'RCS, IBAN, ID card, passport, plates and phones.'),
    'nl': ('Netherlands', 'Dutch regexes', 'Dutch regexes: BSN, KvK, btw-nummer, IBAN, kenteken',
           'Python regexes for Dutch identifiers, with checksum validation: BSN, RSIN, KvK, btw-nummer, IBAN, '
           'passport and ID card, kenteken, postcode and phones.'),
    'pl': ('Poland', 'Polish regexes', 'Polish regexes: PESEL, NIP, REGON, KRS, IBAN',
           'Python regexes for Polish identifiers, with checksum validation: PESEL, NIP, REGON, KRS, IBAN and NRB, '
           'dowód osobisty, passport, plates and phones.'),
    'ro': ('Romania', 'Romanian regexes', 'Romanian regexes: CNP, CUI, ONRC, IBAN',
           'Python regexes for Romanian identifiers, with checksum validation: CNP, CUI, ONRC trade register number, '
           'IBAN, ID card, passport, plates and phone numbers.'),
}

folders = sorted(f for f in ROOT.iterdir() if (f / 'regexes.json').exists())
# International first, then the countries by code.
folders.sort(key=lambda f: f.name != 'intl')
for folder in folders:
    code = folder.name
    name, heading, seo_title, description = PAGES.get(code, (code.upper(), code.upper(), '', ''))
    prefix = 'rre' if code == 'intl' else f'rre.{code}'
    regexes = json.loads((folder / 'regexes.json').read_text(encoding='utf-8'))
    described = DESCRIPTIONS / f'{code}.json'
    descriptions = json.loads(described.read_text(encoding='utf-8')) if described.exists() else {}
    front = {'title': name, 'description': description}
    if seo_title:
        front['seo_title'] = f"{seo_title} - {mkdocs_gen_files.config['site_name']}"
    # JSON strings are valid YAML, quotes and colons included
    lines = ['---'] + [f'{k}: {json.dumps(v, ensure_ascii=False)}' for k, v in front.items() if v] + ['---', '']
    lines += [f'# {heading}', '']
    if description:
        lines += [description, '']
    entries = {name: e if isinstance(e, dict) else {'regex': e} for name, e in regexes.items()}
    groups = {}
    for name in entries:
        if name not in CATEGORY:
            log.warning(f'{prefix}.{name} has no category in docs/categories.json')
        if name not in descriptions:
            log.warning(f'{prefix}.{name} has no description in docs/descriptions/{code}.json')
        groups.setdefault(CATEGORY.get(name, 'Other'), []).append(name)
    order = [c for c in [*CATEGORIES, 'Other'] if c in groups]
    lines += [
        f'{len(regexes)} regexes, from `regular_regexes/{code}/regexes.json`, called as `{prefix}.<name>(text)`.',
        '',
        ' · '.join(f'[{c}](#{slugify(c, "-")}) ({len(groups[c])})' for c in order),
    ]
    for category in order:
        lines += ['', f'## {category}', '', '| function | checksum validator |', '|---|---|']
        for name in groups[category]:
            validator = entries[name].get('validator')
            check = f'[`{validator}`](../validators.md#{validator})' if validator else ''
            lines.append(f'| [`{prefix}.{name}`](#{name}) | {check} |')
        for name in groups[category]:
            entry = entries[name]
            lines += ['', f'### {name}', '']
            if name in descriptions:
                lines += [descriptions[name], '']
            lines += [f'`{prefix}.{name}(text)`', '', '```text', entry['regex'], '```']
            if 'validator' in entry:
                v = entry['validator']
                args = ', '.join(f'{k} `{a}`' for k, a in entry.items() if k not in ('regex', 'validator'))
                args = f' ({args})' if args else ''
                lines += ['', f'Matches are checked with [`{v}`](../validators.md#{v}){args}; one that fails it is dropped.']
    # the nav sorts pages by file name, with a folder's index first: that is how International stays on top
    with mkdocs_gen_files.open(f"regexes/{'index' if code == 'intl' else code}.md", 'w') as page:
        page.write('\n'.join(lines) + '\n')

# a name left in docs/categories.json after its regex was renamed or removed
known = {name for f in folders for name in json.loads((f / 'regexes.json').read_text(encoding='utf-8'))}
for name in sorted(set(CATEGORY) - known):
    log.warning(f'docs/categories.json lists {name}, which no folder has')
