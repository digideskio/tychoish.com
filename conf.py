# -*- coding: utf-8 -*-
#
# MongoDB documentation build configuration file, created by
# sphinx-quickstart on Mon Oct  3 09:58:40 2011.
#
# This file is execfile()d with the current directory set to its containing dir.

import sys
import os
import datetime
import logging
import random

from giza.config.runtime import RuntimeStateConfig
from giza.config.helper import fetch_config, get_versions

logging.basicConfig(level=logging.INFO)
conf = fetch_config(RuntimeStateConfig())
sconf = conf.system.files.data.sphinx_local

sys.path.append(os.path.join(conf.paths.projectroot, conf.paths.buildsystem, 'sphinxext'))

# -- General configuration ----------------------------------------------------

needs_sphinx = '1.0'

extensions = [
    'sphinx.ext.extlinks',
    'sphinx.ext.todo',
    'ablog',
    'alabaster',
]

import ablog
import alabaster

blog_baseurl = 'http://tychoish.com/'
blog_feed_archives = True
blog_feed_fulltext = True
blog_archive_titles = True
fontawesome_link_cdn = True


disqus_shortname = 'tychoish'
disqus_pages = False

locale_dirs = [ os.path.join(conf.paths.projectroot, conf.paths.locale) ]
gettext_compact = False

templates_path = ['.templates', ablog.get_html_templates_path() ]

exclude_patterns = []

source_suffix = '.txt'

master_doc = sconf.master_doc
language = 'en'
project = sconf.project
copyright = u'2002-{0} tycho garen'.format(datetime.date.today().year)
version = conf.version.branch
release = conf.version.release

taglines = [
    'Uncertain Seas',
    'Visits, Modes, and Forms',
    'Fly from my Thoughts',
]
rst_epilog = '\n'.join([
    '.. |branch| replace:: ``{0}``'.format(conf.git.branches.current),
    '.. |copy| unicode:: U+000A9',
    '.. |year| replace:: {0}'.format(datetime.date.today().year),
    '.. |hardlink| replace:: {0}/{1}'.format(conf.project.url, conf.git.branches.current),
])

pygments_style = 'sphinx'

extlinks = { }

## add `extlinks` for each published version.
for i in conf.git.branches.published:
    extlinks[i] = ( ''.join([ conf.project.url, '/', i, '%s' ]), '' )

intersphinx_mapping = {}
for i in conf.system.files.data.intersphinx:
    intersphinx_mapping[i.name] = ( i.url, os.path.join(conf.paths.projectroot,
                                                        conf.paths.output,
                                                        i.path))

# -- Options for HTML output ---------------------------------------------------

html_theme = sconf.theme.name
html_theme_path = [ os.path.join(conf.paths.output, 'institute-tools', 'themes'), alabaster.get_path() ]
html_title = conf.project.title
htmlhelp_basename = 'rhizome'

html_logo = None
html_static_path = sconf.paths.static

html_copy_source = False
html_use_smartypants = True
html_domain_indices = True
html_use_index = True
html_split_index = False
html_show_sourcelink = False
html_show_sphinx = True
html_show_copyright = True

html_theme_options = {
    'analytics_id': sconf.theme.google_analytics,
}

html_sidebars = sconf.sidebars

# -- Options for Blogging --------------------------------------------------

blog_authors = {
    'tychoish': ('tychoish', 'http://tychoish.net'),
    'Sam Kleinman': ('Sam Kleinman', 'http://tychoish.net'),
}

post_date_format = "%Y-%m-%d"

# -- Options for LaTeX output --------------------------------------------------

latex_documents = []
if 'pdfs' in conf.system.files.data:
    for pdf in conf.system.files.data.pdfs:
        latex_documents.append((pdf.source, pdf.output, pdf.title, pdf.author, pdf.doc_class))

latex_preamble_elements = [ r'\DeclareUnicodeCharacter{FF04}{\$}',
                            r'\DeclareUnicodeCharacter{FF0E}{.}',
                            r'\PassOptionsToPackage{hyphens}{url}',
                            r'\usepackage{upquote}',
                            r'\pagestyle{plain}',
                            r'\pagenumbering{arabic}' ]
latex_elements = {
    'preamble': '\n'.join(latex_preamble_elements),
    'pointsize': '10pt',
    'papersize': 'letterpaper'
}

latex_paper_size = 'letter'
latex_use_parts = False
latex_show_pagerefs = True
latex_show_urls = 'footnote'
latex_domain_indices = False
latex_logo = None
latex_appendices = []

# -- Options for manual page output --------------------------------------------

man_pages = []
if 'manpages' in conf.system.files.data:
    for mp in conf.system.files.data.manpages:
        man_pages.apend((mp.file, mp.name, mp.title, mp.authors, mp.section))

# -- Options for Epub output ---------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = conf.project.title
epub_author = u'MongoDB Documentation Project'
epub_publisher = u'MongoDB, Inc.'
epub_copyright = copyright
epub_theme = 'epub_mongodb'
epub_tocdup = True
epub_tocdepth = 3
epub_language = language
epub_scheme = 'url'
epub_identifier = '/'.join([conf.project.url, conf.git.branches.current])
epub_exclude_files = []

epub_pre_files = []
epub_post_files = []

# put it into your conf.py
def setup(app):
    # disable versioning for speed
    from sphinx.builders.gettext import I18nBuilder
    I18nBuilder.versioning_method = 'none'

    def doctree_read(app, doctree):
        if not isinstance(app.builder, I18nBuilder):
            return
        from docutils import nodes
        from sphinx.versioning import add_uids
        list(add_uids(doctree, nodes.TextElement))
    app.connect('doctree-read', doctree_read)
