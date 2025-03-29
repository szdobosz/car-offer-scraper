# **OTOMOTO SCRAPER**
1. **Cel projektu:**

Projekt polega na scrapowaniu danych na temat ogłoszeń z Otomoto. W obecnej wersji eksportuje do Excela dane takie jak: marka, model, rok produkcji, cena, waluta, przebieg, rodzaj paliwa.

2. **Jakie biblioteki są używane:**

**requests**
- Używana do wysyłania żądań HTTP i pobierania zawartości stron internetowych.

**BeautifulSoup (z bs4)**
- Służy do analizy kodu HTML i ekstrakcji danych z wybranych elementów strony.

**pandas**
- Używana do organizacji danych w tabelach i zapisywania ich do pliku Excel.

**time**
- Wykorzystywana do wprowadzenia opóźnień między żądaniami w celu uniknięcia blokady IP przez serwer Otomoto.

**concurrent.futures**
- Pozwala na równoległe wykonywanie żądań HTTP, przyspieszając pobieranie danych z wielu stron.

3. **Opisz (dodaj komentarze w kodzie) krok po kroku co wykonuje się w skrypcie.**

4. **Podaj przykłady danych wejściowych.**

- **Model samochodu**

W formacie: audi/a4, bmw/m5, toyota/corolla

Używany do generowania URL podstron Otomoto, np.: https://www.otomoto.pl/osobowe/audi/a4.

- **Maksymalna liczba stron**

Liczba całkowita (np. 5, 10), która wskazuje, ile stron wyników wyszukiwania program ma przeszukać.

5. **Wyjaśnij, jak interpretować wyniki.**

Dane zapisane w pliku Excel zawierają następujące kolumny
Każdy wiersz odpowiada jednej ofercie. Kolumny zawierają następujące informacje:

- Link: URL do oferty.

- Nazwa pojazdu: Tytuł oferty.

- Cena i Waluta: Cena podana w ogłoszeniu oraz waluta.

- Parametry techniczne: Szczegóły, takie jak rok produkcji, przebieg, moc, pojemność silnika.

6. **Opisz, jak można rozszerzyć projekt.**

- **Dodanie nowych parametrów**

Wyszukanie dodatkowych szczegółów ofert, takich jak lokalizacja, data publikacji ogłoszenia, czy wyposażenie.

- **Obsługa większej liczby kategorii**

Rozszerzenie wyszukiwań o inne sekcje Otomoto, np. samochody dostawcze, motocykle, przyczepy.

- **Filtrowanie wyników**

Dodanie opcji wprowadzania kryteriów, takich jak przedział cenowy, rocznik, maksymalny przebieg (opcje filtrów ewentualnie działają częsciowo w skoroszycie Excela.)

- **Obsługa większej liczby serwisów**

Rozszerzenie na inne portale motoryzacyjne, np. Autoscout, Mobile.de.

- **Automatyczna aktualizacja**

Ustawienie harmonogramu automatycznego pobierania danych (np. raz dziennie).

- **Poprawa odporności na zmiany w HTML strony**

Implementacja mechanizmów adaptacyjnych na wypadek, gdyby struktura strony Otomoto się zmieniła. Można to osiągnąć, np. przez użycie bibliotek obsługujących dynamiczne renderowanie.

![image](https://github.com/user-attachments/assets/2092c16c-46f4-43f7-b5da-ac729d684c26)
![image](https://github.com/user-attachments/assets/eb263d66-86a5-4b7a-ab85-f9d99504cb97)


