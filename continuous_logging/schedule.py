import datetime
from os import path
import win32com.client


def schedule_continuous_logging(action, often, repetition, when):
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')

    if action == "Disable":
        task = root_folder.GetTask("Continuous Logging")
        task.Enabled = False
        return

    task_def = scheduler.NewTask(0)

    if often in ["On Start Up", "Multiple Times a Day"]:
        # Create startup trigger
        TASK_TRIGGER_BOOT = 8
        startup_trigger = task_def.Triggers.Create(TASK_TRIGGER_BOOT)

    if often == "Multiple Times a Day":
        # Create hourly trigger
        TASK_TRIGGER_DAILY = 2
        hourly_trigger = task_def.Triggers.Create(TASK_TRIGGER_DAILY)
        hourly_trigger.StartBoundary = datetime.datetime.now().isoformat()
        hourly_trigger.DaysInterval = 1  # Repeat every day

    # Set repetition for hourly trigger
    if repetition == "Every Hour":
        hourly_trigger.Repetition.Interval = 'PT1H'  # Every hour
    elif repetition == "Every Two Hours":
        hourly_trigger.Repetition.Interval = 'PT2H'  # Every Two Hours
    else:
        hourly_trigger.Repetition.Interval = 'PT30M'  # 30 Minutes
    # hourly_trigger.Repetition.Duration = 'P1D'  # For a 24-hour period

    # Create action
    TASK_ACTION_EXEC = 0
    action = task_def.Actions.Create(TASK_ACTION_EXEC)
    action.ID = 'DO NOTHING'
    action.Path = path.join(path.abspath(""), 'continuous_logging/Continuous Logging.exe')

    app_path = path.join(path.abspath(""), "Time Logger.py")
    console_app_path = path.join(path.abspath(""), "Continuous Logging.exe")

    if action == 'Open Time Logger' and path.exists(app_path):
        action.Arguments = f'app "{app_path}"'
    elif action == "Open Console App" and path.exists((console_app_path)):
        action.Arguments = f'console "{console_app_path}"'
    else:
        action.Arguments = f'{console_app_path}, {app_path}'

    # Set parameters
    task_def.RegistrationInfo.Description = "Can't commit to a diary? Write one line entries."
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False

    # Register task
    # If task already exists, it will be updated
    TASK_CREATE_OR_UPDATE = 6
    TASK_LOGON_NONE = 0
    root_folder.RegisterTaskDefinition(
        'Continuous Logging',  # Task name
        task_def,
        TASK_CREATE_OR_UPDATE,
        '',  # No user
        '',  # No password
        TASK_LOGON_NONE)


schedule_continuous_logging(None, "Multiple Times a Day", None, None)
