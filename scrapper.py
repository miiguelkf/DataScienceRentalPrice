from selenium import webdriver
import time
import numpy as np
import pandas as pd

def get_data(driver):

    try:
        title = driver.find_element_by_xpath("//h1[@class='sc-1q9n36n-0 ghXeyc sc-bdVaJa hgGleC']").text
        address = driver.find_element_by_xpath("//p[@data-testid='listing-address-subtitle']").text
    except:
        title = address = np.nan

    #General Infos
    try:
        infos = driver.find_elements_by_xpath("//div[@class='MuiGrid-root tptht-0 fAvqys MuiGrid-item MuiGrid-grid-xs-3 MuiGrid-grid-sm-3 MuiGrid-grid-md-1']")
        area = infos[0].text
        bedroom = infos[1].text
        bathroom = infos[2].text
        garage = infos[3].text
        floor = infos[4].text
        pet = infos[5].text
        furniture = infos[6].text
        subway = infos[7].text
    except:
        area = bedroom = bathroom = garage = floor = pet = furniture = subway = np.nan

    #Price Infos
    infos = driver.find_elements_by_xpath("//li[contains(@class, 'MuiListItem-root rf1epz-0')]")
    for info in infos:
        if 'Aluguel' in info.text: rent = info.text
        elif 'Condomínio' in info.text: condominium = info.text
        elif 'IPTU' in info.text: taxes = info.text
        elif 'Seguro incêndio' in info.text: fire_insurance = info.text
        elif 'Taxa de serviço' in info.text: services = info.text
        elif 'Total' in info.text: total = info.text

    if 'rent' not in locals(): rent = np.nan
    if 'condominium' not in locals(): condominium = np.nan
    if 'taxes' not in locals(): taxes = np.nan
    if 'fire_insurance' not in locals(): fire_insurance = np.nan
    if 'services' not in locals(): services = np.nan
    if 'total' not in locals(): total = np.nan

    return{
        "Title":title,
        "Address":address,
        "Area":area,
        "Bedroom":bedroom,
        "Garage":garage,
        "Floor":floor,
        "Pet":pet,
        "Furniture":furniture,
        "Area":area,
        "Subway":subway,
        "Rent":rent,
        "Condominium":condominium,
        "Taxes":taxes,
        "Fire Insurance":fire_insurance,
        "Services":services,
        "Total":total
    }

#Initializing the webdriver
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
path = 'chromedriver'
driver = webdriver.Chrome(executable_path=path, options=options)

url = 'https://www.quintoandar.com.br/alugar/imovel/sao-paulo-sp-brasil'
driver.get(url)
time.sleep(5)
driver.set_window_size(1600, 1024)
time.sleep(3)

num_houses = 8000
historical_houses = []
houses = []

#Fix - Scrolling the page a few items and going back to initial
aux = driver.find_elements_by_xpath("//div[@class='sc-1qwl1yl-0 igVsBW']")
driver.execute_script("arguments[0].scrollIntoView();", aux[12])
time.sleep(.5)
driver.execute_script("arguments[0].scrollIntoView();", aux[0])
time.sleep(.5)

while len(houses) < num_houses:

    house_buttons = driver.find_elements_by_xpath("//div[@class='sc-1qwl1yl-0 igVsBW']")

    for house_button in house_buttons:

        #Fix - Sometimes the element is fond, but I am getting "element not attached" error (idk why). This remove those cases
        try:
            text = house_button.text
        except:
            continue
        
        #Check if button is indeed a house and if it wasnt previously scrapped
        if (not 'Sem tempo pra procurar' in house_button.text) and (not 'Ainda não encontrou seu lar' in house_button.text) and (not house_button in historical_houses):

            print("Progress: {}".format("" + str(len(houses)) + "/" + str(num_houses)))

            house_button.click()

            #Try to open new tab (if it fails keep trying 5 more times)
            new_tab = False
            retry_qty = 0
            while not new_tab and retry_qty < 5:
                try:
                    #Switch to it
                    driver.switch_to.window(driver.window_handles[1])
                    new_tab = True
                except:
                    retry_qty = retry_qty + 1
                    time.sleep(.3)

            if not new_tab:
                continue

            #Wait page load its infos (if it fails keep trying 10 more times)
            page_loaded = False
            retry_qty = 0
            while not page_loaded and retry_qty < 10:
                try:
                    driver.find_elements_by_xpath("//li[contains(@class, 'MuiListItem-root rf1epz-0')]")
                    driver.find_element_by_xpath("//h1[@class='sc-1q9n36n-0 ghXeyc sc-bdVaJa hgGleC']").text
                    page_loaded = True
                except:
                    retry_qty = retry_qty + 1                            
                    time.sleep(.5)
            
            if not page_loaded:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(.5)
                continue

            ##LOADING THE DATA
            data = get_data(driver)
            data['Text'] = text
            houses.append(data)
            
            #Close Tab and go back to main
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(.5)

    #Save all elements scrapped
    historical_houses = historical_houses + house_buttons
    pd.DataFrame(houses).to_csv('quintoandar_data.csv', index=False)

driver.close()
