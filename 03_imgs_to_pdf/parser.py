import json
import os
import img2pdf

import requests
from bs4 import BeautifulSoup

HTML_FILE = "tools.html"

URL ="https://www.recordpower.co.uk/"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User - Agent": "Mozilla / 5.0(Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36(KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
}


def get_data(url):

    req = requests.get(url=URL, headers=HEADERS)
    response = req.text
    with open("tools.html", "w", encoding='utf-8') as file:
        file.write(response)


def img_2_pdf():
    img_list = os.listdir("media")      # unsorted list of imgs
    img_list =[f"media/{i}.jpg" for i in range(0, 4)]
    with open("result1.pdf", "wb") as pdf_file:
        pdf_file.write(img2pdf.convert(img_list))
    print('PDF file created successfully')


def main():
    file_check1 = os.path.exists(HTML_FILE)
    file_check2 = os.path.isfile(HTML_FILE)
    if not (file_check1 & file_check2):
        get_data(url)

    with open("tools.html", mode='r', encoding='utf-8') as f:
        src = f.read()
    soup = BeautifulSoup(src, 'lxml')

    courusel = soup.find_all("li", class_="splide__slide")
    # print(f' courusel: \n {courusel}')

    links = []
    for item in courusel:
        link = item.find("a").find("img").get("src")
        links.append(f'{URL}{link}')
    print(links)
    with open("links.lst","w", encoding='UTF-8') as file:
        json.dump(links, file, indent=4, ensure_ascii=False)

    link_count = 0
    img_list =[]
    if links:
        for link in links:
            req = requests.get(url=link, headers=HEADERS)
            response = req.content

            with open(f"media/{link_count}.jpg", "wb") as file:
                file.write(response)
                print(f'downloaded img{link_count}')
            img_list.append(f"media/{link_count}.jpg")
            link_count +=1
    print(img_list)

    # pip install img2pdf
    # create pdf file
    with open("result.pdf", "wb") as pdf_file:
        pdf_file.write(img2pdf.convert(img_list))
    print('PDF file created successfully')


if __name__ == "__main__":
    main()
    img_2_pdf()



