def am_pm(t):
    hh = t.hour if t.hour <= 12 else t.hour - 12
    hh = 12 if t.hour == 0 else hh
    c = "am" if t.hour < 12 else "pm"
    mm = t.minute if t.minute > 9 else "0" + str(t.minute)
    return f"{'' if hh > 9 else 0}{hh}:{mm} {c}"


def dtstr(dt):
    return f'{dt.date()} {am_pm(dt)}'
