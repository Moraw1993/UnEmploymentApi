# UnEmploymentApi

ETL Pipline for Unemployment rate from BDL API

## Install Python on Oracle linux 6

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
