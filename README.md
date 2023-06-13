# UnEmploymentApi

Ten projekt przedstawia proces ETL pipeline (Extract, Transform, Load) w języku Python, który pobiera dane z REST-API BDL (Bank danych lokalnych), przetwarza je i zapisuje do plików w formacie .csv

## Opis projektu

W związku z potrzebą uruchomienia programu na Oracle linux 6, została użyta werjsa Python 3.6.8

Projekt ma na celu zautomatyzowanie pobierania danych z REST-API BDL, które zawierają informacje statystyczne na temat stopy bezrobocia w powiatach, województach i Polsce. Naspnie dane są przetwarzane, tak aby uzyskać potrzebne informacje w odpowiednim formacie, a finalnie zapisywane do plików CSV.

Użytkownik będzie miał wybór sposobu pobierania danych:

- Pobieranie danych dla kolejnych miesięcy zgodnych z plikiem konfiguracyjnym.
- Wybór roku lub/i miesiąca, dla którego mają być pobrane dane.

## Kroki instalacji dla Oracle Linux 6

1. [Instalacja pythona 3.6.8 na Oracle linux 6](#install-python-on-oracle-linux-6)

2. [Pobranie repo projektu](#pobieranie-projektu)

3. [Konfiguracja projektu](#konfiguracja-projektu)

### install python on oracle linux 6

W celu zapewnienia prawidłowego działania Pythona należy przejść poniższe korki:

Na samym początku musisz zainstalować niezbędne paczki do prawidłowego działania Pythona.

~~~~bash
sudo yum install openssl openssl-devel zlib-devel bzip2 bzip2-devel readline-devel 
sqlite sqlite-devel tk-devel libffi-devel gdbm-devel
~~~~

Utworzyć folder python w ścieżce do której chcemy pobrać plik

~~~~bash
mkdir python
cd python
~~~~

Pobierz Pythona w wersji 3.6.8:

~~~~bash
wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz
~~~~

Następnie rozpakuj go:

~~~~bash
tar xvzf Python-3.6.8.tgz
~~~~

Po rozpakowaniu przejdź do folderu i uruchom proces konfiguracji środowiska.

Poprzez --prefix zmieniamy domyślny folder instalacji

~~~~bash
cd Python-3.6.8
./configure --prefix=/opt/python3.6
~~~~

Kompilacja i instlacja

~~~~bash
make && sudo make install
~~~~

Po instalacji należy wykonać polecenia tworzące symbolic links

~~~~bash
sudo ln -s /opt/python3.6/bin/python3.6 /usr/bin/python36
sudo ln -s /opt/python3.6/bin/idle3.6 /usr/bin/idle-python36
sudo ln -s /opt/python3.6/bin/pip3 /usr/bin/pip
~~~~

Przetestuj czy działa:

~~~~bash
python36
~~~~

Po urochomieniu powinno przejść do pythona. w celu wyjścia wpisujemy exit()

### pobieranie projektu

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

tar xvzf main.zip
~~~~

### konfiguracja projektu

W głównym folderze projektu musimy utworzyć niezbędne pliki do działania narzędzie:

#### Instalacja środowiska wirtualnego

~~~~bash
python3 -m venv my_venv
~~~~

#### utworzenie pliku ze zmiennymi środwiskowymi

~~~~bash
nano .env
~~~~

Wpisujemy potrzebne zmienne:

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

#### Aktuwacja środowiska i instalacja niezbędnych paczek

~~~~bash
source my_venv/bin/activate

pip install -r requirements.txt
~~~~
