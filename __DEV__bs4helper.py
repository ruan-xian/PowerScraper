from bs4 import BeautifulSoup

source = open('./output/PowerschoolScraper/PowerSchool/home.html','r')
soup = BeautifulSoup(source,'html.parser')
source.close()

out = open('soup.html','w+')
out.write(soup.prettify())
out.close()