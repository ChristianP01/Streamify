# Streamify

Questo repository rappresenta il progetto sviluppato per il corso di **Tecnologie Web**.
Si tratta di un servizio di **streaming**, utilizza **Django** come framework.

Le funzionalità principali implementate sono:
* Login e registrazione di un utente;
* Possibilità di "guardare" un film;
* Possibilità di recensire un film;
* Ranking di film, per voto e per genere;
* Recommendation system basato sui gusti degli altri utenti;
* Grafici rappresentanti un riassunto dei propri gusti verso i vari generi dei film guardati;
* Group chat divisa per film;

# Usage

```
git clone https://github.com/ChristianP01/ProgettoTW.git;
cd ProgettoTW/;
pip install -r requirements.txt;
python manage.py runserver --insecure;
firefox localhost:8000/streamify/home/;
```

N.B. E' necessario usare il flag --insecure nel runnare il server perchè con debug=False potrebbe dare problemi di sicurezza nel servire file statici.
