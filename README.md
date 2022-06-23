# CeneoWebScraper

## Instalacja

### Konfiguracja interaktywna

W przypadku braku pliku config.yml w katalogu głównym aplikacji, uruchomiony zostanie tekstowy konfigurator pozwalający na jego stworzenie jak i oferujący możliwość wygenerowania pomocniczego pliku stack.yml, który pozwoli na łatwe na uruchomienie bazy danych z wykorzystaniem oprogramowania [Docker](https://www.docker.com/get-started/) przy pomocy polecenia:

```bash
docker compose -f stack.yml up
```

> Uwaga! Baza danych programu powinna być pusta przy pierwszym uruchomieniu, program sam utworzy odpowiednie tabele po połączeniu się z nią.

### Konfiguracja ręczna

#### Baza danych MySQL (Docker)

Program współpracuje z bazą danych MySQL, którą na potrzeby m.in. pracy lokalnej można uruchomić z wykorzystaniem oprogramowania wirtualizacyjnego Docker.

Oto przykładowa zawartość pliku stack.yml:

```yml
version: '3.1'

services:
  db:
    image: mysql
    environment:
      MYSQL_ROOT_PASSWORD: passwd
    ports:
      - "3307:3306"
```

Aby uruchomić serwer MySQL po utworzeniu pliku można skorzystać z komendy:

```bash
docker compose -f stack.yml up
```

#### Konfiguracja programu

By program mógł pracować prawidłowo, konieczne jest utworzenie pliku config.yml w katalogu głównym projektu zawierającego dane konfiguracyjne połączenia z bazą danych.

Oto przykładowa zawartość pliku config.yml, pozwalająca na połączenie z bazą danych uruchomioną w poprzedniej sekcji:

```yml
db:
  username: root
  password: passwd
  hostname: localhost
  port: 3307
```
## Struktura opinii w serwisie [Ceneo.pl](https://www.ceneo.pl/101052360#tab=reviews)

|Skadowa opinii|Selektor|Nazwa zmiennej|Typ danych|
|--------------|--------|--------------|----------|
|opinia|div.js_product-review|opinion|bs4.element.Tag|
|identyfikator opinii|div.js_product-review\["data-entry-id"\]|opinion_id||
|autor opinii|span.user-post__author-name|author||
|rekomendacja autora|span.user-post__author-recomendation > em|recommendation||
|liczba gwiazdek|span.user-post__score-count|stars||
|treść opinii|div.user-post__text|content||
|lista zalet|div\[class$=positives\] ~ div.review-feature__item|pros||
|lista wad|div\[class$=negatives\] ~ div.review-feature__item|cons||
|dla ilu osób przydatna|button.vote-yes > span|useful||
|dla ilu osób nieprzydatna|button.vote-no > span|useless||
|data wystawienia opinii|span.user-post__published > time:nth-child(1)\["datetime"\]|published||
|data zakupu produktu|span.user-post__published > time:nth-child(2)\["datetime"\]|purchased||
|potwierdzenie zakupem|div.review-pz|verified_purchase||