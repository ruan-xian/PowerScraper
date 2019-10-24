import os,sys,json
import WebHandler
import logging

original_directory = os.getcwd()

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(os.path.realpath(sys.executable)))
else:
    try:
        os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
    except:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

logging.basicConfig(filename='./ps.log',filemode='a',format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)

try:
    options_file = open('options.json','r')
    options_json = json.load(options_file)
    options_file.close()
except:
    logging.error("Failed to read options.json")
    sys.exit()

##################### LOAD OPTIONS ########################
values = {
    'username':'',
    'password':'',
    'get_individual_assignments':True,
    'get_old_html':False,
    'font':'Cambria',
    'right_indent':"50%"
    }
options = {}
for arg,default_value in values.items():
    options[arg] = options_json.get(arg,default_value)
###########################################################

if len(sys.argv) == 3:
    options['username'] = sys.argv[1]
    options['password'] = sys.argv[2]
elif options['username'] == '':
    logging.error('Login credentials are required.')
    sys.exit()

logging.info("Starting scrape for user {}".format(options['username']))
succ = WebHandler.getPowerSchool(options)
os.chdir(original_directory)
logging.info("Success!" if succ == 0 else "Failed")
sys.exit()