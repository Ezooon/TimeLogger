from winotify import Notification, audio


def notify():
    notification = Notification(
        app_id="TimeLogger",
        title="What's new?",
        msg="Don't let your live pass you by",
        duration="long",
        icon=r"E:\Workspace\projects\TimeLogger\assets\logo.png",
        launch=r"E:\Workspace\projects\TimeLogger\new_log.py",
    )
    notification.set_audio(audio.Default, loop=True)
    notification.add_actions(label="Console", launch=r"E:\Workspace\projects\TimeLogger\new_log.py")
    notification.add_actions(label="Time Logger", launch=r"E:\Workspace\projects\TimeLogger\main.py")
    notification.show()


# while True:
#     print("NOW!")
notify()  # just found out that Task Scheduler allows repetition
# now I need ot find out how to config it automatically.
# its Cronjobs on Linux.
# sleep(60*60)
