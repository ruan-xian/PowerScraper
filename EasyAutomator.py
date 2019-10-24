# Helps configure a task to launch PowerScraper at a specified time each day.

import win32com.client
import os
import sys

if getattr(sys, 'frozen', False):
    cur_path = os.path.dirname(os.path.realpath(sys.executable))
else:
    try:
        cur_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    except:
        cur_path = os.path.dirname(os.path.realpath(__file__))

user = input("Enter your PowerSchool username\n>")
pw = input("Enter your PowerSchool password\n>")
print("Setting up a task to run PowerScraper at 9:30 PM EST. If this time is not good for you, you may change it in Task Scheduler.")
print("Also, Daylight Savings Time is ass and it might run at 8:30 EST instead. Whatever.")

computer_name = "" #leave all blank for current computer, current user
computer_username = ""
computer_userdomain = ""
computer_password = ""
action_id = "PowerScraper easy setup" #arbitrary action ID
action_path = cur_path+r"\PowerScraper.exe" #executable path (could be python.exe)
action_arguments = user + " " + pw #arguments (could be something.py)
action_workdir = r"" #working directory for action executable
author = "Ryan Xu, AAST 2020" #so that end users know who you are
description = "Automatically runs PowerScraper at either 8:30 or 9:30 PM. Daylight savings time is ass." #so that end users can identify the task
task_id = "Automatic PowerScraper Task"
task_hidden = False #set this to True to hide the task in the interface
username = ""
password = ""
run_flags = "TASK_RUN_NO_FLAGS" #see dict below, use in combo with username/password
#define constants
TASK_TRIGGER_DAILY = 2
TASK_CREATE = 2
TASK_CREATE_OR_UPDATE = 6
TASK_ACTION_EXEC = 0
IID_ITask = "{148BD524-A2AB-11CE-B11F-00AA00530503}"
RUNFLAGSENUM = {
    "TASK_RUN_NO_FLAGS"              : 0,
    "TASK_RUN_AS_SELF"               : 1,
    "TASK_RUN_IGNORE_CONSTRAINTS"    : 2,
    "TASK_RUN_USE_SESSION_ID"        : 4,
    "TASK_RUN_USER_SID"              : 8 
}
#connect to the scheduler (Vista/Server 2008 and above only)
scheduler = win32com.client.Dispatch("Schedule.Service")
scheduler.Connect(computer_name or None, computer_username or None, computer_userdomain or None, computer_password or None)
rootFolder = scheduler.GetFolder("\\")
#(re)define the task
taskDef = scheduler.NewTask(0)
colTriggers = taskDef.Triggers
trigger = colTriggers.Create(TASK_TRIGGER_DAILY)
trigger.DaysInterval = 1
trigger.StartBoundary = "2000-01-01T01:30:00-00:00" #9:30 EST
trigger.Enabled = True
colActions = taskDef.Actions
action = colActions.Create(TASK_ACTION_EXEC)
action.ID = action_id
action.Path = action_path
action.WorkingDirectory = action_workdir
action.Arguments = action_arguments
info = taskDef.RegistrationInfo
info.Author = author
info.Description = description
settings = taskDef.Settings
settings.Enabled = True
settings.Hidden = task_hidden
#register the task (create or update, just keep the task name the same)
result = rootFolder.RegisterTaskDefinition(task_id, taskDef, TASK_CREATE_OR_UPDATE, "", "", RUNFLAGSENUM[run_flags] ) #username, password
run_test = input("Success! Would you like to run the task once to test it? [Y/N]\n>")
#run the task once
if run_test.startswith('y'):
    print("Running task")
    task = rootFolder.GetTask(task_id)
    runningTask = task.Run("")
    print("Task finished. Check your install folder for output files/logs.")