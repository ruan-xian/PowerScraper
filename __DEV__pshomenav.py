from bs4 import BeautifulSoup

source = open('./output/PowerschoolScraper/PowerSchool/home.html','r')
soup = BeautifulSoup(source,'html.parser')
source.close()

possible_statuses = ('.','-','AU','AE','TE','TU','T','HU','HE',
'AR','ER','MP','MA','FT','CV','CT','DT','STC','SD','ISS','OSS','CAE')

ct = 0
last_class = ""
for link in soup.find_all('a'):
    if link.get('href').startswith("scores.html"):
        ct += 1
        gen = link.parent.parent.stripped_strings
        next(gen)
        s = next(gen)
        while s in possible_statuses:
            s = next(gen)
        if s != last_class:
            ct = 1
            last_class = s
            if s.startswith('~Lunch') or s.startswith('~Homeroom'):
                continue
            print("\n" + s)
        if s.startswith('~Lunch') or s.startswith('~Homeroom'):
            continue
        if (link.string is None):
            grades = link.stripped_strings
            print("  T" + str(ct) + "\t" + next(grades) + "\t" + next(grades))