# pip install beautifulsoup4
import re

from bs4 import BeautifulSoup



# pip install beautifulsoup4
# pip install lxml

# for reading from web:
import urllib.request

# if cached file exists:
from pathlib import Path
my_file = Path("cached.html")
if my_file.is_file():
    print('open file "cached.html"')
    with open('cached.html', mode='r', encoding='utf-8') as f:
        src = f.read()

else:
    # if web page:
    print('open web')
    fp = urllib.request.urlopen("http://www.malchevskiy.ru/computer.html")
    mybytes = fp.read()
    src = mybytes.decode("utf8")
    fp.close()
    print(src)
    print('writing to file')
    with open('cached.html', mode='w', encoding='utf-8') as f:
        f.writelines(src)


    # print(src)


"""
# if existing html file:
with open('c://user/index.html', mode = 'r') as file:
    src = file.read()
"""



soup =BeautifulSoup(src, 'lxml')   # lxml - parser need to install
# pip install lxml

# title

title = soup.title
print (title)
title1 = soup.title.text
print (title1)
title2 = soup.title.string
print (title2)

# find() findall()
page_h2 = soup.find('h2')  # first element <h1 class="a11y-hidden" tabindex="-1">Все сервисы</h1>
print(page_h2)

page_all_h2 = soup.find_all('h2')  # all elements in list
print(page_all_h2)

for item in page_all_h2:
    print(item.text)

"""
<div class='user__name'>
    <span> Mr Andersson </span>
</div>
"""

user__name = soup.find("div", class_='user__name')
print(user__name)   # ->   <span> Mr Andersson </span>
print(user__name.text.strip())   # ->   Mr Andersson

user__name = soup.find("div", class_='user__name').find("span").text
print(user__name)
user__name = soup.find("div", {"class": 'user__name'}).find("span").text   # with dict
print(user__name)

# find_all_text

find_all_spans = soup.find(class_='user__info').find_all('span')  # -> list
print(find_all_spans)

for item in find_all_spans:
    print(item.text)

print(find_all_spans[1])
print(find_all_spans[2].text)

# links to social networks:
social_links = soup.find(class_="social__networks").find('ul').find_all('a')
print(f'social_links: {social_links}')
"""
[
<a href="http://instagram.com/username">Instagram</a>, 
<a href="http://twitter.com/username">Twitter</a>, 
<a href="http://youtube.com/username">Youtube</a>
]
"""



for item in social_links:
    print(f'social_links: {item.text}')
# social_links: Instagram
# social_links: Twitter
# social_links: Youtube

for item in social_links:
    # print(re.search(r'"(.*?)"', str(item)))
    print(re.findall(r'"(.*?)"', str(item))[0])
"""
http://instagram.com/username
http://twitter.com/username
http://youtube.com/username
"""

all_links = soup.find_all("a")
print(all_links)
"""
[<a href="http://instagram.com/username">Instagram</a>, 
<a href="http://twitter.com/username">Twitter</a>, 
<a href="http://youtube.com/username">Youtube</a>]
"""

for item in all_links:              # <a href="http://instagram.com/username">Instagram</a>,
    item_url = item.get("href")     #->  http://instagram.com/username
    print(item_url)
    item_text = item.text           # -> Instagram
    print(item_text)

# find_parent()   find_parents()

post_div = soup.find(class_ = "post__text").find_parent()
print(post_div)
"""
output: 
<div class="user__post__info">
<div class="post__title">
<h3>Российская нейросеть сортирует пластик с точностью 95%</h3>
</div>
<div class="post__text">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
                    et dolore magna aliqua. Vitae justo eget magna fermentum iaculis eu. Nibh sit amet commodo nulla
                    facilisi nullam vehicula ipsum. Elit pellentesque habitant morbi tristique senectus et netus et
                    malesuada.
                </div>
</div>
"""


post_div = soup.find(class_ = "post__text").find_parent("div", "user__post")
print(post_div)
"""
<div class="user__post">
<div class="user__post__info">
<div class="post__title">
<h3>Российская нейросеть сортирует пластик с точностью 95%</h3>
</div>
<div class="post__text">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
                    et dolore magna aliqua. Vitae justo eget magna fermentum iaculis eu. Nibh sit amet commodo nulla
                    facilisi nullam vehicula ipsum. Elit pellentesque habitant morbi tristique senectus et netus et
                    malesuada.
                </div>
</div>
</div>

Process finished with exit code 0
"""
print('\n****************  FIND PARENTS ***************\n')
post_divs = soup.find(class_ = "post__text").find_parents()
print(post_divs)

# .next_element()   .previous_element()

print('\n****************  NEXT ELEMENT ***************\n')
next_el = soup.find(class_="post__title").next_element      # here will be <CR>
next_el = soup.find(class_="post__title").next_element.next_element.text    # Российская нейросеть сортирует пластик с точностью 95%
print(next_el)

find_next_el = soup.find(class_="post__title").find_next().text               # Российская нейросеть сортирует пластик с точностью 95%
print(next_el)

print('\n****************  FIND_NEXT_SIBLING() .FIND_PREVIOUS_SIBLING()  ***************\n')

# returns next element inside the tag

find_next_sib = soup.find(class_="post__title").find_next_sibling()               # find prev div inside same parent (brother-div)
print(find_next_sib)

"""
<div class="post__text">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore
                    et dolore magna aliqua. Vitae justo eget magna fermentum iaculis eu. Nibh sit amet commodo nulla
                    facilisi nullam vehicula ipsum. Elit pellentesque habitant morbi tristique senectus et netus et
                    malesuada.
                </div>
"""

find_next_sib = soup.find(class_="post__text").find_previous_sibling()               # find next div inside same parent
print(find_next_sib)
"""
<div class="post__title">
<h3>Российская нейросеть сортирует пластик с точностью 95%</h3>
</div>
"""

links_all = soup.find(class_="some__links").find_all("a")
print(links_all)

"""
<div class = "some__links>
<a href='/clothes/' data-attr='777'>Wear for adults</a>
</div>
"""
"""
[<a data-attr="shop_link" href="/supermarket/">Магазин</a>, <a data-attr="777" href="/clothes/">Одежда для взрослых</a>]
"""

for link in links_all:
    link_href = link.get('href')        #  > /supermarket/
    link_href1 = link["href"]           #  > /supermarket/
    link_data = link.get('data-attr')   #  > shop_link
    link_data1 = link["data-attr"]      #  > shop_link

    print(link_href)
    print(link_href1)
    print(link_data)
    print(link_data1)

#поиск по части текста не работает

# <a data-attr="777" href="/clothes/">Одежда для взрослых</a>
find_a_by_text1 = soup.find("a", text="Одежда")  # doesn't work
find_a_by_text2 = soup.find("a", text="Одежда для взрослых")  # this work
find_a_by_text3 = soup.find("a", text=re.compile("Одежда"))  # this work - looking in links

find_by_text4 = soup.find_all(text=re.compile("([Оо]дежда)"))  # this work - looking in site: Одежда and одежда
print(find_by_text4)

