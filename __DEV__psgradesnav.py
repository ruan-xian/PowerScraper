from bs4 import BeautifulSoup

f = open('class_page.html','r')
individual_soup = BeautifulSoup(f,'html.parser')
f.close()

table = individual_soup.select('#scoreTable')[0]
# g = open('score_table.html','w+')
# g.write(str(table))
# g.close()
assignments = BeautifulSoup(str(table),'html.parser').find_all(lambda tag : tag.name == 'span' and tag.get('class') == ['ng-binding'])
grades = BeautifulSoup(str(table),'html.parser').find_all(lambda tag : tag.name == 'span' and tag.get('class') == ['ng-binding','ng-scope'])
last_updated = grades[-1].string.strip()
grades = grades[:-1]

total_stats = zip(assignments,grades)

for assignment,grade in total_stats:
    print(assignment.string.strip() + " " + grade.string.strip())

# for thing in BeautifulSoup(str(table),'html.parser').select(".ng-binding"):
#     print(thing.get('class'))