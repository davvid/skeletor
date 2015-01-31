import sys, os

sys.path.insert(0, os.path.abspath('..'))
import skeletor
import skeletor.core.version

sys.path.insert(1, os.path.abspath('.'))
try:
    import sphinxtogithub
    sphinxtogithub #  import side-effects
except ImportError, e:
    raise ImportError('Could not import sphinxtogithub\n'
                      'Is the git submodule populated at thirdparty/sphinx-to-github?\n'
                      'At the project root run:\n'
                      '\tgit submodule init\n'
                      '\tgit submodule update')

extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.doctest',
        'sphinx.ext.intersphinx',
        'sphinx.ext.todo',
        'sphinx.ext.coverage',
        'sphinxtogithub',
        ]

sphinx_to_github = True

templates_path = ['templates']
source_suffix = '.rst'
source_encoding = 'utf-8'
master_doc = 'index'

project = 'skeletor'
copyright = '2015, David Aguilar'
version = skeletor.core.version.VERSION
release = version

exclude_trees = []
pygments_style = 'default'

html_theme = 'default'
html_static_path = filter(os.path.exists, ['static'])
htmlhelp_basename = 'doc'

latex_documents = [
  ('index', 'index.tex', 'Skeletor Documentation',
   'David Aguilar', 'manual'),
]

intersphinx_mapping = {'http://docs.python.org/': None}
