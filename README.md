# PowerScraper

## Latest Stable Build

You can download the Windows project [here](https://drive.google.com/open?id=16UMbQoXHwigCkT86fDDq_zKD8AX91jkv) -
save everything in the folder. Scroll to the bottom of the readme for version history.

## About

The purpose of this project is to set up an automatable task to download grades from PowerSchool.
Following the district choice to close access to PowerSchool outside of 6-10 PM, many have reported
*more* stress as they have to remember to check within this timeframe, and I have frequently found
that I did not remember to check a specific class. This will **NOT** allow you to see up-to-date
grades outside of 6-10 like before, but it **will** let you see your grades *from* 6-10 outside
of this time.

## Usage

Within the folder, you will find a file called options.json. This file contains all the
configuration options for the app, including (but not limited to):
    
    Username
    
    Password
    
    Whether to get individual assignments or not (significantly increases runtime)
    
    Whether to get the html of the overview site or not (looks ugly, may or may not give more info)

To change an option, simply change the value after the colon. Note that if there are quotes, you
*must* include them. Deleting an option will simply set it to a default value.

To run the app, just run PowerScraper.exe. If you specified a username and password in options.json,
the app will run automatically. Otherwise, you must somehow supply your credentials. There are two choices:
command line arguments and manual typing when prompted. 
**As of October 22nd, manual typing is no longer supported.**
If you wish to automate the app, you must either 
give credentials in the command line or in options.json. To give them in the command line:

PowerScraper.exe \<username\> \<password\>

Both of these options will run the same way.

**Results are stored in a folder called "output", located in the folder where the .exe is stored.**
Logs are stored in a file called "ps.log".

## Automation

This program is kinda pointless if you don't set up an automatic task to run it, unless you just
forget what your grades were very easily. So here's some instructions:

### Windows

1. Press the Windows button, search for "Task Scheduler" and open it.

2. On the left sidebar, click "Task Scheduler Library".

3. On the right sidebar, click "Create Basic Task".

4. Give it a name and a description, and click "Next".

5. Select "Daily", and click "Next".

6. Choose the time you want to scrape - make sure it's between 6 and 10 PM!

7. Choose "Start a Program".

8. Click browse and choose the location where PowerScraper.exe is stored.
If you did not put your username and password into options.json, put them into
the arguments, with a single space separating them.

9. Click through the rest, and you're done!
To test out your task, right-click the task in the middle menu, and click run.
To check if it worked, go to where PowerScraper.exe is stored.
**If successful, you should find your files in a folder called "output".**

### Mac

get fucked

### Linux

If you use linux you're smart enough to do this yourself

## If you're on Git and therefore don't have an .exe

I'm assuming you have python + pip, and you're on Windows, so:

Go to the command line and run:

pip install auto-py-to-exe
auto-py-to-exe

A window should open in your browser. In path to file, select PowerScraper.py.
Under "Additional Files", add options.json, chromedriver.exe, and README.md.
Under advanced, you can choose where the .exe gets outputted.
Now you can convert, and use the program as normal.

## Known Issues

If you have an elective or other one-tri class, it will always be listed as Tri 1.

I am currently trying to get Mac support - if I do, be aware that Mac releases will
always be behind Windows, since you have to make Mac apps on a Mac.

## Concerns

If you're worried about whether I'm stealing your login info or your grades, you can look at the code at 
https://github.com/ruan-xian/PowerScraper. You can then use the instructions above to compile it yourself.

## Version history

### October 22nd, 2019

- Made running completely silent
    - As a consequence, you can no longer login while the app is already running
- Added logging
- Added font options
- Beautified pages

### Before

i don't really remember