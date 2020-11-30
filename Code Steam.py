import json
from tkinter import *
namenlijst_lengte = 1000

with open('steam.json', 'r') as json_file:
    data = json.load(json_file)


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


root = Tk()
frame = Frame(root)

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.configure(bg='darkblue')

titel =            Label(master=root,
                         bg="darkblue",
                         fg="white",
                         text="Steamspellen",
                         font=('helvetica', 50, 'bold'))

eerstenaam_tonen = Label(master=root,
                         bg='darkblue',
                         fg='white',
                         font=('helvetica', 15, 'bold'))


knop_eerstenaam =       Button(master=root,
                               bg='blue2',
                               fg='white',
                               text="Laat eerste spel zien",
                               font=('helvetica', 15, 'bold'),
                               command=eersteNaam)

knop_gesorteerd_appid = Button(master=root,
                               bg='blue2',
                               fg='white',
                               text="Sorteer spellen op appid",
                               font=('helvetica', 15, 'bold'),
                               command=lambda: gesorteerd('appid'))

knop_gesorteerd_naam =  Button(master=root,
                               bg='blue2',
                               fg='white',
                               text="Sorteer spellen op naam",
                               font=('helvetica', 15, 'bold'),
                               command=lambda: gesorteerd('name'))

knop_gesorteerd_prijs = Button(master=root,
                               bg='blue2',
                               fg='white',
                               text="Sorteer spellen op prijs",
                               font=('helvetica', 15, 'bold'),
                               command=lambda: gesorteerd('price'))

knop_gesorteerd_datum = Button(master=root,
                               bg='blue2',
                               fg='white',
                               text="Sorteer spellen op datum",
                               font=('helvetica', 15, 'bold'),
                               command=lambda: gesorteerd('release_date'))


spellen_lijst = Listbox(master=frame,
                        bg='darkblue',
                        fg='white',
                        bd=20,
                        height= 15,
                        width= 100,
                        font=('helvetica', 15,))

scroll_bar = Scrollbar(frame)
scroll_barx = Scrollbar(frame, orient=HORIZONTAL)

spellen_lijst.config(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=spellen_lijst.yview)
spellen_lijst.config(xscrollcommand=scroll_barx.set)
scroll_barx.config(command=spellen_lijst.xview)

scroll_bar.pack(side="right", fill=Y)
scroll_barx.pack(side="bottom", fill='x')
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



