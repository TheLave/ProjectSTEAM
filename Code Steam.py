import json
from tkinter import *
namenlijst_lengte = 1000

with open('steam.json', 'r') as json_file:
    data = json.load(json_file)

def eersteNaam():
    naam_eerste_spel = data[0]["name"]
    eerstenaam_tonen.config(text=f'{naam_eerste_spel}')

def appid_gesorteerd():
    spellen_lijst.delete(0, 'end')
    gesorteerd_prijs = sorted(data[0:namenlijst_lengte], key=lambda i: i['appid'])
    spel_nummer = 0
    while spel_nummer < namenlijst_lengte:
        spellen_lijst.insert(spel_nummer + 1, gesorteerd_prijs[spel_nummer])
        spel_nummer += 1

def prijs_gesorteerd():
    spellen_lijst.delete(0, 'end')
    gesorteerd_prijs = sorted(data[0:namenlijst_lengte], key=lambda i: i['price'])
    spel_nummer = 0
    while spel_nummer < namenlijst_lengte:
        spellen_lijst.insert(spel_nummer + 1, gesorteerd_prijs[spel_nummer])
        spel_nummer += 1

def naam_gesorteerd():
    spellen_lijst.delete(0, 'end')
    gesorteerd_prijs = sorted(data[0:namenlijst_lengte], key=lambda i: i['name'])
    spel_nummer = 0
    while spel_nummer < namenlijst_lengte:
        spellen_lijst.insert(spel_nummer + 1, gesorteerd_prijs[spel_nummer])
        spel_nummer += 1

def datum_gesorteerd():
    spellen_lijst.delete(0, 'end')
    gesorteerd_prijs = sorted(data[0:namenlijst_lengte], key=lambda i: i['release_date'])
    spel_nummer = 0
    while spel_nummer < namenlijst_lengte:
        spellen_lijst.insert(spel_nummer + 1, gesorteerd_prijs[spel_nummer])
        spel_nummer += 1

root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.configure(bg = 'darkblue')

titel = Label(master=root,
              bg="darkblue",
              fg="white",
              text="Steamspellen",
              font=('helvetica', 50, 'bold'))
titel.pack(pady=40)

knop_eerstenaam = Button(master=root,
                          bg='blue2',
                          fg='white',
                          text="Laat eerste spel zien",
                          font=('helvetica', 15, 'bold'),
                         command=eersteNaam)
knop_eerstenaam.pack(pady=10)

eerstenaam_tonen = Label(master=root,
                         bg='darkblue',
                         fg='white',
                         font=('helvetica', 15, 'bold')
                         )
eerstenaam_tonen.pack(pady=10)

knop_gesorteerd_appid = Button(master=root,
                          bg='blue2',
                          fg='white',
                          text="Sorteer spellen op appid",
                          font=('helvetica', 15, 'bold'),
                                 command=appid_gesorteerd
                                 )
knop_gesorteerd_appid.pack()

knop_gesorteerd_naam = Button(master=root,
                          bg='blue2',
                          fg='white',
                          text="Sorteer spellen op naam",
                          font=('helvetica', 15, 'bold'),
                                 command=naam_gesorteerd
                                 )
knop_gesorteerd_naam.pack()

knop_gesorteerd_prijs = Button(master=root,
                          bg='blue2',
                          fg='white',
                          text="Sorteer spellen op prijs",
                          font=('helvetica', 15, 'bold'),
                                 command=prijs_gesorteerd
                                 )
knop_gesorteerd_prijs.pack()

knop_gesorteerd_datum = Button(master=root,
                          bg='blue2',
                          fg='white',
                          text="Sorteer spellen op datum",
                          font=('helvetica', 15, 'bold'),
                                 command=datum_gesorteerd
                                 )
knop_gesorteerd_datum.pack()

spellen_lijst = Listbox(master=root,
                        bg='darkblue',
                        fg='white',
                        bd=20,
                        height= 15,
                        width= 100,
                        font=('helvetica', 15,))
spellen_lijst.pack(pady=10)

root.mainloop()



