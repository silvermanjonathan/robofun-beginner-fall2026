"""Render the printable worksheets to PDF. Run after render.py when a worksheet changes.

Needs WeasyPrint (pip install weasyprint; on a Mac, brew install weasyprint). The web
fonts load from Google Fonts. A machine that cannot reach Google Fonts falls back to
its own fonts unless DM Sans, JetBrains Mono, and Bricolage Grotesque are installed
locally, so after rendering, check the fonts listed in the PDF's properties.
"""

import os

from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get("BVC_OUT", os.path.dirname(HERE))

PAGES = ["session02_worksheet.html"]

for name in PAGES:
    src = os.path.join(SITE, name)
    dst = src[:-5] + ".pdf"
    HTML(src).write_pdf(dst)
    print("wrote", os.path.basename(dst))
