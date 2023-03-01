from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import jinja2


app = Flask(__name__)
env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET','POST'])
def results():
    serial_number = request.form.get('serial_number')
    print(f'serial_number: {serial_number}')
    additional_info = request.form.get('additional_info')
    if (additional_info == "yes"):
        brand = request.form.get('brand')
        vehicle_type = request.form.get('vehicle_type')

        parts = get_parts(serial_number)

        if not parts:
            message = "There are no parts with this serial number"
            return render_template('results.html', message=message)

        # Filter parts by brand and vehicle type
        matching_parts = [part for part in parts if brand.lower() in part['description'].lower() and vehicle_type.lower() in part['description'].lower()]
        if not matching_parts:
            message = "There are no parts that match your vehicle"
            return render_template('results.html', message=message)

        # Recommend the part with the lowest price
        recommended_part = min(matching_parts, key=lambda x: x['price'])

        return render_template('results.html', parts=parts, recommended_part=recommended_part)

    else:
        parts = get_parts(serial_number)

        if not parts:
            message = "There are no parts with this serial number"
            return render_template('results.html', message=message)

        return render_template('results.html', parts=parts)


if __name__ == '__main__':
    app.run(debug=True)
