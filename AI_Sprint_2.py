import json
from tkinter import *

with open("steam.json", "r") as json_file:
    data = json.load(json_file)


def programma_sluiten(event):
    """
    Sluit het programma af.
    """
    root.destroy()


def eerste_spel_tonen():
    """
    Toont in de GUI het eerste spel dat op Steam is gepubliceerd.
    """
    eerste_spel = data[0]["name"]

    naam_eerste_spel.config(text=f'{eerste_spel}')


def mergesort(lijst, zoekterm):
    """
    Sorteert volgens het mergesort algoritme de meegegeven lijst gebaseerd op de meegegeven zoekterm.
    """
    if len(lijst) > 1:
        aantal_games = len(lijst)
        index_midden_lijst = aantal_games // 2
        linker_lijst = lijst[:index_midden_lijst]
        rechter_lijst = lijst[index_midden_lijst:]

        # Splitsing van de lijst (Recursief, totdat de sublijsten 1 element bevatten).
        mergesort(linker_lijst, zoekterm)
        mergesort(rechter_lijst, zoekterm)

        # Merge gedeelte van de functie.
        i = j = k = 0

        while i < len(linker_lijst) and j < len(rechter_lijst):
            if linker_lijst[i][zoekterm] < rechter_lijst[j][zoekterm]:
                lijst[k] = linker_lijst[i]
                i += 1
            else:
                lijst[k] = rechter_lijst[j]
                j += 1
            k += 1

        while i < len(linker_lijst):
            lijst[k] = linker_lijst[i]
            i += 1
            k += 1

        while j < len(rechter_lijst):
            lijst[k] = rechter_lijst[j]
            j += 1
            k += 1

    return lijst


def sorteren(zoekterm):
    """
    Insert de gesorteerde lijst in de Listbox van de GUI.
    """
    aantal_spellen = len(data)

    gesorteerde_weergave.delete(0, "end")
    gesorteerd = mergesort(data, zoekterm)

    spel_nummer = 0

    while spel_nummer < aantal_spellen:
        gesorteerde_weergave.insert("end", "naam: {:<80} appid:{:<} prijs:${:<} datum van uitgave:{:<}".format(gesorteerd[spel_nummer]['name'],
                gesorteerd[spel_nummer]['appid'],gesorteerd[spel_nummer]['price'], gesorteerd[spel_nummer]['release_date'] ))
        spel_nummer += 1

def zoek_balk():
    """
    Een functie om naar een specifiek items in de JSON lijst te zoeken
    """
    target = target_entry.get()
    for i in range(len(data)):
        if target.lower() in data[i]['name'].lower():
          gesorteerde_weergave.insert("end", "naam: {:35} appid:{:<5} prijs: ${:<10} datum van uitgave: {:}".format(data[i]['name'],
                    data[i]['appid'],data[i]['price'], data[i]['release_date'] ))
        
# GUI (Tkinter)
root = Tk()

root.bind("<Escape>", programma_sluiten)

root.attributes("-fullscreen", True)

root.configure(background="darkblue")

frame = Frame(master=root)

titel = Label(master=root,
              background="darkblue",
              foreground="white",
              text="Steamspellen",
              font=("helvetica", 50, "bold"))



zoek_balk_knop = Button(master=root,
                        text="zoeken",
                        command= zoek_balk)

target_entry = Entry(master=root)

zoek_balk_knop.pack()
target_entry.pack()




titel = Label(master=root,
              background="darkblue",
              foreground="white",
              text="Steamspellen",
              font=("helvetica", 50, "bold"))

naam_eerste_spel = Label(master=root,
                         background="darkblue",
                         foreground="white",
                         font=("helvetica", 15, "bold"))

knop_eerste_spel = Button(master=root,
                          background="blue2",
                          foreground="white",
                          text="Laat eerste spel zien",
                          font=("helvetica", 15, "bold"),
                          command=eerste_spel_tonen)

knop_sorteren_op_appid = Button(master=root,
                                background="blue2",
                                foreground="white",
                                text="Sorteer spellen op appid",
                                font=("helvetica", 15, "bold"),
                                command=lambda: sorteren("appid"))

knop_sorteren_op_naam = Button(master=root,
                               background="blue2",
                               foreground="white",
                               text="Sorteer spellen op naam",
                               font=("helvetica", 15, "bold"),
                               command=lambda: sorteren("name"))

knop_sorteren_op_prijs = Button(master=root,
                                background="blue2",
                                foreground="white",
                                text="Sorteer spellen op prijs",
                                font=("helvetica", 15, "bold"),
                                command=lambda: sorteren("price"))

knop_sorteren_op_datum = Button(master=root,
                                background="blue2",
                                foreground="white",
                                text="Sorteer spellen op datum",
                                font=("helvetica", 15, "bold"),
                                command=lambda: sorteren("release_date"))

gesorteerde_weergave = Listbox(master=frame,
                               background="darkblue",
                               foreground="white",
                               border=20,
                               height=15,
                               width=100,
                               font=("helvetica", 15,))

scroll_bar_y = Scrollbar(frame)
scroll_bar_x = Scrollbar(frame, orient=HORIZONTAL)

gesorteerde_weergave.config(yscrollcommand=scroll_bar_y.set)
scroll_bar_y.config(command=gesorteerde_weergave.yview)
gesorteerde_weergave.config(xscrollcommand=scroll_bar_x.set)
scroll_bar_x.config(command=gesorteerde_weergave.xview)

scroll_bar_y.pack(side="right", fill="y")
scroll_bar_x.pack(side="bottom", fill="x")
titel.pack(pady=40)
naam_eerste_spel.pack(pady=10)
knop_eerste_spel.pack(pady=10)
knop_sorteren_op_appid.pack()
knop_sorteren_op_naam.pack()
knop_sorteren_op_prijs.pack()
knop_sorteren_op_datum.pack()
frame.pack()
gesorteerde_weergave.pack()

root.mainloop()