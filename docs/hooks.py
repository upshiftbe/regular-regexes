"""MkDocs hook for the shadcn theme.

The theme dates every page from git, and git fails on a file outside the repository: the regex pages are written at
build time (gen_pages.py) into a temporary folder. Those pages are skipped; the others keep their dates.
"""

from pathlib import Path

from shadcn.plugins.mixins import git

_dated = git.GitTimestampsMixin.on_page_markdown


def _on_page_markdown(self, markdown, /, *, page, config, files):
    src = page.file.abs_src_path
    if src and not Path(src).resolve().is_relative_to(Path(config.docs_dir).resolve()):
        # skip the theme's git dates, keep the rest of the plugin chain
        return super(git.GitTimestampsMixin, self).on_page_markdown(markdown, page=page, config=config, files=files)
    return _dated(self, markdown, page=page, config=config, files=files)


git.GitTimestampsMixin.on_page_markdown = _on_page_markdown
