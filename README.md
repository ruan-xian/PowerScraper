# PowerScraper

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
*must* include them. Deleting an option will simply sit it to a default value.

To run the app, just run PowerScraper.exe. If you specified a username and password in options.json,
the app will run automatically. Otherwise, you must somehow supply your credentials. There are two choices:
command line arguments and manual typing when prompted. If you wish to automate the app, you must either 
give credentials in the command line or in options.json. To give them in the command line:

PowerScraper.exe \<username\> \<password\>

All of these will run the same way.

