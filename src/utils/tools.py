import datetime


def fields(*args: str) -> str:
    return ",".join(args)


def dt_format(dt: datetime.datetime) -> str:
    return dt.isoformat(timespec="seconds").replace("+00:00", "+0000")
