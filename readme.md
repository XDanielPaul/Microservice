## Microservice pre prácu s externým API

Verzia Pythonu 3.9.6

#### Spustenie:
- nainštalovanie dependencií pomocou príkazu v konzoli *pip install -r requirements.txt*
- treba v súbore app.py prepísať v premennej *app.config['SQLALCHEMY_DATABASE_URI']* za *sqlite:///* absolútnu cestu k .db súboru
- pomocou príkazu v konzoli *set FLASK_APP = app.py*  treba nastaviť target pre flask
- spustenie pomocou príkazu v konzoli *flask run*