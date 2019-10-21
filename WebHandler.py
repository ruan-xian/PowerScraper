from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import os

def getPowerSchool(options):
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--incognito')
    chrome_option.add_argument('--headless')
    chrome_option.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=chrome_option)

    try:
        try:
            browser.get("https://ps01.bergen.org/public/")
        except:
            print("Something went wrong while opening PowerSchool. Maybe it's down, or your connection is poor?")
            browser.close()
            browser.quit()
            return -1

        browser.find_element_by_id('fieldAccount').send_keys(options['username'])
        browser.find_element_by_id('fieldPassword').send_keys(options['password'])
        browser.find_element_by_id('btn-enter').click()
        try:
            browser.find_element_by_id('btn-gradesAttendance').click()
        except:
            print("Powerschool is closed or your login failed.")
            browser.close()
            browser.quit()
            return -1
        content = str(browser.page_source)

        if not os.path.exists("./output"):
            os.mkdir("./output")

        if (options['get_old_html']):
            f = open("./output/home.html","w+")
            f.write(content)
            f.close()

        soup = BeautifulSoup(content,'html.parser')
        possible_statuses = ('.','-','AU','AE','TE','TU','T','HU','HE','AR','ER',
            'MP','MA','FT','CV','CT','DT','STC','SD','ISS','OSS','CAE')

        f = open("./output/overview.html","w+")

        ct = 0
        last_class = ""
        f.write("Overview for " + options['username'] + "\n")
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
                    if (options['get_individual_assignments']):
                        handle_class_page(browser,link.get('href'),last_class+" T"+str(ct))
        f.close()
    except:
        browser.close()
        browser.quit()
        return -1

    browser.close()
    browser.quit()
    return 0

def handle_class_page(browser,link,class_name):
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
        print("Failed to get assignments for " + class_name)
        return
    table = BeautifulSoup(str(browser.page_source),'html.parser').select('#scoreTable')[0]
    assignments = table.find_all(lambda tag : tag.name == 'span' and tag.get('class') == ['ng-binding'])
    grades = table.find_all(lambda tag : tag.name == 'span' and tag.get('class') == ['ng-binding','ng-scope'])
    last_updated = grades[len(grades)-1].string.strip()
    grades = grades[:-1]

    total_stats = zip(assignments,grades)

    f = open('./output/' + class_name + '.txt','w+')

    f.write(last_updated+"\n\n")
    for assignment,grade in total_stats:
        f.write(assignment.string.strip() + " " + grade.string.strip() + "\n")

    f.close()