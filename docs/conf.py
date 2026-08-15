# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Instruction"
copyright = "2026, GengRuomei"
author = "GengRuomei"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_nb", "sphinx_copybutton"]
nb_execution_mode = "off"
myst_enable_extensions = ["dollarmath", "amsmath", "colon_fence", "alert"]

language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = ["main.css"]
html_js_files = ["main.js"]
html_favicon = "_static/favicon.png"

pygments_style = "friendly"
pygments_dark_style = "one-dark"

html_permalinks = False
