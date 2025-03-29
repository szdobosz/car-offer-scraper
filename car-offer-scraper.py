#załadowanie bibliotek potrzebnych do działania programu
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import concurrent.futures

#podstawowe URL otomoto, dzięki któremu można później ściągać oferty samochodów osobowych
BASE_URL = "https://www.otomoto.pl/osobowe/"
#nagłówek User-Agent sprawia, że program wygląda dla strony internetowej (w tym przypadku Otomoto) jak przeglądarka Chrome/Safari; Accept-language wskazuje preferowany język; Referer wskazuje serwerowi, skąd pochodzi żądanie (tutaj z google.com)
#dzięki tym nagłówkom, program wygląda dla serwera jak rzeczywista przeglądarka internetowa, a nie np. bot, co zmniejsza ryzyko odzrucenia żądania i ograniczenia dostępu do Otomoto
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.google.com"
}

#ta funkcja pobiera linki (maksymalnie 10 stron) zaczynających się jak BASE_URL
def get_page_links(model, max_pages=10):
    links = []
    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}{model}?page={page}"
        print(f"Pobieranie strony: {url}")
        try:
            response = requests.get(url,headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            #program wyszukuje wprowadzoną przez użytkownika liczbę stron, na każdej z tych stron szuka tytułów ofert (na podstawie kodu/klasy HTML) i wybiera z nich pojedyncze linki
            ads = soup.find_all('h2', class_='e4b361b0') #Tytuł/Nagłówek oferty
            if not ads:
                print("Nie znaleziono ofert na stronie.")
                return []

            for ad in ads:
                link = ad.find('a').get('href')
                if link:
                    links.append(link)
        except requests.RequestException as e:
            print(f"Błąd podczas pobierania strony: {e}")
            break
    return links

#ta funkcja pobiera szczegóły ofert na podstawie informacji zawartych w klasach HTML
def scrape_offer_details(url):
    print(f"Pobieranie szczegółów oferty: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)
        #return 0

        # Pobierz szczegóły oferty
        details = {}
        details["Link"] = url

        # Nazwa pojazdu
        title = soup.find('h1', class_="offer-title big-text e12csvfg2 ooa-1dueukt")#class_="offer-title big-text e12csvfg2 ooa-1dueukt er34gjf0"
        details["Nazwa pojazdu"] = title.text.strip() if title else "Brak"

        # Skrócony opis
        #short_description = soup.find('div', class_='ewg8vos8 ooa-1tku07r er34gjf0') #'p'
        #details["Skrócony opis"] = short_description.text.strip() if short_description else "Brak" #NIEISTOTNE!!!!!!!

        # Cena i waluta
        price = soup.find('h3',class_="offer-price__number ex6ng1i5 ooa-1kdys7g" )#class_="offer-price__number evnmei44 ooa-1kdys7g"
        currency = soup.find('p', class_="offer-price__currency ex6ng1i6 ooa-m6bn4u")#class_="offer-price__currency ex6ng1i6 ooa-m6bn4u"
        details["Cena"] = price.text.strip() if price else "Brak"
        details["Waluta"] = currency.text.strip() if currency else "Brak"

        # Szczegóły techniczne
        params = soup.find_all('div', class_="ooa-1jqwucs e1btp7411" )#class_="ooa-1jqwucs ee3fiwr1"
        for param in params:
            #nazwa parametru (np. Pojemność skokowa, moc, przebieg)
            keys = param.find_all('p', class_="e1btp7413 ooa-rlgnr")#class_="ee3fiwr3 ooa-rlgnr"
            #wartość parametru (np. 1496 cm3, 200 KM, 82800 km)
            values = param.find_all('p', class_="e1btp7412 ooa-1rcllto")#class_="ee3fiwr2 ooa-1rcllto"
            for key, value in zip(keys, values):
                details[key.text.strip()] = value.text.strip()

        return details
    except requests.RequestException as e:
        print(f"Błąd podczas pobierania szczegółów: {e}")
        return None

#główna funkcja programu
def main():
    #wprowadzenie marki/modelu samochodu + liczby stron z ofertami
    model = input("Podaj model samochodu (np. audi/a4): ").strip().lower()
    max_pages = int(input("Podaj maksymalną liczbę stron do przeszukania: "))

    #pobieranie linków
    links = get_page_links(model, max_pages=max_pages)
    print(f"Znaleziono {len(links)} ofert.")

    #pobieranie szczegółów z wyszukanych ofert
    offers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(scrape_offer_details, link): link for link in links}
        for future in concurrent.futures.as_completed(future_to_url):
            details = future.result()
            if details:
                offers.append(details)

            #opcjonalna przerwa między żądaniami
            time.sleep(1)

    #zapisanie wyników do pliku Excel
    if offers:
        df = pd.DataFrame(offers)
        output_file = f"{model.replace('/', '_')}_otomoto.xlsx"
        df.to_excel(output_file, index=False)
        print(f"Zapisano dane do pliku: {output_file}")
    else:
        print("Brak danych do zapisania.")

#inicjacja programu
if __name__ == "__main__":
    main()