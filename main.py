import json
import re
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ChromeDriver
import Space_type
from dash import Dash, dash_table, html, Input, Output
import webbrowser
import urllib.parse

driver = ChromeDriver.configure_driver()

url = Space_type.get_url()

final_url = Space_type.open_browser_and_select_filters(url,driver)

def show_results(data):
    for index, item in enumerate(data, start=1):
        print(f"Anunț {index}:")
        for key, value in item.items():
            print(f"  {key}: {value}")
        print("-" * 50)

def write_results(filename, data):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(f"Rezultatele au fost salvate în '{filename}'.")

def extract_price(price_text):
    """Extrage prețul numeric din textul prețului"""
    if price_text:
        # Înlocuim orice text care nu este o cifră sau simbolul "$" (de exemplu " per month")
        match = re.search(r'(\d+)', price_text.replace('$', '').replace(' per month', '').strip())
        if match:
            return int(match.group(1))  # Returnăm prețul ca număr
    return None  # Dacă nu există preț, returnăm None

def scrape_website():
    driver = ChromeDriver.configure_driver()
    driver.get(final_url)

    print(f"Search on: {final_url}")
    try:
        # Așteaptă să se încarce pagina
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.premium.css-1omkpog.e1jqslr40')))
        print("Pagina s-a încărcat cu succes")

        # Găsește containerele
        containers = driver.find_elements(By.CSS_SELECTOR, '.item.css-1cpzyck.eq4or9x0')
        if not containers:
            print("Nu s-au găsit anunțuri pe pagină.")
            return []
        else:
            print("Container găsit")
            data = []
            for container in containers:
                try:
                    # Creează un dicționar pentru a stoca informațiile
                    item_data = {}

                    # Titlul (headline)
                    button = container.find_element(By.TAG_NAME, 'button')
                    item_data['headline'] = button.get_attribute('headline')

                    # Prețul
                    try:
                        price_element = container.find_element(By.CSS_SELECTOR, '.price')
                        item_data['price'] = price_element.text
                    except:
                        item_data['price'] = None

                    # Link-ul
                    try:
                        link_element = container.find_element(By.TAG_NAME, 'a')
                        item_data['link'] = link_element.get_attribute('href')
                    except:
                        item_data['link'] = None

                    # Locația
                    try:
                        location_element = container.find_element(By.CSS_SELECTOR, '.address')  # Ajustează selectorul
                        item_data['location'] = location_element.text
                    except:
                        item_data['location'] = None

                    # Adaugă informațiile în lista finală
                    data.append(item_data)

                except Exception as e:
                    print(f"Eroare la procesarea containerului: {e}")

            return data

    except Exception as e:
        print(f"Eroare generală: {e}")
        return []

    finally:
        driver.quit()

def run_dash_app(data):
    # Locația utilizatorului (setată manual pentru acest exemplu)
    user_lat, user_lng = 11.5564, 104.9282  # Phnom Penh, Cambodgia (exemplu)

    # Transformăm datele într-un DataFrame
    df = pd.DataFrame(data)

    # Creăm aplicația Dash
    app = Dash(__name__)

    app.layout = html.Div([
        html.H1("Tabel Interactiv cu Prețuri"),
        dash_table.DataTable(
            id='price-table',
            columns=[
                {'name': 'Price', 'id': 'price', 'type': 'text'},
                {'name': 'Headline', 'id': 'headline', 'type': 'text'},
                {'name': 'Location', 'id': 'location', 'type': 'text'},
            ],
            data=df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'},
            filter_action='native',  # Activăm filtrarea
            sort_action='native',    # Activăm sortarea
            sort_mode='multi',       # Permitem sortarea pe mai multe coloane
            page_size=10,
        ),
        html.Div(id='details-output', style={'marginTop': '20px'})
    ])

    # Callback pentru afișarea detaliilor și deschiderea Google Maps
    @app.callback(
        Output('details-output', 'children'),
        Input('price-table', 'active_cell')
    )
    def display_details_and_open_maps(active_cell):
        if active_cell:
            row_index = active_cell['row']
            row_data = df.iloc[row_index]
            location = row_data.get('location', 'N/A')

            # Codificăm locația pentru URL
            encoded_location = urllib.parse.quote(location)
            maps_url = f"https://www.google.com/maps/dir/{user_lat},{user_lng}/{encoded_location}"

            # Construim detalii
            details = [
                html.H4("Detalii Anunț:"),
                html.P(f"Headline: {row_data.get('headline', 'N/A')}"),
                html.P(f"Price: {row_data.get('price', 'N/A')}"),
                html.P(f"Location: {location}"),
                html.A("Deschide în Google Maps", href=maps_url, target='_blank', style={'color': 'blue'})
            ]
            return details
        return "Selectează un rând pentru detalii."

    # Pornim aplicația
    webbrowser.open('http://127.0.0.1:8051/')
    app.run_server(debug=True, port=8051, use_reloader=False)

if __name__ == "__main__":
    results = scrape_website()
    if results:
        write_results('results.json', results)
        run_dash_app(results)
