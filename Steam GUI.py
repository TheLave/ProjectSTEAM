from tkinter import *
import json


class FrameMenubalk:
    def __init__(self, master):
        self.frame = Frame(master=master,
                           background="#202224")
        self.frame.pack(fill=X)


class KnopMenubalk1:
    def __init__(self, master, text, command):
        self.button = Button(master=master,
                             foreground="#a1aab8",
                             activeforeground="#c4ccd8",
                             background="#202224",
                             activebackground="#202224",
                             borderwidth=0,
                             text=text,
                             font=("helvetica", 12, "bold"),
                             command=command)
        self.button.pack(side=RIGHT,
                         padx=15)


class KnopMenubalk2:
    def __init__(self, master, text, command):
        self.button = Button(master=master,
                             foreground="#a1aab8",
                             activeforeground="#c4ccd8",
                             background="#202224",
                             activebackground="#202224",
                             borderwidth=0,
                             text=text,
                             font=("helvetica", 18),
                             command=command)
        self.button.pack(side=LEFT,
                         padx=10,
                         pady=2)


# Constructor nog niet af
class CheckKnopStoreOpties:
    def __init__(self):
        pass


class SteamGUI:
    def __init__(self, master):
        data = json_bestand_inlezen()

        def product_zoeken():
            """
            Zoekt naar producten waarvan de naam overeenkomt met de gegeven zoekterm.
            """
            listbox_producten.delete(0, "end")

            zoekterm = entry_zoekbalk_producten.get()
            maximum_lengte_naam = 40

            for game in range(len(data)):
                if zoekterm.lower() in data[game]['name'].lower():
                    listbox_producten.insert("end",
                                             f"{data[game]['name'][:maximum_lengte_naam]:{maximum_lengte_naam}}    "
                                             f"{data[game]['release_date']:<14}"
                                             f"{data[game]['price']:>7.2f}")

        def store_scherm_tonen():
            knop_store.button.configure(foreground="white")
            knop1.button.configure(foreground="#a1aab8")
            knop2.button.configure(foreground="#a1aab8")
            knop3.button.configure(foreground="#a1aab8")

            frame_knop1.forget()
            frame_knop2.forget()
            frame_knop3.forget()
            frame_store.pack(fill=BOTH,
                             expand=TRUE)

        def knop_1_scherm_tonen():
            knop1.button.configure(foreground="white")
            knop2.button.configure(foreground="#a1aab8")
            knop3.button.configure(foreground="#a1aab8")
            knop_store.button.configure(foreground="#a1aab8")

            frame_knop2.forget()
            frame_knop3.forget()
            frame_store.forget()
            frame_knop1.pack(fill=BOTH,
                             expand=TRUE)

        def knop_2_scherm_tonen():
            knop2.button.configure(foreground="white")
            knop1.button.configure(foreground="#a1aab8")
            knop3.button.configure(foreground="#a1aab8")
            knop_store.button.configure(foreground="#a1aab8")

            frame_knop1.forget()
            frame_knop3.forget()
            frame_store.forget()
            frame_knop2.pack(fill=BOTH,
                             expand=TRUE)

        def knop_3_scherm_tonen():
            knop3.button.configure(foreground="white")
            knop1.button.configure(foreground="#a1aab8")
            knop2.button.configure(foreground="#a1aab8")
            knop_store.button.configure(foreground="#a1aab8")

            frame_knop1.forget()
            frame_knop2.forget()
            frame_store.forget()
            frame_knop3.pack(fill=BOTH,
                             expand=TRUE)


# Configs
        master.title("Steam")
        master.bind("<Escape>", master.destroy)
        master.attributes("-fullscreen", True)

# Widgets
        hoofdframe = Frame(master=master,
                           background="#1b2837")
        hoofdframe.pack(fill=BOTH,
                        expand=TRUE)

        # Menubalk1
        frame_menubalk1 = FrameMenubalk(hoofdframe)
        knop_programma_sluiten = KnopMenubalk1(frame_menubalk1.frame, "x", master.quit)
        knop_programma_minimaliseren = KnopMenubalk1(frame_menubalk1.frame, "-", master.iconify)

        # Menubalk2
        frame_menubalk2 = FrameMenubalk(hoofdframe)
        knop_store = KnopMenubalk2(frame_menubalk2.frame, "STORE", store_scherm_tonen)
        knop1 = KnopMenubalk2(frame_menubalk2.frame, "KNOP1", knop_1_scherm_tonen)
        knop2 = KnopMenubalk2(frame_menubalk2.frame, "KNOP2", knop_2_scherm_tonen)
        knop3 = KnopMenubalk2(frame_menubalk2.frame, "KNOP3", knop_3_scherm_tonen)

    # Schermen
        # Store scherm
        frame_store = Frame(master=hoofdframe,
                            background="#1b2837")

        frame_store_producten = Frame(master=frame_store,
                                      background="#1b2837")
        frame_store_producten.pack(side=LEFT,
                                   padx=(450, 10))

        frame_zoekbalk_producten = Frame(master=frame_store_producten,
                                         background="#101822")
        frame_zoekbalk_producten.pack(padx=10,
                                      pady=10)

        entry_zoekbalk_producten = Entry(master=frame_zoekbalk_producten,
                                         foreground="white",
                                         background="#213a4a",
                                         width=30,
                                         font=("helvetica", 14))
        entry_zoekbalk_producten.pack(side=LEFT,
                                      padx=7,
                                      pady=10)

        knop_zoekbalk_producten = Button(master=frame_zoekbalk_producten,
                                         foreground="#63cde8",
                                         activeforeground="white",
                                         background="#213a4a",
                                         activebackground="#4685a7",
                                         width=8,
                                         text="Search",
                                         font=("helvetica", 10, "bold"),
                                         command=product_zoeken)
        knop_zoekbalk_producten.pack(side=LEFT)

        label_sort_by = Label(master=frame_zoekbalk_producten,
                              foreground="#2f475e",
                              background="#101822",
                              text="Sort by",
                              font=("helvetica", 10))
        label_sort_by.pack(side=RIGHT,
                           padx=(100, 10))

        # menu_sort_by = ...
        # menu_sort_by.pack()

        listbox_producten = Listbox(master=frame_store_producten,
                                    foreground="#a1aab8",
                                    background="#1b2837",
                                    border=0,
                                    height=48,
                                    width=80,
                                    font=("monaco", 12))
        listbox_producten.pack(padx=20)

        frame_store_opties = Frame(master=frame_store,
                                   background="#1b2837")
        frame_store_opties.pack(side=RIGHT)

        # Knop1 scherm
        frame_knop1 = Frame(master=hoofdframe,
                            background="green")

        # Knop2 scherm
        frame_knop2 = Frame(master=hoofdframe,
                            background="blue")

        # Knop3 scherm
        frame_knop3 = Frame(master=hoofdframe,
                            background="yellow")

        # To do:
        # Zorgen dat listbox bij default alle games heeft (bij voorkeur gesorteerd op rating)
        # - Dropdown menu for Sort by
                # Release Date (misschien ook inverted, dus van nieuw-oud)
                # Name (misschien ook inverted, dus van z-a)
                # Lowest Price
                # Highest Price
                # User Reviews (= rating, zie rating system & en misschien ook inverted)
        # - Scale for maximum price
        # - Scale for minimum price
        # - Scale for required_age
        # - Check buttons for platforms
        # - Check buttons for steamspy_tags
        # - Check buttons for genres
        # - Check button for language "English"
        # - Rating system
                # Ratingspercentage berekenen door (positive_ratings / negative_ratings) * 100
                # Ratingspercentage koppelen aan rating (Overwhelmingly positive, Positive, Mixed, Mostly Negative, etc...
                    # https://www.gamasutra.com/blogs/LarsDoucet/20141006/227162/Fixing_Steams_User_Rating_Charts.php#:~:text=94%20-%2080%25%20%3A%20Very%20Positive,40%20-%2069%25%20%3A%20Mixed
                # Rating weergeven bij zoeken van games


def json_bestand_inlezen():
    with open("steam.json", "r") as json_file:
        return json.load(json_file)


def mergesort(lijst, zoekterm):
    """
    Sorteert volgens het mergesort algoritme de meegegeven lijst gebaseerd op de meegegeven zoekterm.
    """
    if len(lijst) > 1:
        index_midden_lijst = len(lijst) // 2
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


def main():
    root = Tk()
    steam_gui = SteamGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
