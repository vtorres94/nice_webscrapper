from selenium.webdriver import Edge
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrapper():

    try:
        all_products = []

        driver = Edge()
        driver.get(
            "https://www.niceonline.com/corp/Products?nPage=1&nPageItems=1000"
        )

        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "item-container"))
        )

        for product in products:

            p = {
                'name': product.find_element(By.CLASS_NAME, "item-name").text or "",
                'code': product.find_element(By.CLASS_NAME, "item-code").text or "",
                'price': product.find_element(By.CLASS_NAME, "item-price").text or "",
                'image': product.find_element(
                    By.TAG_NAME, "img").get_attribute('src') or ""
            }

            if p.get('code') not in [p.get('code') for p in all_products]:

                print('Product:', p.get('code'), 'Guardado')

                all_products.append(p)

        save_products(all_products)
        save_to_csv(all_products)

    except Exception as e:
        print('Error: ', e)
        driver.quit()


def save_products(products):
    import json
    with open('products.json', 'w') as file:
        json.dump(products, file)


def save_to_csv(products):
    import csv
    with open('products.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Code', 'Price', 'Image'])
        for product in products:
            writer.writerow([product['name'], product['code'],
                            product['price'], product['image']])


scrapper()
