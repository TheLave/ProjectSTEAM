# Project STEAM

## Doel van dit project
Het doel van het 'Project STEAM' is om gamers op het bekende platform [Steam](https://store.steampowered.com/) een grafische weergave aan te bieden van het gaming gedrag van zichzelf en hun vrienden. Deze applicatie moet worden ondersteund door een netwerk waarbij gebruik wordt gemaakt van een [RaspberryPi](https://www.raspberrypi.org/).

De gebruiker moet in de applicatie een aantal vragen beantwoord krijgen:
- Welke games spelen mijn vrienden?
- Welke spellen worden het meest gespeeld?
- Wanneer zijn jouw vrienden online?
- Wanneer heb je gepland om te gaan spelen?
- Welke aanbevelingen kunnen er gemaakt worden om te spelen?

## Projectleden
### Jeroen Baltjes
Studentnummer: 1782230  
GitHub Username: Lobohuargo822
### Hieu Bui
Studentnummer: 1795248  
GitHub Username: Hijeu
### Robin Kroesen
Studentnummer: 1779750  
GitHub Username: RobinKroesen
### Martijn Thiadens
Studentnummer: 1763328  
GitHub Username: TheLave
### Koen van Veldhuisen
Studentnummer: 1786495  
GitHub Username: koen1508

## Applicatie instructies
De applicatie bestaat uit het [Python bestand](https://github.com/TheLave/ProjectSTEAM/blob/main/Code%20Steam.py) en het [JSON bestand](https://github.com/TheLave/ProjectSTEAM/blob/main/steam.json). Het python bestand (Code_Steam.py) kan worden geopend vanuit PyCharm. Door op het groene play icoontje te klikken of door de keyboard shortcut `SHIFT + F10` in te drukken zal het script uitgevoerd worden.

De applicatie bestaat uit het homescherm en 5 knoppen. De bovenste knop laat de naam van het eerste spel in het JSON bestand zien. De andere knoppen sorteren het gehele bestand respectievelijk (van boven naar beneden in de applicatie) op: appid, naam, prijs en datum.

Er kan een regel aangeklikt worden om deze te highlighten. De applicatie heeft een verticale en horizontale scrollbar om de gehele regels te kunnen lezen. Elke regel bevat informatie over slechts één spel.
