REST Api voor artikelen, met permissions.
In django, standaard django auth backend + UI gebruiken voor users/groups/permissions
SSL/HTTPS required (lets encrypt)

Voor een artikel zijn er 3 permissies:
- add
- change
- delete

Bij acties die een artikel aanpassen, wordt de juiste permissie gechecked.
Permissie kan in de standaard django admin UI gegeven worden op user en/of groep niveau.

Elke call heeft altijd een "result" veld en bevat "ok" = ok, of de foutmelding.

# Installatie howto
Om te testen / ontwikkelen:

- pip3 install -r requirements.txt
- cp articleapi/settings.py.example articleapi/settings.py
- aanpassen settings.py naar wens
  (voor nu alleen SECRET_KEY invullen/aanpassen en evt. DATABASE als je geen sqlite wilt)
- ./migrate.py makemigrations
- ./migrate.py migrate (maakt sqlite database aan)
- ./migrate.py createsuperuser  (maak de 1e admin account aan)
- ./migrate.py runserver

Nu draait er een debug servertje op localhost:8000 waartegen je kunt testen.
ga naar http://localhost:8000/admin/ om users te beheren

# CALLS

## POST /api/v1/login
input:
```json
{
  "username": "henk",
  "password": "lol"
}
```

output:
```json
{
 "result": "ok",
 "token": "kdjsfiowejiofjaioejfi"
}
```

curl example:
```
curl -X POST -v http://localhost:8000/api/v1/login --data '{"username": "ronald", "password": "lalala21"}'
```

## GET /api/v1/articles:
input: none

Geeft de complete lijst met artikelen terug

output:
```json
 "result": "ok",
 "articles": [
   { "1": 
     {
        "subject": "Atikel onderwerp / headline",
        "author": "henk",
        ... overige metadata die nodig is voor een lijst
     },
     "2":
     {
        "subject": "2e Artikel",
        enz. enz...
     }
   }
 ]
}
```

curl example:
```
curl http://localhost:8000/api/v1/articles
```


## GET /api/v1/article/\<id\>
input: none

output:
```json
{
  "result": "ok",
  "article": {
     "id": "<id>",
     "subject": "Artikel onderwerp",
     "body": "Artikel body",
     ... meer spannende artikel dingen
  }
}
```


## PUT /api/v1/article
Nieuw artikel aanmaken
Token moet van een user zijn met 'article add' permissions.

input:
```json
{
  "token": "<auth token>",
  "subject": "Artikel onderwerp",
  "body": "Artikel inhoud",
  "author": "auteur"
}
```

output:
```json
{
  "result": "ok",
  "id": "<nieuw aangemaakt article id>"
}
```


## POST /api/v1/article/\<id\>
Artikel aanpassen
Token moet van een user zijn met 'article change' permissions

input:
```json
{
  "token": "<auth token>",
  "subject": "nieuw subject",
  "body": "nieuwe body",
  "author": "nieuwe auteur"
}
```

output:
```json
{
  "result": "ok"
}
```

curl example:
```
curl -X POST http://localhost:8000/api/v1/article/3 --data '{"token": "d4e9f218e9e44adeaf33cbbe66026ae3", "subject": "Artikel onderwerp aangepast", "body": "Artikel inhoud aangepast", "author": "blaat"}'
```


## DELETE /api/v1/article/\<id\>
Artikel verwijderen
Token moet van een user zijn met 'article delete' permissions

input: none

output:
```json
{
  "result": "ok"
}
```

curl example:
```
curl -X DELETE http://localhost:8000/api/v1/article/4 --data '{"token": "d4e9f218e9e44adeaf33cbbe66026ae3"}'
```
