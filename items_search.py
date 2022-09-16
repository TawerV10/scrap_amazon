from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import csv

with open('output.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([
        'Title', 'Price', 'Link', 'Image'
    ])

try:
    options = webdriver.ChromeOptions()

    options.add_argument('--disable-blink-features=AutomationControlled')
    options.binary_location = 'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'

    driver = webdriver.Chrome(options=options)

    driver.get('https://www.amazon.com')
    sleep(10)

    count = 1
    for i in range(1, 4):
        url = f'https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cp_n_date%3A1249034011&dc&fs=true&page={i}&qid=1663162004&ref=sr_pg_{i}'

        driver.get(url)
        sleep(5)

        soup = BeautifulSoup(driver.page_source, 'lxml')

        items = soup.find_all('div', class_='a-section a-spacing-base')
        for item in items:
            title = item.find('span', class_='a-size-base-plus a-color-base a-text-normal').text
            link = 'https://www.amazon.com' + item.find('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal').get('href')
            image = item.find('img', class_='s-image').get('src')
            try:
                price = item.find('span', class_='a-offscreen').text
            except:
                price = None

            with open('output.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    title, price, link, image
                ])

            print(f'{count}. {title}')
            count += 1

except Exception as ex:
    print(ex)
finally:
    driver.stop_client()
    driver.close()
    driver.quit()