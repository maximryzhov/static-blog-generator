import email.utils

from datetime import datetime

from src.settings import PUBLISHED_DATE_FORMAT


def date_filter(value):
    if value:
        return datetime.strftime(value, PUBLISHED_DATE_FORMAT)


def rfc822_filter(value):
    return email.utils.format_datetime(value)
