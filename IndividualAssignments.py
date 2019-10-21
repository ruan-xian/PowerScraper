from bs4 import BeautifulSoup

def handle_class_page(page_source,class_name,tri):
    table = BeautifulSoup(page_source,'html.parser').select('#scoreTable')[0]
    assignments = table.find_all(lambda tag : tag.name == 'span' and tag.get('class') == ['ng-binding'])
    grades = table.find_all(lambda tag : tag.name == 'span' and tag.get('class') == ['ng-binding','ng-scope'])
    last_updated = grades[len(grades)-1].string.strip()
    grades = grades[:-1]

    total_stats = zip(assignments,grades)

    f = open('./output/' + class_name +' T'+str(tri) + '.txt','w+')

    f.write(last_updated+"\n\n")
    for assignment,grade in total_stats:
        f.write(assignment.string.strip() + " " + grade.string.strip() + "\n")

    f.close()