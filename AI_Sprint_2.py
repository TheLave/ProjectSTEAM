import json
from tkinter import *

namenlijst_lengte = 1000

with open('steam.json', 'r') as json_file:
    data = json.load(json_file)


def programma_sluiten(event):
    root.destroy()


def eersteNaam():
    naam_eerste_spel = data[0]["name"]
    eerstenaam_tonen.config(text=f'{naam_eerste_spel}')


def gesorteerd(sort):
    spellen_lijst.delete(0, 'end')
    gesorteerd = sorted(data[0:namenlijst_lengte], key=lambda i: i[sort])
    spel_nummer = 0

    while spel_nummer < namenlijst_lengte:
        spellen_lijst.insert(spel_nummer + 1, gesorteerd[spel_nummer])
        spel_nummer += 1


# GUI (Tkinter)
root = Tk()

root.bind('<Escape>', programma_sluiten)

root.attributes("-fullscreen", True)

root.configure(background="darkblue")

frame = Frame(master=root)

titel = Label(master=root,
              background="darkblue",
              foreground="white",
              text="Steamspellen",
              font=("helvetica", 50, "bold"))

eerstenaam_tonen = Label(master=root,
                         background="darkblue",
                         foreground="white",
                         font=("helvetica", 15, "bold"))

knop_eerstenaam = Button(master=root,
                         background="blue2",
                         foreground="white",
                         text="Laat eerste spel zien",
                         font=("helvetica", 15, "bold"),
                         command=eersteNaam)

knop_gesorteerd_appid = Button(master=root,
                               background="blue2",
                               foreground="white",
                               text="Sorteer spellen op appid",
                               font=("helvetica", 15, "bold"),
                               command=lambda: gesorteerd("appid"))

knop_gesorteerd_naam =  Button(master=root,
                               background="blue2",
                               foreground="white",
                               text="Sorteer spellen op naam",
                               font=("helvetica", 15, "bold"),
                               command=lambda: gesorteerd("name"))

knop_gesorteerd_prijs = Button(master=root,
                               background="blue2",
                               foreground="white",
                               text="Sorteer spellen op prijs",
                               font=("helvetica", 15, "bold"),
                               command=lambda: gesorteerd("price"))

knop_gesorteerd_datum = Button(master=root,
                               background="blue2",
                               foreground="white",
                               text="Sorteer spellen op datum",
                               font=("helvetica", 15, "bold"),
                               command=lambda: gesorteerd("release_date"))

spellen_lijst = Listbox(master=frame,
                        background="darkblue",
                        foreground="white",
                        border=20,
                        height=15,
                        width=100,
                        font=("helvetica", 15,))

scroll_bar_y = Scrollbar(frame)
scroll_bar_x = Scrollbar(frame, orient=HORIZONTAL)

spellen_lijst.config(yscrollcommand=scroll_bar_y.set)
scroll_bar_y.config(command=spellen_lijst.yview)
spellen_lijst.config(xscrollcommand=scroll_bar_x.set)
scroll_bar_x.config(command=spellen_lijst.xview)

scroll_bar_y.pack(side="right", fill="y")
scroll_bar_x.pack(side="bottom", fill="x")
titel.pack(pady=40)
eerstenaam_tonen.pack(pady=10)
knop_eerstenaam.pack(pady=10)
knop_gesorteerd_appid.pack()
knop_gesorteerd_naam.pack()
knop_gesorteerd_prijs.pack()
knop_gesorteerd_datum.pack()
frame.pack()
spellen_lijst.pack()

root.mainloop()

