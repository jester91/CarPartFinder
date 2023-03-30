from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_parts_ovoko(serial_number):
    options = Options()
    options.headless = True
    with webdriver.Chrome(options=options) as driver:
        url = f"https://ovoko.pl/szukaj?q={serial_number}"
        print(f"URL: {url}")
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        parts = []
        for item in soup.find_all("article"):
            name = item.find("div", class_="products__text__header")
            price = item.find("div", class_="products__price")
            description = item.find("div", class_="products__text__description__main")
            link = item.find("a", href=True, class_="ga-tracking-event-js")
            parts.append({"name": name.text.strip(), "description": description.text.strip(), "price": price.text.strip(), "link": link['href']})
        if not parts:
            print("There are no parts with this serial number")
        else:
            return sorted(parts, key=lambda x: x["price"])

def get_parts_olx(serial_number):
    options = Options()
    options.headless = True
    with webdriver.Chrome(options=options) as driver:
        url = f"https://www.olx.pl/oferty/q-{serial_number}"
        print(f"URL: {url}")
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        olx_parts = []
        for item in soup.find_all("div", class_="css-oukcj3"):
            name = item.find("h6", class_="css-16v5mdi er34gjf0")
            price = item.find("p", class_="css-10b0gli er34gjf0")
            description = item.find("p", class_="css-veheph er34gjf0")
            link = item.find("a", href=True, class_="css-rc5s2u")
            olx_parts.append({"name": name.text.strip(),"description": description.text.strip(), "price": price.text.strip(), "link": link['href']})
        if not olx_parts:
            print("There are no parts with this serial number")
        else:
            return sorted(olx_parts, key=lambda x: x["price"])

def get_parts_ebay_klein(serial_number):
    options = Options()
    options.headless = True
    with webdriver.Chrome(options=options) as driver:
        url = f"https://www.ebay-kleinanzeigen.de/s-{serial_number}/k0"
        print(f"URL: {url}")
        driver.get(url)
        
        try:
            # Wait for the search results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "aditem-main"))
            )
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            ebayklein_parts = []
            for item in soup.find_all("article", class_="aditem"):
                name = item.find("a", class_="ellipsis")
                price = item.find("p", class_="aditem-main--middle--price-shipping--price")
                description = item.find("p", class_="aditem-main--middle--description")
                link = item.find("a", href=True, class_="ellipsis")
                ebayklein_parts.append({"name": name.text.strip(),"description": description.text.strip(), "price": price.text.strip(), "link": link['href']})
            if not ebayklein_parts:
                print("There are no parts with this serial number")
            else:
                return sorted(ebayklein_parts, key=lambda x: x["price"])
        except Exception as e:
            print(f"An error occurred while searching eBay Kleinanzeigen: {e}")
            print(driver.page_source)
        finally:
            driver.quit()

serial_number = input("Enter the serial number of the part: ")
additional_info = input("Do you want to share more information about your car? (If you share it will recommend the best option) Skip if no ")
if (additional_info == "yes"):
    brand = input("Enter the brand of your vehicle: ")
    vehicle_type = input("Enter the type of your vehicle: ")

    parts = get_parts_ovoko(serial_number)
    print("\n")

    if not parts:
        print("There are no parts with this serial number")
    else:
        # Filter parts by brand and vehicle type
        matching_parts = [part for part in parts if brand.lower() in part['description'].lower() and vehicle_type.lower() in part['description'].lower()]

        if not matching_parts:
            print("There are no parts that match your vehicle")

        else:
            # Recommend the part with the lowest price
            recommended_part = min(matching_parts, key=lambda x: x['price'])

            print(f"The recommended part for your {brand} {vehicle_type} is:")
            print(f"{recommended_part['name']} - {recommended_part['price']} - and it was in {recommended_part['description']} - LINK: {recommended_part['link']}")
            print("\n")

            print(f"All Parts for serial number {serial_number}:")
            for part in parts:
                if(part['description']):
                    print(f"{part['name']} - for {part['price']} - and it was in {part['description']} - LINK: {part['link']}")
                else:
                    print(f"{part['name']} - for {part['price']} - LINK: {part['link']}")
            print("\n")
else:
#TODO I have to find a better solution to look up different websites
    #parts = get_parts_ovoko(serial_number)
    #parts+= get_parts_olx(serial_number)
    parts= get_parts_ebay_klein(serial_number)
    print("\n")
    if not parts:
        print("There are no parts with this serial number")
    else:
        for part in parts:
            full_link="https://www.ebay-kleinanzeigen.de"+part["link"]
            print(f"{part['name']} - {part['price']} - and it was in {part['description']} - LINK: {full_link}")
