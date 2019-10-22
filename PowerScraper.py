from time import sleep
from bs4 import BeautifulSoup
import os,sys,json
import WebHandler
import logging

original_directory = os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))

logging.basicConfig(filename='ps.log',filemode='a',format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)

options_file = open('options.json','r')
options_json = json.load(options_file)
options_file.close()

##################### LOAD OPTIONS ########################
available_args = (
    'username',
    'password',
    'get_individual_assignments',
    'get_old_html',
    'font'
    )
default_values = {
    'username':'',
    'password':'',
    'get_individual_assignments':True,
    'get_old_html':False,
    'font':'Cambria'
    }
options = {}
for arg in available_args:
    options[arg] = options_json.get(arg,default_values[arg])
###########################################################

if len(sys.argv) == 3:
    options['username'] = sys.argv[1]
    options['password'] = sys.argv[2]
elif options['username'] == '':
    options['username'] = input("Enter username\n>")
    options['password'] = input("Enter password (this is plaintext so be careful)\n>")

logging.info("Starting scrape for user {}".format(options['username']))
succ = WebHandler.getPowerSchool(options)
os.chdir(original_directory)
logging.info("Success!" if succ == 0 else "Failed")
sys.exit()