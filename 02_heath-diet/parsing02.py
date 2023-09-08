import csv
import os.path
import random
from time import sleep

import requests
from bs4 import BeautifulSoup
import json

HTML_FILE = "index.html"
ALL_CATEG_JSON_FILE = "all_categ_dict.json"
HEADERS = {
    "Accept": "*/*",
    "User-Agent":
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
}

url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"

index_check1 = os.path.exists(HTML_FILE)
index_check2 = os.path.isfile(HTML_FILE)

if not (index_check1 & index_check2):
    headers ={
    "Accept":  "*/*",
    "User-Agent":
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
    }
    req = requests.get(url, headers=HEADERS)

    src = req.text
    # print(src)

    with open('index.html', mode = 'w', encoding='utf-8') as f:
        f.write(src)


with open("index.html", mode='r', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src,'lxml')

# 1, get all links, they are under same div


index_check3 = os.path.exists(ALL_CATEG_JSON_FILE)
index_check4 = os.path.isfile(ALL_CATEG_JSON_FILE)

if not (index_check3 & index_check4):
    all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")
    all_categories = {}
    for item in all_products_hrefs:
        # print(item)
        item_text = item.text
        item_href = f'https://health-diet.ru{item.get("href")}'
        # print(f'{item_text}  {item_href}')
        all_categories[item_text] = item_href
    with open('all_categ_dict.json', mode="w", encoding ='utf-8') as file:
        json.dump(all_categories, file, indent=4, ensure_ascii=False)
else:
    with open(ALL_CATEG_JSON_FILE, mode='r', encoding='utf-8') as file:
        all_categories = json.load(file)

# print(f'all categories: \n {all_categories}')

iteration_count = int(len(all_categories))-1
print(f'total iterations: {iteration_count}')
count = 0
for category_name, category_href in all_categories.items():


    # if count == 0:
    rep =[",", " ", "-", "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")
    # print(category_name)
    req = requests.get(url=category_href, headers=HEADERS)
    src = req.text

    with open(f"html_data/{count}_{category_name}.html", mode="w", encoding='utf-8') as f:
        f.write(src)


    # with open(f"html_data/{count}_{category_name}.html", mode="r", encoding='utf-8') as f:
    #     src=f.read()

    soup = BeautifulSoup(src,"lxml")

    # check page it data table exists:

    alert_block = soup.find(class_="uk-alert-danger")
    if alert_block is not None:
        continue

    # ******************* looking for table headers: *****************
    table_headers = soup.find(class_="mzr-tc-group-table").find("tr").find_all("th")
    # print(f'table_headers: {table_headers}')
    product = table_headers[0].text
    calories = table_headers[1].text
    proteins = table_headers[2].text
    fats = table_headers[3].text
    carbohydrates = table_headers[4].text
    with open(f"html_data/{count}_{category_name}.csv", mode="w", encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # writer.writerow(['sep=,'])
        writer.writerow(
            [
                "product",
                "calories",
                "proteins",
                "fats",
                "carbohydrates"
            ]
        )
        # collect food data
        products_data = soup.find(class_="mzr-tc-group-table").find("tbody").find_all("tr")
        product_info=[]

        for item in products_data:
            product_tds = item.find_all("td")
            # print(f'product_tds: {product_tds}')
            product = product_tds[0].find("a").text
            calories = product_tds[1].text
            proteins = product_tds[2].text
            fats = product_tds[3].text
            carbohydrates = product_tds[4].text
            # print (f'product: {product}')
            # print (f'proteins: {proteins}')

            product_info.append(
                {
                    "product": product,
                    "calories": calories,
                    "proteins": proteins,
                    "fats": fats,
                    "carbohydrates": carbohydrates
                }
            )
            with open(f"html_data/{count}_{category_name}.csv", mode="a", encoding='utf-8', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(
                        [
                            product,
                            calories,
                            proteins,
                            fats,
                            carbohydrates
                        ]
                    )
    with open(f"html_data/{count}_{category_name}.json", mode="a", encoding='utf-8') as json_file:
            json.dump(product_info, json_file, indent=4, ensure_ascii=False)

    count +=1
    print(f'# Iteration: {count}  {category_name} has been written')
    iteration_count = iteration_count -1
    if iteration_count == 0:
        print('writing done')
        break

    print (f'left {iteration_count} iterations')
    # sleep(random.randrange(1, 2))















