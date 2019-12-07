import datetime

def get_date(string):
        parts = string.split("-")
        return datetime.date(int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip()))
