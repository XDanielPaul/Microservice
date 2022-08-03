## Microservice pre prácu s externým API
Zadanie bolo integrované do celku pomocou Flasku, ktorý volá requesty na svoj backend a výsledok zobrazuje na frontende. Ako databázové riešenie bolo použité SQLite s SQLAlchemy.

Verzia Pythonu 3.9.6
VirtualEnv 20.1.0

#### Spustenie:
- pomocou príkazu v konzoli si treba vytvoriť virtuálne prostredie *virtualenv "meno projektu"*
- Do vygenerovaného priečinku treba clonenuť súbory z github repozitára
- Následne si vo vygenerovanom priečinku treba aktivovať virtuálne prostredie pomocou príkazu v konzoli *source Scripts/activate*
- nainštalovanie dependencií pomocou príkazu v konzoli *pip install -r requirements.txt*
- v priečinku *src* pomocou príkazu v konzoli *set FLASK_APP = app.py*  treba nastaviť target pre flask
- v priečinku *src* vygenerovanie tabuľky v .db súbore príkazom *flask restart_tables*
- v priečinku *src* spustenie pomocou príkazu v konzoli *flask run* alebo *python app.py*
- zahostuje sa lokálny server na adrese http://127.0.0.1:5000/

#### Funkcionalita:
- na začiatku sa otvorí landing page
- na navigation bare sú taby s rozdelenou funkcionalitou
- pri "Add post" si uživateľ vyberie UserID pod akým chce príspevok uverejniť, nadpis, telo a odošle ho tlačítkom Add post
- pri "Search posts" si môže vyfiltrovať posty podľa id postu alebo id užívateľa
- posty, ktoré sú uložené v databázi je možné editovať a mazať
  
### Poznámky:
- rozdelil som zobrazovanie postov pre väčšiu prehľadnosť
- API som integroval do riešenia
- zameriaval som sa na backend riešenia, takže frontend je veľmi provizorný a slúži iba na manipuláciu a zobrazovanie
- čas strávený na úlohe: 9 hodín