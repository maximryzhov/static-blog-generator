import os
import time

import xml.sax.saxutils

from src.settings import SITE_URL, SITEMAP_CHANGEFREQ, SITEMAP_PRIORITY, INDEX_DIR


def build_sitemap_url(path, lastmod=None, changefreq=SITEMAP_CHANGEFREQ, priority=SITEMAP_PRIORITY):
    if lastmod is None:
        lastmod = time.time()
    rel_path = os.path.relpath(path, INDEX_DIR)
    return {
        "loc": xml.sax.saxutils.escape(SITE_URL + "/" + rel_path.replace(os.sep, "/")),
        "lastmod": time.strftime("%Y-%m-%d", time.localtime(lastmod)),
        "changefreq": changefreq,
        "priority": priority
    }
