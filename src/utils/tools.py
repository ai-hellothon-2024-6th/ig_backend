import datetime
from datetime import timedelta


def fields(*args: str) -> str:
    return ",".join(args)


def utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def dt_format(dt: datetime.datetime) -> str:
    return dt.isoformat(timespec="seconds").replace("+00:00", "+0000")
