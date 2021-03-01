import os
from datetime import datetime

import xml.sax.saxutils

from settings import SITE_URL, SITEMAP_CHANGEFREQ, SITEMAP_PRIORITY, INDEX_DIR


def build_sitemap_url(path, lastmod=None, changefreq=SITEMAP_CHANGEFREQ, priority=SITEMAP_PRIORITY):
    if lastmod is None:
        lastmod = datetime.today()
    rel_path = os.path.relpath(path, INDEX_DIR)
    return {
        "loc": xml.sax.saxutils.escape(SITE_URL + "/" + rel_path.replace(os.sep, "/")),
        "lastmod": lastmod.strftime("%Y-%m-%d"),
        "changefreq": changefreq,
        "priority": priority
    }
