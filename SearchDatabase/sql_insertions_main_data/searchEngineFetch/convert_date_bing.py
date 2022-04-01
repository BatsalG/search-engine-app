from datetime import datetime, timedelta

def date_bing(date_):
    minute = 0
    hour = 0
    day = 0
    if date_[-1] == "m":
        minute = int(date_[:-1])
    elif date_[-1] == "h":
        hour = int(date_[:-1])
    elif date_[-1] == "d":
        day = int(date_[:-1])
    else:
        pass
    date_published = datetime.today() - timedelta(days = day, hours=hour, minutes=minute)
    date_published = date_published.strftime('%a, %d %b %Y %X')
    return date_published
