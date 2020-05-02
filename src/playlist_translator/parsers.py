import datetime
from typing import Dict, List

from glom import glom

APPLE_DATE_FORMAT = '%Y-%m-%d'


def parse_apple_date(date_str: str) -> datetime.date:
    dt = datetime.datetime.strptime(date_str, APPLE_DATE_FORMAT)
    return dt
