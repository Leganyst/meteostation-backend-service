from datetime import datetime

from fastapi import HTTPException

def parse_datetime(dt_string) -> datetime | None:
    try:
        if dt_string is not None:
            return datetime.strptime(dt_string, "%d.%m.%Y, %H:%M:%S")
        return None
    except:
        raise HTTPException(status_code=400, detail="Incorrect date format, should be DD.MM.YYYY, HH:MM:SS")

def format_datetime(dt):
    return dt.strftime("%d.%m.%Y, %H:%M:%S") if dt else None
