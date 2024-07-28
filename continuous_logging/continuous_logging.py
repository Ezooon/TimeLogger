import sys
from os import system, path
from winotify import Notification, audio


def notify(console_app_path, app_path):
    print(console_app_path, app_path)
    notification = Notification(
        app_id="TimeLogger",
        title="What's new?",
        msg="Don't let your live pass you by",
        duration="long",
        icon=path.join(path.abspath(""), "logo.png"),
        launch=console_app_path,
    )
    notification.set_audio(audio.Default, loop=True)
    notification.add_actions(label="Console", launch=console_app_path)
    notification.add_actions(label="Time Logger", launch=app_path)
    notification.show()


options = sys.argv
if "console" in options:
    console_app_path = options[2] if len(options) > 2 else path.join(*path.split(path.abspath(""))[:-1], "new_log.py")
    if console_app_path.endswith('.py'):
        system(f'cmd /c "E:/Workspace/evenv10/Scripts/python.exe "{console_app_path}""')
    else:
        system(f'cmd /c ""{console_app_path}""')

elif "app" in options:
    app_path = options[2] if len(options) > 2 else path.join(*path.split(path.abspath(""))[:-1], "main.py")
    if app_path.endswith('.py'):
        system(f'cmd /c "E:/Workspace/evenv10/Scripts/python.exe "{app_path}""')
    else:
        system(f'cmd /c ""{app_path}""')

else:
    console_app_path = options[1] if len(options) > 1 else path.join(*path.split(path.abspath(""))[:-1], "concole_application.py")
    app_path = options[2] if len(options) > 2 else path.join(*path.split(path.abspath(""))[:-1], "main.py")
    notify(console_app_path, app_path)
