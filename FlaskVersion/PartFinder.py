from flask import Flask, render_template, request
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
        for item in soup.find_all("div", class_="products__items"):
            name = item.find("div", class_="products__text__header")
            price = item.find("div", class_="products__price")
            description = item.find(
                "div", class_="products__text__description__main")
            link = item.find("a", href=True, class_="ga-tracking-event-js")
            if name:
                parts.append({
                    "name": name.text.strip(),
                    "description": description.text.strip(),
                    "price": price.text.strip(),
                    "link": link['href']
                })
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
            if name:
                olx_parts.append({
                    "name": name.text.strip(),
                    "description": description.text.strip(),
                    "price": price.text.strip(),
                    "link": link['href']
                })
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
                price = item.find(
                    "p", class_="aditem-main--middle--price-shipping--price")
                description = item.find(
                    "p", class_="aditem-main--middle--description")
                link = item.find("a", href=True, class_="ellipsis")
                if name:
                    ebayklein_parts.append({
                        "name": name.text.strip(),
                        "description": description.text.strip(),
                        "price": price.text.strip(),
                        "link": link['href']
                    })
        except Exception as e:
            print(f"An error occurred while searching eBay Kleinanzeigen: {e}")
            print(driver.page_source)
        finally:
            driver.quit()

        return sorted(ebayklein_parts, key=lambda x: x["price"])


app = Flask(__name__)

# Define your other functions here


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Process the form data here
        serial_number = request.form['serial_number']

        # Process the data and retrieve the results from different websites
        ebay_parts = get_parts_ebay_klein(serial_number)
        ovoko_parts = get_parts_ovoko(serial_number)
        olx_parts = get_parts_olx(serial_number)

        # Process the retrieved parts and prepare the message
        message = ""


        if not ebay_parts:
            message += "There are no parts with this serial number on eBay Kleinanzeigen\n"
        else:
            message += "eBay Kleinanzeigen:\n"
            for part in ebay_parts:
                part['full_link'] = "https://www.ebay-kleinanzeigen.de" + part["link"]
                message += f"{part['name']} - {part['price']} - {part['description']} - {part['full_link']}\n"

        if not olx_parts:
            message += "There are no parts with this serial number on OLX\n"
        else:
            message += "OLX:\n"
            for part in olx_parts:
                part['full_link'] = "https://www.olx.pl" + part["link"]
                message += f"{part['name']} - {part['price']} - {part['description']} - {part['full_link']}\n"

        if not ovoko_parts:
            message += "There are no parts with this serial number on Ovoko\n"
        else:
            message += "Ovoko:\n"
            for part in ovoko_parts:
                part['full_link'] = "https://ovoko.pl/" + part["link"]
                message += f"{part['name']} - {part['price']} - {part['description']} - {part['full_link']}\n"

        return render_template('results.html', message=message, parts=[])

    return render_template('index.html')


@app.route('/results', methods=['GET', 'POST'])
def results():
    serial_number = request.form['serial_number']

    # Process the data and retrieve the results from different websites
    ebay_parts = get_parts_ebay_klein(serial_number)
    ovoko_parts = get_parts_ovoko(serial_number)
    olx_parts = get_parts_olx(serial_number)

    parts = ebay_parts + ovoko_parts + olx_parts

    message = "No parts found." if not parts else ""

    return render_template('results.html', message=message, parts=parts)


if __name__ == '__main__':
    app.run(debug=True)
