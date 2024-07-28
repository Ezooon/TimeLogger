import os
import sys


def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # If _MEIPASS does not exist, we are in development mode or a directory bundle
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def am_pm(t):
    hh = t.hour if t.hour <= 12 else t.hour - 12
    hh = 12 if t.hour == 0 else hh
    c = "am" if t.hour < 12 else "pm"
    mm = t.minute if t.minute > 9 else "0" + str(t.minute)
    return f"{'' if hh > 9 else 0}{hh}:{mm} {c}"


def dtstr(dt):
    return f'{dt.date()} {am_pm(dt)}'
