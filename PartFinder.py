from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_parts(serial_number):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    url = f"https://ovoko.pl/szukaj?q={serial_number}"
    print(f"URL: {url}")
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    parts = []
    for item in soup.find_all("div", class_="products__items"):
        name = item.find("div", class_="products__text__header")
        price = item.find("div", class_="products__price")
        description = item.find("div", class_="products__text__description__main")
        link = item.find("a", href=True, class_="ga-tracking-event-js")
        parts.append({"name": name.text.strip(), "description": description.text.strip(), "price": price.text.strip(), "link": link['href']})
    driver.quit()
    if not parts:
        print("There are no parts with this serial number")
    else:
        return sorted(parts, key=lambda x: x["price"])

serial_number = input("Enter the serial number of the part: ")
brand = input("Enter the brand of your vehicle: ")
vehicle_type = input("Enter the type of your vehicle: ")
i=0

parts = get_parts(serial_number)
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
            print(f"{part['name']} - for {part['price']} - and it was in {part['description']} - LINK: {part['link']}")
        print("\n")