# ASEiED-Zad4
Projekt zaliczeniowy z przedmiotu Autonomiczne Systemy Ekspertyzy i Eksploracji Danych

## Treść zadania
Wykonaj analizę danych tekstowych pochodzących z różnych stron internetowych. Zebrane dane zgrupowane zostały w foldery odpowiadające dacie zapisu. Zadanie wymaga przeanalizowania danych ze stron stworzynych w jęzku polski w dwóch przedziałach czasowych:
- marzec/kwiecień 2019
- marzec/kwiecień 2019

W rozpatrywanych przedziałach czasowych szukamy wystąpień słów tj. wirus, covid19, covid, pandemia.

Analiza porównawcza powinna pokazywać wzrost użycia wskazanych słów. Wzrost należy pokazać w skali dniowej. Na podstawie meta informacji należy dokonać klasyfikacji tematycznej wykorzystanych do analizy stron.
Zbiory danych:  
- http://commoncrawl.org/the-data/get-started/  
- https://registry.opendata.aws/commoncrawl/  

Wymagania:
- Technologie: EMR/Spark/Python/Scala/Java
- Rezultaty proszę zaprezentować w formie graficznej z wykorzystaniem odpowiedniej biblioteki 
- Kod źródłowy projektu należy umieścić w środowisku github
- Sprawozdanie projektu należy zapisać w pliku README.md

## Konfiguracja na Amazon Web Services
1. Stworzenie klucza korzystając z _EC2_ (w formacie _ppk_)
2. Stworzenie _bucket_ na _S3_ oraz wrzucenie skryptów, które będą wykorzystywane do obliczeń
3. Stworzenie i konfiguracja klastra obliczeniowego w EMR (Elastic Map Reduce):
    - Tworzenie w trybie zaawansowanym
    - Wybranie pożądanych opcji konfiguracyjnych
    - Konfiguracja _bootstrap actions_ w celu instalacji modułów na node'ach master oraz slave (zreazlizowane poprzez skrypt shellowy)
    - Podpięcie wspomnianego w punkcie pierwszym klucza
    - Określenie reguł SSH dla ruchu przychodzącego
    - Połączenie się z węzłem głównym Amazon EMR za pomocą SSH
4. Działania na klastrze w celu uruchomienia skryptu:
    - Za pomocą komendy _**aws s3 cp s3://bucket/plik .**_ pobierany jest plik na główny węzeł
    - Za pomocą komendy _**spark-submit ./plik**_ uruchamiany jest skrypt
    
## Opis rozwiązania
### AWS 
Rozpoczęto od nawiązania sesji za pomocą _SparkSession_
Następnie w oparciu o zasoby commoncrawl wysyłano zapytania SQL w następującej postaci:
```SQL
SELECT url, warc_filename, warc_record_offset, warc_record_length
FROM ccindex
WHERE crawl='CC-MAIN-2020-16' 
AND subset='warc' 
AND url_host_tld='pl'
```
Rezultat tego zapytania był przetwarzany w celu uzyskania pojedynczego rekordu. Na jego podstawie udało się wyodrębnić dane pozwalające wyznaczyć liczbę wystąpień pożądanych słów, a także dostać się do metadanych umożliwających klasyfikacje stron na różną tematykę (np. rozrywka, polityka, technologia).

Po przetworzeniu danych były one dostosowywane do przedstawionej formy ([data, słowa_kluczowe, poszukiwane_słowo, ilość_wystąpień]) oraz zapisywane na bucket.
### Graficzne przedstawienie danych
W odrębnym skrypcie napisanym w języku python dokonano dalszego przetwarzenia dancych w celu graficznego przedstawienia różnic wystąpień słów pandemia, covid, covid19, wirus.

Jest to zrealizowane jako wykres słupkowy, gdzie x jest osią czasu z podziałem na dni miesiąca marca i kwietnia. 
Poniżej przedstawiono wykresy porównawcze dla każdego ze słów. Porównano wystąpienia z roku 2019 oraz 2020.
![wirus](https://raw.githubusercontent.com/MichalStachowski/ASEiED-Zad4/master/img/wirus_porownanie.png)
![pandemia](https://raw.githubusercontent.com/MichalStachowski/ASEiED-Zad4/master/img/pandemia_porownanie.png)
![covid](https://raw.githubusercontent.com/MichalStachowski/ASEiED-Zad4/master/img/covid_porownanie.png)
![covid19](https://raw.githubusercontent.com/MichalStachowski/ASEiED-Zad4/master/img/covid19_porownanie.png)
Z przedstawionych powyżej wykresów można zauważyć brak punktów wspólnych dla wystąpień danego dnia. Widać jednak również wzrost występowania poszukiwanych fraz na korzyść roku 2020 (przy analizie zbliżonej liczby stron internetowych).

W celu głębszego ukazania różnic dokonano kategoryzacji treści. Kategoryzacja polegała na wyodrębnieniu najczęściej występujących słów kluczowych i przypisaniu ich do jednej z następujących kategorii:
* edukacja
* zdrowie
* polityka
* technologia
* rozrywka
* pozostałe

Wyniki kategoryzacji zostały przedstawione w poniższej tabeli:
![kategorie](https://raw.githubusercontent.com/MichalStachowski/ASEiED-Zad4/master/img/klasyfikacja_metadane.PNG)  
Widać, że w każdej z analizowanych dziedzin życia nastąpił wzrost zainteresowania pandemią oraz tematami z nią związanymi.
