import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd

def page_scraper(driver, houses):
      j = 1
      while True:
            house = {}
            try: 
                element = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, f"/html/body/div[6]/div/div[2]/div[1]/a[{j}]/article/div[2]/div[1]/div[1]"
        )))
            except TimeoutException:
                print("No more elements in this page")
                break

            else:
                house['address'] = " ".join(element.text.split()[2:])
                time.sleep(1)
                initial_price = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, f"/html/body/div[6]/div/div[2]/div[1]/a[{j}]/article/div[2]/div[1]/div[2]/span[1]/span")))
                house['initial_price'] = initial_price.text[:-2]
                time.sleep(1)
                final_price = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, f"/html/body/div[6]/div/div[2]/div[1]/a[{j}]/article/div[2]/div[1]/div[2]/span[2]/span[1]")))
                house['final_price'] = final_price.text
                time.sleep(1)
                print(house)
                time.sleep(1)
                j+= 1
                houses.append(house)

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://alertasubastas.com/subastas-publicas-vivienda/madrid-madrid?filtro=puja_con,finaliza_desde-1-Mar-2025_hasta-1-Mar-2026')
    time.sleep(2)

    element = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/dialog/div/div/div[2]/div[2]/div[2]/div[2]/button"
    )))
    element.click()

    element = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div/div[2]/div[3]/span"
    )))
    n_pages = int(element.text.split()[-1])
    print(element)
    houses = []
    page_scraper(driver, houses)
    for i in range(2,n_pages+1):
        j = 2 
        try: 
            driver.get(f'https://alertasubastas.com/subastas-publicas-vivienda/madrid-madrid/pagina-{i}?filtro=puja_con,finaliza_desde-1-Mar-2025_hasta-1-Mar-2026')
        except:
            print("Page not found")
            break

        page_scraper(driver, houses)

    time.sleep(1)

    driver.close()

    df = pd.DataFrame.from_dict(houses, orient = 'columns')
    df.to_csv('houses2.csv')

    print("Scraping completed")

main()
