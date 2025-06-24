import os
import sys

sys.path.insert(0, os.path.abspath("../../src/"))

# -- Project information
project = "ultra-piston"
copyright = "2025-present, Jiggly Balls"
author = "Jiggly Balls"

# version = f"{version_info.major}.{version_info.minor}"
# release = f"{version_info.major}.{version_info.minor}.{version_info.patch} - {version_info.releaselevel}"


version = "1.0"
release = "1.0.0 - final"

# -- General configuration
extensions = [
    "sphinxcontrib.autodoc_pydantic",
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "numpydoc",
    # "sphinx.ext.numpydoc",
    # "sphinx.ext.napolean",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
]
# extensions = ["sphinx.ext.autodoc", "sphinx.ext.napolean"]
source_encoding = "utf-8"
exclude_patterns = ["_build", ".DS_Store"]
html_theme = "furo"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

autodoc_member_order = "bysource"  # This because idk how to make properties appear separately from methods...
intersphinx_disabled_domains = ["std"]
napoleon_use_param = True
numpydoc_show_class_members = False
# numpydoc_attributes_as_param_list = False
toc_object_entries = False
always_document_param_types = True
toc_object_entries_show_parents = "hide"
autosectionlabel_prefix_document = True
autosummary_generate = False
autosummary_generate_overwrite = False
autodoc_typehints = "none"  # "description"
autodoc_typehints_description_target = "documented_params"
autoclass_content = "both"

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "friendly"

templates_path = ["_templates"]
modindex_common_prefix = ["src."]

# -- Options for HTML output
html_title = f"{project} v{version} Documentation"
html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/Jiggly-Balls/game-state",
    "source_branch": "main",
    "source_directory": "docs/source/",
    "top_of_page_buttons": ["view", "edit"],
}
htmlhelp_basename = "ultra_piston_doc"

# -- Options for EPUB output
epub_show_urls = "footnote"
