from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import os
import lxml
import logging
import re

def getPowerSchool(options):
    #logging.basicConfig(filename='ps.log',filemode='a',format='%(asctime)s - %(message)s',level=logging.INFO)

    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--incognito')
    chrome_option.add_argument('--headless')
    chrome_option.add_argument("--disable-dev-shm-usage")
    chrome_option.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_option)

    try:
        browser.get("https://ps01.bergen.org/public/")
        browser.find_element_by_id('fieldAccount').send_keys(options['username'])
        browser.find_element_by_id('fieldPassword').send_keys(options['password'])
        browser.find_element_by_id('btn-enter').click()
    except:
        logging.error("Something went wrong while opening PowerSchool. Maybe it's down, or your connection is poor?")
        browser.close()
        browser.quit()
        return -1
    try:
        browser.find_element_by_id('btn-gradesAttendance').click()
    except:
        logging.error("Powerschool is closed or your login failed.")
        browser.close()
        browser.quit()
        return -1
    content = str(browser.page_source)

    if not os.path.exists("./output"):
        os.mkdir("./output")
    if not os.path.exists("./output/CSS"):
        os.mkdir("./output/CSS")

    if (options['get_old_html']):
        f = open("./output/home.html","w+")
        f.write(content)
        f.close()

    generateCSS(options)

    soup = BeautifulSoup(content,'html.parser')
    possible_statuses = ('.','-','AU','AE','TE','TU','T','HU','HE','AR','ER',
        'MP','MA','FT','CV','CT','DT','STC','SD','ISS','OSS','CAE')

    f = open("./output/overview.html","w+")
    f.write("<head><title>Overview</title>")
    f.write('<link rel="stylesheet" href="CSS/main.css">')

    f.write("<body>")

    last_class = ""
    f.write("<h1>")
    f.write("Overview for " + options['username'] + "\n")
    f.write("</h1>")
    for link in soup.find_all('a'):
        if link.get('href').startswith("scores.html"):
            gen = link.parent.parent.stripped_strings # if it ain't broke don't fix it
            next(gen)
            s = next(gen)
            while s in possible_statuses: # clear out the attendance stats. May implement some attendance tracking later.
                s = next(gen)
            if s != last_class:
                last_class = s
                if s.startswith('~Lunch') or s.startswith('~Homeroom'):
                    continue
                f.write("<h3>")
                f.write(s + "\n")
                f.write("</h3>")
            if s.startswith('~Lunch') or s.startswith('~Homeroom'):
                continue
            if (link.string is None): # this means there is a grade for the tri
                assignments_retrieved = -1
                grades = link.stripped_strings
                letter_grade = next(grades)
                number_grade = next(grades)
                tri = re.search(r'fg=T\d',link.get('href')).group(0)[3:]
                if (options['get_individual_assignments']):
                    assignments_retrieved = handleClassPage(browser,link.get('href'),last_class+" "+tri,number_grade)
                if assignments_retrieved == 0:
                    f.write('<a href="')
                    f.write(last_class+" "+tri +'.html')
                    f.write(r'" class="tab">')
                else:
                    f.write(r'<p class="tab">')
                f.write("  " + tri + " " + number_grade + " " + letter_grade + "\n")
                if assignments_retrieved == 0:
                    f.write('</a>')
                else:
                    f.write(r'</p>')
                f.write('<br>')
    f.write("</body>")
    f.close()

    browser.close()
    browser.quit()
    return 0

def handleClassPage(browser,link,class_name,average=None):
    browser.get('https://ps01.bergen.org/guardian/'+link)
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
        logging.warning("Failed to get assignments for " + class_name)
        return -1
    table = BeautifulSoup(str(browser.page_source),'html.parser').select('#scoreTable')[0]
    assignments = table.find_all(lambda tag : tag.name == 'span' and tag.get('class') == ['ng-binding'])
    grades = table.find_all(lambda tag : tag.name == 'span' and tag.get('class') == ['ng-binding','ng-scope'])
    last_updated = grades[len(grades)-1].string.strip()
    grades = grades[:-1]

    total_stats = zip(assignments,grades)

    f = open('./output/' + class_name + '.html','w+')

    f.write("<head><title>{}</title>".format(class_name))
    f.write('<link rel="stylesheet" href="CSS/main.css">')

    f.write("<body>")

    f.write('<h1>')
    f.write(class_name +"\n")
    f.write('</h1>')
    f.write('<h2>')
    f.write("Average: " + average +"\n")
    f.write('</h2>')

    f.write('<h3>')
    f.write(last_updated+"\n")
    f.write('</h3>')

    f.write('<a href="overview.html">Back to overview</a>')

    for assignment,grade in total_stats:
        f.write(r'<p style="text-align:left">')
        f.write(assignment.string.strip())
        f.write(r'<span style="float:right" class="rtab">')
        f.write(grade.string.strip())
        f.write('</span>')
        f.write('</p>')
        f.write('<hr class="rtab">')

    f.write('<a href="overview.html">Back to overview</a>')
    f.write("</body>")

    f.close()
    return 0

def generateCSS(options):
    f = open("./output/CSS/main.css","w+")

    f.write("body { font-family: " + options['font'] + " }\n")

    f.write(r".tab { margin-left: 2%; }")
    f.write(r".rtab { margin-right: " + options['right_indent'] + r"; }")

    f.close()
    return