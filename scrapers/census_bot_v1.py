import threading

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import os

from selenium.webdriver.common.action_chains import ActionChains

def get_district_data(link:str, district_id:str):
    path = f"{district_id}"

    # Create folder
    if not os.path.exists(district_id):
        os.mkdir(district_id)

    # Open website
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(link)
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior",
        {
            "behavior": "allow",
            "downloadPath": path
        }
    )
    
    select = Select(driver.find_element(By.ID, 'DropDownList_Listado_Territorios'))
    select.select_by_value(district_id)

    # Iterate through all graphs
    graph_ids = [(8,1),(12,1),(19,1),(26,1),(26,1),(33,1),(40,1),(47,1),(54,1),(61,1),(73,1),(73,2),(77,1),(88,1),(88,2),(95,1),(105,1),(105,2),(112,1),(122,1),(122,2),(129,1),(138,1)]
    special_ids = [69, 98, 115]

    for id in graph_ids:
        trigger_xpath = f"/html/body/form/section/div[1]/table/tbody/tr[{id[0]}]/td[{id[1]}]/div[2]/div[1]/img"
        option_xpath  = f"/html/body/form/section/div[1]/table/tbody/tr[{id[0]}]/td[{id[1]}]/div[2]/div[1]/div/ul/a[3]"

        # 1) Hover the trigger (hover-based menu needs this)
        trigger = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, trigger_xpath)))
        ActionChains(driver).move_to_element(trigger).pause(0.2).perform()

        # 2) Wait until the option is visible (not just present)
        option = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, option_xpath)))

        option.click()

    for id in special_ids:
        trigger_xpath = f"/html/body/form/section/div[1]/table/tbody/tr[{id}]/td/div[2]/div[1]/img"
        option_xpath  = f"/html/body/form/section/div[1]/table/tbody/tr[{id}]/td/div[2]/div[1]/div/ul/a[3]"

        # 1) Hover the trigger (hover-based menu needs this)
        trigger = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, trigger_xpath)))
        ActionChains(driver).move_to_element(trigger).pause(0.2).perform()

        # 2) Wait until the option is visible (not just present)
        option = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, option_xpath)))

        option.click()


def main():
    if not os.path.exists("census_data"):
        os.mkdir("census_data")
    os.chdir("census_data")

    link = "http://portalestadistico.com/municipioencifras/?pn=madrid&pc=ztv21&idp=35&idpl=1329&idioma="
    threads = []

    for i in range(1,22):
        end = str(i) if i>9 else f"0{i}"
        district_id = "28079DIS" + end
        t = threading.Thread(target=get_district_data, args=(link, district_id))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

main()
