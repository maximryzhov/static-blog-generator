from os import listdir
from os.path import isfile, join
from datetime import datetime
import json
from collections import defaultdict

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from jinja2 import FileSystemLoader, Environment

from settings import *
from utils import slugify, remove_tags
from template_filters import date_filter, rfc822_filter
from sitemap import build_sitemap_url
from paginator import Paginator


def get_env():
    """
    Returns Jinja2 environment instance
    with required globals and filters set up
    """
    loader = FileSystemLoader(TEMPLATES_DIR)
    env = Environment(loader=loader)
    env.filters.update({
        'date': date_filter,
        'rfc822': rfc822_filter
    })
    env.globals.update({
        'SITE_NAME': SITE_NAME,
        'SITE_URL': SITE_URL,
        'SITE_DESCRIPTION': SITE_DESCRIPTION,
        'SITE_KEYWORDS': SITE_KEYWORDS,
        "SITE_LANGUAGE": SITE_LANGUAGE,
        'ADMIN_EMAIL': ADMIN_EMAIL,
        'GOOGLE_ANALYTICS_ID': GOOGLE_ANALYTICS_ID,
        'WIDGETPACK_ID': WIDGETPACK_ID
    })
    return env


def load_drafts():
    """
    Loads draft files from the DRAFTS_DIR
    returns list of strings with file contents
    """
    drafts = []
    for item in listdir(DRAFTS_DIR):
        path_to_item = join(DRAFTS_DIR, item)
        if isfile(path_to_item):
            try:
                basename, ext = item.split('.')
            except ValueError:
                pass
            else:
                if ext in DRAFTS_EXTENSIONS:
                    f = open(path_to_item, "r")
                    contents = f.read()
                    f.close()
                    drafts.append(contents)
    return drafts


def process_markdown(draft):
    """
    Processes draft contents and returns a dictionary with entry data and a list of dictionaries with tag data
    """
    md = markdown.Markdown(extensions=['meta', CodeHiliteExtension(), 'fenced_code'])
    html = md.convert(draft)
    title = md.Meta.get("title")[0]
    hidden = md.Meta.get("hidden", ["false"])[0]
    
    if hidden.lower() == 'true':
        print(f"Skipping hidden post '{title}'")
        return None  
    elif hidden.lower() == 'false':
        pass
    else:
        raise Exception("'hidden' should be 'true' or 'false', not '{published}' ({title})")
    
    title = md.Meta.get("title")[0]
    slug = slugify(title)

    tags = []
    for tag_name in md.Meta.get("tags", []):
        tag_slug = slugify(tag_name)
        tag = {
            "name": tag_name,
            "slug": tag_slug,
            "url": f"{TAGS_LOCATION}/{tag_slug}.html"
        }
        tags.append(tag)

    entry = dict(
        html=html,
        title=title,
        slug=slugify(title),
        url=f"{ENTRIES_LOCATION}/{slug}.html",
        description=md.Meta.get("description", [""])[0],
        date=datetime.strptime(md.Meta.get("date")[0], DRAFTS_DATE_FORMAT),
        tags=tags
    )
    return entry


def process_drafts(drafts):
    """
    Processes a list of draft strings (in Markdown)
    Adds tag count and a reference to a list of entries for each tag
    """
    entries = []
    tags = []
    tag_occurrences = []
    entries_with_tag = defaultdict(list)

    for draft in drafts:
        entry = process_markdown(draft)
        if entry is None:
            continue

        entries.append(entry)
        for entry_tag in entry.get('tags'):
            entry_ref = {
                "title": entry["title"],
                "url": entry["url"],
                "date": entry["date"]
            }

            entries_with_tag[entry_tag["slug"]].append(entry_ref)
            if not entry_tag["slug"] in tag_occurrences:
                tags.append(entry_tag)
            tag_occurrences.append(entry_tag["slug"])

    for tag in tags:
        tag["count"] = tag_occurrences.count(tag["slug"])
        tag["entries"] = entries_with_tag[tag["slug"]]
    entries = sorted(entries, key=lambda e: e['date'], reverse=True)

    return entries, tags


def write(path, content):
    f = open(path, "w")
    f.write(content)
    f.close()


def build_entry_detail_pages(env, entries):
    entry_detail_tpl = env.get_template("entry-detail.html")
    urls = []
    if not os.path.exists(ENTRIES_DIR):
        os.mkdir(ENTRIES_DIR)
    for entry in entries:
        entry_html = entry_detail_tpl.render(entry=entry)
        path = join(ENTRIES_DIR, f"{entry['slug']}.html")
        urls.append(build_sitemap_url(path, lastmod=entry['date']))
        write(path, entry_html)
    return urls


def build_entry_list_pages(env, entries):
    urls = []
    entry_list_tpl = env.get_template("entry-list.html")
    p = Paginator(ENTRIES_PER_PAGE, page_name="index")
    for batch in p.paginate(entries):
        entry_list_html = entry_list_tpl.render(entries=batch, paginator=p, page_name="index")
        filename = "index.html"
        if p.page_num > 1:
            filename = f"index{p.page_num}.html"
        path = join(INDEX_DIR, filename)
        urls.append(build_sitemap_url(path, lastmod=env.globals['last_updated']))
        write(path, entry_list_html)
    return urls


def build_tag_detail_pages(env, tags):
    urls = []
    if not os.path.exists(TAGS_DIR):
        os.mkdir(TAGS_DIR)
    tag_detail_tpl = env.get_template("tag-detail.html")
    for tag in tags:
        tag_detail_html = tag_detail_tpl.render(tag=tag)
        path = join(TAGS_DIR, f"{tag['slug']}.html")
        urls.append(build_sitemap_url(path, lastmod=env.globals['last_updated']))
        write(path, tag_detail_html)
    return urls


def build_tag_list_pages(env, tags):
    urls = []
    tag_list_tpl = env.get_template("tag-list.html")
    tag_list_html = tag_list_tpl.render(tags=tags)
    path = join(TAGS_DIR, "index.html")
    urls.append(build_sitemap_url(path, lastmod=env.globals['last_updated']))
    write(path, tag_list_html)
    return urls


def build_search_results_page(env):
    search_tpl = env.get_template("search.html")
    search_html = search_tpl.render()
    path = join(INDEX_DIR, "search.html")
    write(path, search_html)


def build_error_pages(env):
    errors = ((404, "Page not found"),
              (500, "Sever error"), (403, "Forbidden"))
    error_tpl = env.get_template("error.html")
    for code, message in errors:
        error_html = error_tpl.render(code=code, message=message)
        path = join(INDEX_DIR, "{}.html".format(code))
        write(path, error_html)


def build_sitemap(env, sitemap_urls):
    sitemap_tpl = env.get_template("sitemap.xml")
    sitemap_xml = sitemap_tpl.render(urls=sitemap_urls)
    path = join(INDEX_DIR, "sitemap.xml")
    write(path, sitemap_xml)


def build_rss_feed(env, entries):
    feed_tpl = env.get_template("feed.xml")
    feed_xml = feed_tpl.render(entries=entries)
    path = join(INDEX_DIR, "feed.xml")
    write(path, feed_xml)


def build_search_db(entries):
    search = []
    for index, entry in enumerate(entries):
        item = {
            "id": index,
            "title": entry['title'],
            "date": entry['date'].strftime(PUBLISHED_DATE_FORMAT),
            "content": remove_tags(entry['html']),
            "url": entry['url']
        }
        search.append(item)
    search_json = json.dumps(search)
    path = join(INDEX_DIR, "search.json")
    write(path, search_json)


def build_webmanifest():
    webmanifest = {
        "name": SITE_NAME,
        "short_name": SITE_NAME,
        "start_url": "/",
        "description": SITE_DESCRIPTION,
        "icons": [{
            "src": "icon.png",
            "sizes": "192x192",
            "type": "image/png"
        }]
    }
    webmanifest_json = json.dumps(webmanifest, indent=4)
    path = join(INDEX_DIR, "site.webmanifest")
    write(path, webmanifest_json)


def build_all():
    sitemap_urls = []

    drafts = load_drafts()
    entries, tags = process_drafts(drafts)

    last_updated = entries[0]['date'] if entries else datetime.today()
    env = get_env()
    env.globals['last_updated'] = last_updated

    sitemap_urls += build_entry_detail_pages(env, entries)
    sitemap_urls += build_entry_list_pages(env, entries)
    sitemap_urls += build_tag_detail_pages(env, tags)
    sitemap_urls += build_tag_list_pages(env, tags)
    build_error_pages(env)
    build_search_results_page(env)
    build_sitemap(env, sitemap_urls)
    build_rss_feed(env, entries)
    build_search_db(entries)
    build_webmanifest()
