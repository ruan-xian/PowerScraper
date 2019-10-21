from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from bs4 import BeautifulSoup
import os,sys,json
import IndividualAssignments

option = webdriver.ChromeOptions()
option.add_argument('--incognito')
option.add_argument('--headless')
option.add_argument("--disable-dev-shm-usage")

original_directory = os.getcwd()
os.chdir(os.path.dirname(sys.argv[0]))

options_file = open('options.json','r')
options_json = json.load(options_file)
options_file.close()

##################### LOAD OPTIONS ########################
available_args = ('username','password','get_individual_assignments')
default_values = {'username':'','password':'','get_individual_assignments':False}
options = {}
for arg in available_args:
    options[arg] = options_json.get(arg,default_values[arg])
###########################################################

browser = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=option)

try:
    browser.get("https://ps01.bergen.org/public/")
except:
    print("Something went wrong while opening PowerSchool. Maybe it's down, or your connection is poor?")
    browser.close()
    browser.quit()
    os.chdir(original_directory)
    sys.exit(-1)

if len(sys.argv) == 3:
    username = sys.argv[1]
    password = sys.argv[2]
elif options['username'] != '':
    username = options['username']
    password = options['password']
else:
    username = input("Enter username\n>")
    password = input("Enter password (this is plaintext so be careful)\n>")

browser.find_element_by_id('fieldAccount').send_keys(username)
browser.find_element_by_id('fieldPassword').send_keys(password)
browser.find_element_by_id('btn-enter').click()
try:
    browser.find_element_by_id('btn-gradesAttendance').click()
except:
    print("Powerschool is closed or your login failed.")
    browser.close()
    browser.quit()
    os.chdir(original_directory)
    sys.exit()
content = str(browser.page_source)

if not os.path.exists("./output"):
    os.mkdir("./output")

f = open("./output/home.html","w+")
f.write(content)
f.close()



soup = BeautifulSoup(content,'html.parser')
possible_statuses = ('.','-','AU','AE','TE','TU','T','HU','HE','AR','ER',
    'MP','MA','FT','CV','CT','DT','STC','SD','ISS','OSS','CAE')

f = open("./output/test_overview.html","w+")

ct = 0
last_class = ""
f.write("Overview for " + username + "\n")
done = False
for link in soup.find_all('a'):
    if link.get('href').startswith("scores.html"):
        ct += 1
        gen = link.parent.parent.stripped_strings # if it ain't broke don't fix it
        next(gen)
        s = next(gen)
        while s in possible_statuses:
            s = next(gen)
        if s != last_class:
            ct = 1
            last_class = s
            if s.startswith('~Lunch') or s.startswith('~Homeroom'):
                continue
            f.write("\n" + s + "\n")
        if s.startswith('~Lunch') or s.startswith('~Homeroom'):
            continue
        if (link.string is None): # this means there is a grade for the tri
            grades = link.stripped_strings
            f.write("  T" + str(ct) + "\t" + next(grades) + "\t" + next(grades) + "\n")
            browser.get('https://ps01.bergen.org/guardian/'+link.get('href'))
            retry_count = 0
            got_grades_successfully = False
            while (True):
                try:
                    browser.find_element_by_id("scoreTable")
                    got_grades_successfully = True
                    break
                except NoSuchElementException:
                    if (retry_count >= 20):
                        break
                    sleep(0.5)
                    retry_count += 1
            if not got_grades_successfully:
                print("Failed to get assignments for " + last_class)
            else:
                IndividualAssignments.handle_class_page(str(browser.page_source),last_class,ct)

f.close()

browser.close()
browser.quit()
os.chdir(original_directory)
print("Success!")
sys.exit()