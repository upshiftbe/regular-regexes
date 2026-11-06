"""Overlap check: every match the tests produce is also run through every other regex. When another regex returns the
same text, or most of it, the two overlap; every overlap must be listed in tests/overlaps.json with why it's inherent
(the same identifier in two scopes, a number that is valid in two countries' plans, a shape the user chose to keep
bare). A new one fails the run.

pytest --overlaps-update rewrites tests/overlaps.json from a full run; new entries get an empty reason to fill in.
"""

import json
from pathlib import Path

from regular_regexes import rre

ALLOWED = Path(__file__).parent / 'overlaps.json'
_originals, _matches = {}, {}


def pytest_addoption(parser):
    parser.addoption('--overlaps-update', action='store_true', help='rewrite tests/overlaps.json (run the whole suite)')


def _recording(key, f):
    def recorded(text, *args, **kwargs):
        found = f(text, *args, **kwargs)
        _matches.setdefault(key, set()).update(found)
        return found
    return recorded


def pytest_configure(config):
    namespaces = [('', rre)] + [(f'{code}.', ns) for code, ns in vars(rre).items() if not callable(ns)]
    for prefix, ns in namespaces:
        for name, f in list(vars(ns).items()):
            if callable(f):
                _originals[prefix + name] = f
                setattr(ns, name, _recording(prefix + name, f))


def _overlaps():
    pairs = {}
    for key, found in _matches.items():
        for text in found:
            for other, f in _originals.items():
                # password checks one whole value, it doesn't search text
                if other in (key, 'password') or key == 'password':
                    continue
                if any(hit == text or (len(hit) >= len(text) / 2 and (hit in text or text in hit)) for hit in f(text)):
                    pairs.setdefault(f'{key} ~ {other}', text)
    return pairs


def pytest_sessionfinish(session, exitstatus):
    if exitstatus or not _matches:
        return
    found = _overlaps()
    allowed = json.loads(ALLOWED.read_text(encoding='utf-8')) if ALLOWED.exists() else {}
    if session.config.getoption('overlaps_update'):
        text = json.dumps({k: allowed.get(k, '') for k in sorted(found)}, indent=2, ensure_ascii=False) + '\n'
        ALLOWED.write_text(text, encoding='utf-8')
        return
    new = sorted(set(found) - set(allowed))
    if new:
        report = session.config.pluginmanager.get_plugin('terminalreporter')
        report.write_line('')
        report.write_line('Regexes that newly overlap (another regex also matches the example). Tighten one of them, '
                          'or add the pair to tests/overlaps.json with why it is inherent:', red=True)
        for pair in new:
            report.write_line(f'  {pair}: {found[pair]!r}')
        session.exitstatus = 1
