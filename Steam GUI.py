from tkinter import *
import json


class DataBewerking:
    @staticmethod
    def json_bestand_inlezen():
        with open("steam.json", "r") as json_file:
            return json.load(json_file)

    @staticmethod
    def rating_en_rating_percentage_toevoegen_aan_data(data):
        i = 0

        for product in data:
            aantal_ratings = product["positive_ratings"] + product["negative_ratings"]

            if aantal_ratings != 0:
                rating_percentage = round((product["positive_ratings"] / aantal_ratings) * 100)
            else:
                rating_percentage = 0

            if 95 <= rating_percentage <= 100:
                rating = "Overwhelmingly Positive"
            elif 90 <= rating_percentage <= 94:
                rating = "Very Positive"
            elif 80 <= rating_percentage <= 89:
                rating = "Positive"
            elif 70 <= rating_percentage <= 79:
                rating = "Mostly Positive"
            elif 40 <= rating_percentage <= 69:
                rating = "Mixed"
            elif 30 <= rating_percentage <= 39:
                rating = "Mostly Negative"
            elif 20 <= rating_percentage <= 29:
                rating = "Negative"
            elif 10 <= rating_percentage <= 19:
                rating = "Very Negative"
            elif 0 <= rating_percentage <= 9:
                rating = "Overwhelmingly Negative"

            data[i].update({"rating_percentage": rating_percentage, "rating": rating})
            i += 1


class Sorteren:
    @staticmethod
    def merge_sort(lijst, zoekterm):
        """
        Returnt een gesorteerde lijst van de meegegeven lijst, gesorteert volgens het merge sort algoritme gebaseerd op de meegegeven zoekterm.
        """
        if len(lijst) > 1:
            index_midden_lijst = len(lijst) // 2
            linker_lijst = lijst[:index_midden_lijst]
            rechter_lijst = lijst[index_midden_lijst:]

            # Splitsing van de lijst (Recursief, totdat de sublijsten 1 element bevatten).
            Sorteren.merge_sort(linker_lijst, zoekterm)
            Sorteren.merge_sort(rechter_lijst, zoekterm)

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

    @staticmethod
    def lijst_omkeren(lijst):
        """
        Returnt het omgekeerde van de gegeven lijst.
        """
        omgekeerde_lijst = []
        laatste_index_lijst = len(lijst) - 1

        for i in range(laatste_index_lijst, -1, -1):
            omgekeerde_lijst.append(lijst[i])

        return omgekeerde_lijst

    @staticmethod
    def producten_zoeken_op_naam(data, lijst_temp, zoekterm):
        """
        Zoekt naar producten waarvan de naam overeenkomt met de gegeven zoekterm en returnt een lijst hiervan.
        """
        lijst = []
        lijst_temp.clear()

        for product in data:
            if zoekterm.lower() in product['name'].lower():
                lijst.append(product)
                lijst_temp.append(product)

        return lijst

    @staticmethod
    def lijst_sorteren_op_optie(lijst, opties, waarde):
        """
        Sorteert en returnt de meegegeven lijst gebaseerd op de gekozen "sort by" keuze.
        """
        sortering = waarde.get()

        if sortering == opties[0] or sortering == opties[1]:
            zoekterm = "release_date"
        elif sortering == opties[2] or sortering == opties[3]:
            zoekterm = "name"
        elif sortering == opties[4] or sortering == opties[5]:
            zoekterm = "price"
        elif sortering == opties[6] or sortering == opties[7]:
            zoekterm = "rating_percentage"

        lijst = Sorteren.merge_sort(lijst, zoekterm)
        lijst_omgekeerde_sortering = [opties[0], opties[3], opties[5], opties[6]]

        if sortering in lijst_omgekeerde_sortering:
            lijst = Sorteren.lijst_omkeren(lijst)

        return lijst


class SteamGUI:
    def __init__(self, master, data):
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

        # Constructors nog niet af
        class ScaleStore:
            def __init__(self):
                pass

        class CheckKnopStoreOpties:
            def __init__(self):
                pass

        def applicatie_afsluiten(event):
            master.destroy()

        def inhoud_listbox_aanpassen(lijst):
            """
            Inserts de elementen van de meegegeven lijst in listbox_producten.
            """
            listbox_producten.delete(0, "end")

            maximum_lengte_naam = 40

            for product in lijst:
                listbox_producten.insert("end",
                                         f" {product['name'][:maximum_lengte_naam]:{maximum_lengte_naam}}"
                                         f"{product['release_date']:>16}"
                                         f"{product['rating']:>29}"
                                         f"{product['price']:>11.2f}"
                                         f"€")

        lijst_temp = []

        def getoonde_producten_sorteren(opties, waarde):
            lijst = Sorteren.lijst_sorteren_op_optie(lijst_temp, opties, waarde)
            inhoud_listbox_aanpassen(lijst)

        def producten_tonen(opties, waarde):
            zoekterm = entry_zoekbalk_producten.get()
            lijst = Sorteren.producten_zoeken_op_naam(data, lijst_temp, zoekterm)
            lijst = Sorteren.lijst_sorteren_op_optie(lijst, opties, waarde)
            inhoud_listbox_aanpassen(lijst)

        def geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen):
            for knop in knoppen:
                knop.button.configure(foreground="#a1aab8")

            geklikte_knop.button.configure(foreground="white")

        def applicatie_pagina_tonen(gekozen_pagina, paginas):
            for pagina in paginas:
                pagina.forget()

            gekozen_pagina.pack(fill=BOTH,
                                expand=TRUE)

        def store_scherm_tonen(geklikte_knop, knoppen, gekozen_pagina, paginas):
            geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen)
            applicatie_pagina_tonen(gekozen_pagina, paginas)

            entry_zoekbalk_producten.delete(0, "end")

            producten_tonen(sort_by_opties, sort_by_optionmenu_waarde)

        def knop_1_scherm_tonen(geklikte_knop, knoppen, gekozen_pagina, paginas):
            geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen)
            applicatie_pagina_tonen(gekozen_pagina, paginas)

        def knop_2_scherm_tonen(geklikte_knop, knoppen, gekozen_pagina, paginas):
            geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen)
            applicatie_pagina_tonen(gekozen_pagina, paginas)

        def knop_3_scherm_tonen(geklikte_knop, knoppen, gekozen_pagina, paginas):
            geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen)
            applicatie_pagina_tonen(gekozen_pagina, paginas)

        # Configs
        master.title("Steam")
        master.bind("<Escape>", applicatie_afsluiten)
        master.attributes("-fullscreen", True)

        # Widgets
        hoofdframe = Frame(master=master,
                           background="#1b2837")
        hoofdframe.pack(fill=BOTH,
                        expand=TRUE)

        # Menubalk1
        frame_menubalk1 = FrameMenubalk(hoofdframe)
        knop_applicatie_sluiten = KnopMenubalk1(frame_menubalk1.frame, "x", master.destroy)
        knop_applicatie_minimaliseren = KnopMenubalk1(frame_menubalk1.frame, "-", master.iconify)

        # Menubalk2
        frame_menubalk2 = FrameMenubalk(hoofdframe)
        knop_store = KnopMenubalk2(frame_menubalk2.frame, "STORE", lambda: store_scherm_tonen(knop_store, knoppen_menubalk2, frame_store, applicatie_paginas))
        knop1 = KnopMenubalk2(frame_menubalk2.frame, "KNOP1", lambda: knop_1_scherm_tonen(knop1, knoppen_menubalk2, frame_knop1, applicatie_paginas))
        knop2 = KnopMenubalk2(frame_menubalk2.frame, "KNOP2", lambda: knop_2_scherm_tonen(knop2, knoppen_menubalk2, frame_knop2, applicatie_paginas))
        knop3 = KnopMenubalk2(frame_menubalk2.frame, "KNOP3", lambda: knop_3_scherm_tonen(knop3, knoppen_menubalk2, frame_knop3, applicatie_paginas))

        knoppen_menubalk2 = []
        knoppen_menubalk2.extend([knop_store,
                                  knop1,
                                  knop2,
                                  knop3])

        # Schermen
        # Store scherm
        frame_store = Frame(master=hoofdframe,
                            background="#1b2837")

        frame_store_producten = Frame(master=frame_store,
                                      background="#1b2837")
        frame_store_producten.pack(side=LEFT,
                                   padx=(240, 10))

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
                                         command=lambda: producten_tonen(sort_by_opties, sort_by_optionmenu_waarde))
        knop_zoekbalk_producten.pack(side=LEFT)

        label_sort_by = Label(master=frame_zoekbalk_producten,
                              foreground="#2f475e",
                              background="#101822",
                              text="Sort by",
                              font=("helvetica", 10))
        label_sort_by.pack(side=LEFT,
                           padx=(335, 0))

        sort_by_opties = ["Release Date New",
                          "Release Date Old",
                          "Name A-Z",
                          "Name Z-A",
                          "Lowest Price",
                          "Highest Price",
                          "User Reviews Positive",
                          "User Reviews Negative"]

        sort_by_optionmenu_waarde = StringVar()
        sort_by_optionmenu_waarde.set(sort_by_opties[0])

        optionmenu_sort_by = OptionMenu(frame_zoekbalk_producten,
                                        sort_by_optionmenu_waarde,
                                        *sort_by_opties)
        optionmenu_sort_by.configure(foreground="#63cde8",
                                     activeforeground="white",
                                     background="#213a4a",
                                     activebackground="#4685a7",
                                     font=("helvetica", 10, "bold"),
                                     width=21,
                                     highlightthickness=0)
        optionmenu_sort_by.pack(side=LEFT,
                                padx=10)

        sort_by_optionmenu_waarde.trace("w", lambda i, j, k: getoonde_producten_sorteren(sort_by_opties, sort_by_optionmenu_waarde))

        frame_listbox_producten = Frame(master=frame_store_producten,
                                        background="#1b2837")
        frame_listbox_producten.pack()

        listbox_producten = Listbox(master=frame_listbox_producten,
                                    foreground="#a1aab8",
                                    background="#16202d",
                                    selectbackground="#101821",
                                    height=48,
                                    width=99,
                                    font=("monaco", 12))
        listbox_producten.pack(side=LEFT)

        scroll_bar_y_listbox_producten = Scrollbar(master=frame_listbox_producten,
                                                   command=listbox_producten.yview)
        scroll_bar_y_listbox_producten.pack(side=RIGHT,
                                            fill=Y)

        listbox_producten.configure(yscrollcommand=scroll_bar_y_listbox_producten.set)

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

        # Applicatie Pagina's
        applicatie_paginas = []
        applicatie_paginas.extend([frame_store,
                                   frame_knop1,
                                   frame_knop2,
                                   frame_knop3])

        # Store tonen bij het opstarten van de applicatie.
        store_scherm_tonen(knop_store, knoppen_menubalk2, frame_store, applicatie_paginas)


def main():
    data = DataBewerking.json_bestand_inlezen()
    DataBewerking.rating_en_rating_percentage_toevoegen_aan_data(data)

    root = Tk()
    steam_gui = SteamGUI(root, data)
    root.mainloop()


if __name__ == "__main__":
    main()

# To do:
        # Zorgen dat listbox bij default alle producten toont gesorteerd op rating                                                                   DONE
        # - Dropdown menu for Sort by                                                                                                                    DONE
        # - Scale for maximum price
        # - Scale for minimum price
        # - Scale for required_age
        # - Check buttons for platforms
        # - Check buttons for steamspy_tags
        # - Check buttons for genres
        # - Check button for language "English"
        # - Rating system                                                                                                                                DONE
                # Functie schrijven om ratingspercentage van producten toe te voegen aan de data                                                         DONE
                # ratingspercentage koppelen aan rating en toevoegen aan data(Overwhelmingly positive, Positive, Mixed, Mostly Negative, etc...          DONE
                # Rating tonen bij zoeken van producten                                                                                                  DONE