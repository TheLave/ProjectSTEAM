# Project STEAM
Hogeschool Utrecht
HBO-ICT jaar 1 (2020-2021)
Blok B

## Projectleden
#### Jeroen Baltjes
Studentnummer: 1782230  
GitHub Username: Lobohuargo822
Meegewerkt aan: BIM sprint 1, AI sprint 2 (statistiek)
#### Cong Hieu Michel Bui
Studentnummer: 1795248  
GitHub Username: Hijeu
Meegewerkt aan: CSC sprint 1, AI sprint 2 (sorteren)
#### Robin Kroesen
Studentnummer: 1779750  
GitHub Username: RobinKroesen
Meegewerkt aan: AI sprint 1, BIM sprint 2
#### Martijn Thiadens
Studentnummer: 1763328  
GitHub Username: TheLave
Meegewerkt aan: AI sprint 1, TI sprint 2
#### Koen van Veldhuisen
Studentnummer: 1786495  
GitHub Username: koen1508
Meegewerkt aan: AI sprint 1, TI sprint 2

## Doel van dit project
Het doel van het 'Project STEAM' is om gamers op het bekende platform [Steam](https://store.steampowered.com/) een grafische weergave aan te bieden van het gaming gedrag van zichzelf en hun vrienden & het zoeken van games te vereenvoudigen. Deze applicatie moet worden ondersteund door een netwerk waarbij gebruik wordt gemaakt van een [RaspberryPi](https://www.raspberrypi.org/).

De gebruiker moet in de applicatie een aantal vragen beantwoord krijgen:
- Welke games spelen mijn vrienden?
- Welke spellen worden het meest gespeeld?
- Wanneer zijn jouw vrienden online?
- Wanneer heb je gepland om te gaan spelen?
- Welke aanbevelingen kunnen er gemaakt worden om te spelen?

## Applicatie instructies
De applicatie bestaat uit het [Python bestand](https://github.com/TheLave/ProjectSTEAM/blob/main/Steam%20GUI.py) en het [JSON bestand](https://github.com/TheLave/ProjectSTEAM/blob/main/steam.json). Het python bestand (Steam_GUI.py) kan worden geopend vanuit PyCharm. Door op het groene play icoontje te klikken of door de keyboard shortcut `SHIFT + F10` in te drukken zal het script uitgevoerd worden.

De applicatie bestaat uit een menubalk met 3 knoppen om 3 verschillende pagina's te openen. De pagina's zijn (respectievelijk van links naar rechts) "Store", "Stats" & "Raspi". 
- Op de "Store" pagina kan de gebruiker alle producten op Steam vinden door het te zoeken op naam in de zoekbalk. 
Daarnaast is het ook mogelijk om deze games te sorteren op meerdere mogelijkheden (release date, rating, naam, prijs & reviews) van hoog naar laag en andersom.
De gevonden producten zijn ook nog eens te filteren op prijs, leeftijd en verschillende tags (genres, operating system & taal)

- Op de "Stats" pagina krijgt de gebruiker te zien wat de gemiddelde speeltijd/gebruikerstijd is van een product in verschillende prijsbereik.
Ook heeft de gebruiker de mogelijkheid om het percentage te zoeken van een genre ten opzichte van de totale aantal producten.

- Op de "Raspi" pagina kan de gebruiker een aantal TI onderdelen gebruiken als aansturing en weergave van de applicatie. Zo zijn de LED lampjes en de Servo te gebruiken als status indicators van een ingevoerd steamid en/of appid. Er is hier informatie over de onlinestatus en achievement progress beschikbaar. Het display en de twee knoppen zijn te gebruiken om van een ingevoerd steamid, informatie op te halen. Hier is informatie als; Username, echte naam, laatste uitlog, online status en land van herkomst.

Via [STEAMID I/O](https://steamid.io/) is een steam account link in te voeren en kan de steamid (steamID64) opgevraagd worden.
Via [SteamDB](https://steamdb.info/apps/) kan een game opgezocht worden en kan de appid opgevraagd worden.
