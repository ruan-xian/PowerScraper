# PowerScraper

By Ryan Xu, AAST 2020

## Latest Stable Build

You can download the Windows project [here](https://drive.google.com/open?id=16UMbQoXHwigCkT86fDDq_zKD8AX91jkv) -
save everything in the folder. Scroll to the bottom of the readme for version history.

By the way, if someone would be willing to work on getting a Mac port, email me at ryan-xu@live.com.

Thanks!

## About

The purpose of this project is to set up an automatable task to download grades from PowerSchool.
Following the district choice to close access to PowerSchool outside of 6-10 PM, many have reported
*more* stress as they have to remember to check within this timeframe, and I have frequently found
that I did not remember to check a specific class. This will **NOT** allow you to see up-to-date
grades outside of 6-10 like before, but it **will** let you see your grades *from* 6-10 outside
of this time.

Currently, this app is only available for Windows. It might work on Linux, but it also might not.

## Quickstart

If you really don't care about options and just want to get started:

1. Download the latest build from the link above.
2. Run EasyAutomator and follow the prompts.
3. You're done! Output will be in the folder "output", in the same directory. Logs are in ps.log. Don't expect anything to happen right away - give it til 8:30/9:30. If you *do* want to see instant results, though, say yes when prompted to try while running EasyAutomator. Don't expect anything big to happen if it's not 6-10...
4. If something goes wrong and you don't get a result within 2 minutes, check to see if there's an error message in ps.log.

## Usage

Within the folder, you will find a file called options.json. This file contains all the
configuration options for the app, including (but not limited to):
    
    Username
    
    Password
    
    Whether to get individual assignments or not (significantly increases runtime)
    
    Whether to get the html of the overview site or not (looks ugly, may or may not give more info)

To change an option, simply change the value after the colon. Note that if there are quotes, you
*must* include them. Deleting an option will simply set it to a default value.

To run the app, just run PowerScraper.exe by double-clicking it. If you specified a username and password in options.json,
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

#### New on October 24th, 2019

There is now a new application/.exe file called EasyAutomator.exe that comes in the same install folder.
Just run it by double-clicking and follow the prompts, and it'll set up an automatic PowerScraper task!

#### Old way

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

If you want the easy way: Under "Additional Files", add options.json, chromedriver.exe, and README.md.

If you want the hard way, but with cleaner output: Choose "One file", and don't add any additional files. After converting to .exe, copy over the three files listed above into the new folder.

Under advanced, you can choose where the .exe gets outputted.
Now you can convert, and use the program as normal.

To include the new automator, separately compile EasyAutomator.py.

## Known Issues

I don't have a Mac. If you have a Mac and know Python, email me.

## Concerns

If you're worried about whether I'm stealing your login info or your grades, you can look at the code at 
https://github.com/ruan-xian/PowerScraper. You can then use the instructions above to compile it yourself.

If you wish to automate the app, you will have to store your password somewhere in some way, whether it's in options.json or in the 
Task Scheduler. Know that any time you save your password in plaintext, you are decreasing your security.

## Contact

For questions and concerns, email me at ryan-xu@live.com or DM me on Instagram @ruan__xian. Update announcements will be on Instagram.

## Version history

### October 24th, 2019

- Added a new easy way to automate on Windows!
- Unfortunately, Mac support will probably not come in the near future.

### October 23rd, 2019

- New single-file exes!

### October 22nd, 2019

- Made running completely silent
    - As a consequence, you can no longer login while the app is already running
- Added logging
- Added font options
- Beautified pages
- Fixed Tri 1 issue

### Before

i don't really remember
