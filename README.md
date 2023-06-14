# UnEmploymentApi

Ten projekt przedstawia proces ETL pipeline (Extract, Transform, Load) w języku Python, który pobiera dane z REST-API BDL (Bank danych lokalnych), przetwarza je i zapisuje do plików w formacie .csv

## Opis projektu

W związku z potrzebą uruchomienia programu na Oracle linux 6, została użyta werjsa Python 3.6.8

Projekt ma na celu zautomatyzowanie pobierania danych z REST-API BDL, które zawierają informacje statystyczne na temat stopy bezrobocia w powiatach, województach i Polsce. Naspnie dane są przetwarzane, tak aby uzyskać potrzebne informacje w odpowiednim formacie, a finalnie zapisywane do plików CSV.

Użytkownik będzie miał wybór sposobu pobierania danych:

- Pobieranie danych dla kolejnych miesięcy zgodnych z plikiem konfiguracyjnym.
- Wybór roku lub/i miesiąca, dla którego mają być pobrane dane.

## Kroki instalacji dla Oracle Linux 6

1. [Instalacja pythona 3.6.8 na Oracle linux 6](#instalacja-pythona-na-oracle-linux-6)

2. [Pobranie repo projektu](#pobieranie-projektu)

3. [Konfiguracja projektu](#konfiguracja-projektu)

4. [Uruchomienie programu](#uruchomienie-narzedzia)

### Instalacja pythona na oracle linux 6

W celu zapewnienia prawidłowego działania Pythona należy przejść poniższe korki:

Na samym początku musisz zainstalować niezbędne paczki do prawidłowego działania Pythona.

1. Zainstaluj niezbędne paczki do prawidłowego działania pythona

    ~~~~bash
    sudo yum install openssl openssl-devel zlib-devel bzip2 bzip2-devel readline-devel 
    sqlite sqlite-devel tk-devel libffi-devel gdbm-devel
    ~~~~

2. Utwórz folder **python**, w której zostanie pobrany plik:

    ~~~~bash
    mkdir python
    cd python
    ~~~~

3. Pobierz Pythona w wersji 3.6.8:

    ~~~~bash
    wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz
    ~~~~

4. Rozpakuj pobrany plik:

    ~~~~bash
    tar xvzf Python-3.6.8.tgz
    ~~~~

5. Przejdź do folderu Python-3.6.8 i uruchom proces konfiguracji środowiska. Użyj parametru --prefix, aby zmienić folder instalacji:

    ~~~~bash
    cd Python-3.6.8
    ./configure --prefix=/opt/python3.6
    ~~~~

6. Kompiluj i instaluj:

    ~~~~bash
    make && sudo make install
    ~~~~

7. Po instalacji wykonaj polecenia tworzące symboliczne linki:

    ~~~~bash
    sudo ln -s /opt/python3.6/bin/python3.6 /usr/bin/python36
    sudo ln -s /opt/python3.6/bin/idle3.6 /usr/bin/idle-python36
    sudo ln -s /opt/python3.6/bin/pip3 /usr/bin/pip
    ~~~~

8. Przetestuj czy Python działa poprawnie:

    ~~~~bash
    python36
    ~~~~

Po uruchomieniu powinieneś być w interaktywnej konsoli Pythona. Aby wyjść, wpisz **exit()**.

### Pobieranie projektu

#### **GIT**

~~~~bash
git clone https://github.com/Moraw1993/UnEmploymentApi.git
~~~~

#### **SVN**

~~~~bash
svn checkout https://github.com/Moraw1993/UnEmploymentApi.git
~~~~

#### **ZIP**

~~~~bash
wget https://github.com/Moraw1993/UnEmploymentApi/archive/refs/heads/main.zip

unzip main.zip
~~~~

### Konfiguracja projektu

W głównym folderze projektu musimy utworzyć niezbędne pliki do prawidłowego działania narzędzia:

#### Instalacja środowiska wirtualnego

~~~~bash
python36 -m venv venv
~~~~

#### utworzenie pliku ze zmiennymi środwiskowymi

~~~~bash
nano .env
~~~~

Wpisujemy niezbędne zmienne:

~~~~none
X-ClientId = TOKEN_Z_BDL_API

outputFolder = sciezka/do/folderu,2sciezka/do/folderu

## email settings
EmailAcc = email account
EmailPass = email pass
EmailTo = email1@gmail.com,email2@gmail.com
mailhost = host? np. dla gmail smpt.gmail.com
port = port? np. dla gmail 587
~~~~

#### Aktywacja środowiska i instalacja niezbędnych paczek

~~~~bash
source venv/bin/activate

pip install -r requirements.txt
~~~~

### uruchomienie narzedzia

Program napisany jest zgodnie ze wzorcem CLI (Command Line Interface).

Uwaga! Przed uruchomieniem należy znaleźć się w folderze projektu i uruchomić środowisko wirtualne:

- Linux:

    ~~~~bash
    source venv\bin\activate
    ~~~~

- Windows:

    ~~~~cmd
    venv\scripts\activate.bat
    ~~~~

W celu wylistowania dostępnych możliwośći użycia programu należy użyć komendy:

~~~~bash
python main.py -h
~~~~

Możliwości:

1. Pobieranie plików zgodnie z konfiguracją w pliku config.json

    ~~~~bash
    python main.py --config config.json
    ~~~~

2. Pobieranie danych dla zadanego okresu

    Dla konkretnego roku

    ~~~~bash
    python main.py --year XXXX --month XX
    ~~~~

    lub

    Dla wszystkich miesięcy w zadanym roku

    ~~~~bash
    python main.py --year 2022
    ~~~~

    *Należy pamięc, aby miesiąc był zawsze 2 znakowy np. 01,05,12*

3. Dodawania roku do config.json

    Program co zapis danych sprawdza wartość all_download w pliku config.json, jeżeli wszystkie lata mają flage true to dodaje kolejny rok z flagami false dla wszystkich miesięcy.

    W celu wymuszenia dodania kolejnych lat możemy użyć komendy:

    ~~~~bash
    python main.py add_year X
    ### gdzie X liczba lat które chcemy dodać np. 1. Zostanie dodany kolejny rok po najwyższym istniejącym.
    ~~~~
