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
    def producten_zoeken_op_naam(data, lijst, zoekterm):
        """
        Zoekt naar producten waarvan de naam overeenkomt met de gegeven zoekterm en returnt een lijst hiervan.
        """
        lijst.clear()

        for product in data:
            if zoekterm.lower() in product['name'].lower():
                lijst.append(product)

        return lijst

    @staticmethod
    def lijst_sorteren_op_optie(lijst, opties, waarde):
        """
        Sorteert en returnt de meegegeven lijst gebaseerd op de gekozen "sort by" keuze.
        """
        sortering = waarde

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

        def producten_filteren_op_price(lijst):
            gefilterde_prijs = scale_filter_price.scale.get()
            gefilterde_lijst = []

            if gefilterde_prijs == maximum_price:
                label_gefilterde_price.label.configure(text="Any Price")
            elif gefilterde_prijs == 0:
                label_gefilterde_price.label.configure(text=f"Free")
            else:
                label_gefilterde_price.label.configure(text=f"€{gefilterde_prijs},- & under")

            if gefilterde_prijs == maximum_price:
                return lijst
            else:
                for product in lijst:
                    if product["price"] <= gefilterde_prijs:
                        gefilterde_lijst.append(product)
                return gefilterde_lijst

        def producten_filteren_op_age(lijst):
            gefilterde_leeftijd = scale_filter_age.scale.get()
            gefilterde_lijst = []

            if gefilterde_leeftijd == 18:
                label_gefilterde_age.label.configure(text="18+")

                for product in lijst:
                    if product["required_age"] == 18:
                        gefilterde_lijst.append(product)
            else:
                if gefilterde_leeftijd == 0:
                    label_gefilterde_age.label.configure(text="Any Age")
                else:
                    label_gefilterde_age.label.configure(text=f"{gefilterde_leeftijd} & under")

                for product in lijst:
                    if product["required_age"] <= gefilterde_leeftijd:
                        gefilterde_lijst.append(product)

            return gefilterde_lijst

        def geklikte_checkknop_highlighten(checkknop):
            state = checkknop.var.get()

            if state == 1:
                checkknop.checkbutton.configure(activebackground=babyblauw,
                                                background=babyblauw,
                                                activeforeground="white",
                                                foreground="white",
                                                selectcolor=babyblauw)
            else:
                checkknop.checkbutton.configure(activebackground=blauw,
                                                background=blauw,
                                                activeforeground=blauw3,
                                                foreground=blauw3,
                                                selectcolor=blauw)

        def producten_filteren_op_tag(lijst, checkknop, tag):
            geklikte_checkknop_highlighten(checkknop)

            state = checkknop.var.get()
            gefilterde_lijst = []

            if state == 1:
                for product in lijst:
                    if tag in product["categories"] \
                            or tag in product["genres"] \
                            or tag in product["steamspy_tags"] \
                            or tag.lower() in product["platforms"]:
                        gefilterde_lijst.append(product)
                return gefilterde_lijst
            else:
                return lijst

        def producten_filteren_op_language(lijst, checkknop):
            geklikte_checkknop_highlighten(checkknop)

            state = checkknop.var.get()
            gefilterde_lijst = []

            if state == 1:
                for product in lijst:
                    if product["english"] == 1:
                        gefilterde_lijst.append(product)
                return gefilterde_lijst
            else:
                return lijst

        lijst_temp = []

        def getoonde_producten_sorteren_en_filteren():
            lijst = Sorteren.lijst_sorteren_op_optie(lijst_temp, sort_by_opties, sort_by_optionmenu_waarde.get())
            lijst = producten_filteren_op_price(lijst)
            lijst = producten_filteren_op_age(lijst)
            lijst = producten_filteren_op_language(lijst, checkbutton_tags_english)

            for checkbutton in checkbuttons:
                lijst = producten_filteren_op_tag(lijst, checkbutton, checkbutton.checkbutton["text"])

            inhoud_listbox_aanpassen(lijst)

        def producten_tonen():
            zoekterm = entry_zoekbalk_producten.get()

            Sorteren.producten_zoeken_op_naam(data, lijst_temp, zoekterm)
            getoonde_producten_sorteren_en_filteren()

        def geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen):
            for knop in knoppen:
                knop.button.configure(foreground=lichtgrijs)

            geklikte_knop.button.configure(foreground="white")

        def applicatie_pagina_tonen(gekozen_pagina, paginas):
            for pagina in paginas:
                pagina.forget()

            gekozen_pagina.pack(fill=BOTH,
                                expand=TRUE)

        def store_scherm_tonen(geklikte_knop, gekozen_pagina):
            geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen_menubalk2)
            applicatie_pagina_tonen(gekozen_pagina, applicatie_paginas)

            sort_by_optionmenu_waarde.set(sort_by_opties[0])

            entry_zoekbalk_producten.delete(0, "end")
            scale_filter_price.scale.set(maximum_price)
            scale_filter_age.scale.set(0)

            for tag in filter_tags:
                tag.checkbutton.deselect()
                tag.checkbutton.configure(activebackground=blauw,
                                          background=blauw,
                                          activeforeground=blauw3,
                                          foreground=blauw3,
                                          selectcolor=blauw)

            producten_tonen()

        def knop_1_scherm_tonen(geklikte_knop, gekozen_pagina):
            geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen_menubalk2)
            applicatie_pagina_tonen(gekozen_pagina, applicatie_paginas)

        def knop_2_scherm_tonen(geklikte_knop, gekozen_pagina):
            geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen_menubalk2)
            applicatie_pagina_tonen(gekozen_pagina, applicatie_paginas)

        def knop_3_scherm_tonen(geklikte_knop, gekozen_pagina):
            geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen_menubalk2)
            applicatie_pagina_tonen(gekozen_pagina, applicatie_paginas)

        class FrameMenubalk:
            def __init__(self, master):
                self.frame = Frame(master=master,
                                   background=donkergrijs)
                self.frame.pack(fill=X)

        class KnopMenubalk1:
            def __init__(self, master, text, command):
                self.button = Button(master=master,
                                     foreground=lichtgrijs,
                                     activeforeground="white",
                                     background=donkergrijs,
                                     activebackground=donkergrijs,
                                     borderwidth=0,
                                     text=text,
                                     font=("helvetica", 12, "bold"),
                                     command=command)
                self.button.pack(side=RIGHT,
                                 padx=15)

        class KnopMenubalk2:
            def __init__(self, master, text, command):
                self.button = Button(master=master,
                                     foreground=lichtgrijs,
                                     activeforeground="white",
                                     background=donkergrijs,
                                     activebackground=donkergrijs,
                                     borderwidth=0,
                                     text=text,
                                     font=("helvetica", 18),
                                     command=command)
                self.button.pack(side=LEFT,
                                 padx=10,
                                 pady=2)
                knoppen_menubalk2.append(self)

        class FrameFilter:
            def __init__(self, master):
                self.frame = Frame(master=master,
                                   background=blauw,
                                   relief=RIDGE,
                                   borderwidth=1)
                self.frame.pack(pady=(0, 20))

        class LabelFilter:
            def __init__(self, master, foreground, background, text, anchor, pady):
                self.label = Label(master=master,
                                   foreground=foreground,
                                   background=background,
                                   width=30,
                                   text=text,
                                   font=("helvetica", 10),
                                   anchor=anchor)
                self.label.pack(pady=pady)

        class ScaleStore:
            def __init__(self, master, to, command):
                self.scale = Scale(master=master,
                                   troughcolor=babyblauw,
                                   from_=0,
                                   to=to,
                                   length=200,
                                   width=10,
                                   sliderlength=20,
                                   borderwidth=0,
                                   showvalue=0,
                                   orient=HORIZONTAL,
                                   command=command)
                self.scale.set(to)
                self.scale.pack(pady=(15, 0))

        class CheckKnopStoreOpties:
            def __init__(self, master, text, command):
                self.var = IntVar()
                self.checkbutton = Checkbutton(master=master,
                                               width=26,
                                               activebackground=blauw,
                                               background=blauw,
                                               activeforeground=blauw3,
                                               foreground=blauw3,
                                               selectcolor=blauw,
                                               text=text,
                                               font=("helvetica", 10),
                                               variable=self.var,
                                               command=command)
                self.checkbutton.pack()
                filter_tags.append(self)

# Kleurencodes
        navy = "#101822"
        donkerblauw = "#16202d"
        blauw = "#1b2837"
        blauw2 = "#213a4a"
        blauw3 = "#6d8ea4"
        lichtblauw = "#4685a7"
        babyblauw = "#63cde8"
        donkergrijs = "#202224"
        lichtgrijs = "#a1aab8"
        grijs = "#323e4b"

# Configs
        master.title("Steam")
        master.bind("<Escape>", applicatie_afsluiten)
        master.attributes("-fullscreen", True)

# Widgets
        hoofdframe = Frame(master=master,
                           background=blauw)
        hoofdframe.pack(fill=BOTH,
                        expand=TRUE)

    # Menubalken
        # Menubalk1
        frame_menubalk1 = FrameMenubalk(hoofdframe)
        knop_applicatie_sluiten = KnopMenubalk1(frame_menubalk1.frame, "x", master.destroy)
        knop_applicatie_minimaliseren = KnopMenubalk1(frame_menubalk1.frame, "-", master.iconify)

        # Menubalk2
        frame_menubalk2 = FrameMenubalk(hoofdframe)
        knoppen_menubalk2 = []
        knop_store = KnopMenubalk2(frame_menubalk2.frame, "STORE", lambda: store_scherm_tonen(knop_store, frame_store))
        knop1 = KnopMenubalk2(frame_menubalk2.frame, "KNOP1", lambda: knop_1_scherm_tonen(knop1, frame_knop1))
        knop2 = KnopMenubalk2(frame_menubalk2.frame, "KNOP2", lambda: knop_2_scherm_tonen(knop2, frame_knop2))
        knop3 = KnopMenubalk2(frame_menubalk2.frame, "KNOP3", lambda: knop_3_scherm_tonen(knop3, frame_knop3))

    # Applicatie pagina's
        applicatie_paginas = []

        # Store scherm
        frame_store = Frame(master=hoofdframe,
                            background=blauw)

        frame_store_producten = Frame(master=frame_store,
                                      background=blauw)
        frame_store_producten.pack(side=LEFT,
                                   padx=(240, 10))

        # Knop1 scherm
        frame_knop1 = Frame(master=hoofdframe,
                            background="green")

        # Knop2 scherm
        frame_knop2 = Frame(master=hoofdframe,
                            background="blue")

        # Knop3 scherm
        frame_knop3 = Frame(master=hoofdframe,
                            background="yellow")

        applicatie_paginas.extend([frame_store,
                                   frame_knop1,
                                   frame_knop2,
                                   frame_knop3])

            # Widgets op Store pagina
                # Zoekbalk
        frame_zoekbalk_producten = Frame(master=frame_store_producten,
                                         background=navy)
        frame_zoekbalk_producten.pack(padx=10,
                                      pady=10)

        entry_zoekbalk_producten = Entry(master=frame_zoekbalk_producten,
                                         foreground="white",
                                         background=blauw2,
                                         width=30,
                                         font=("helvetica", 14))
        entry_zoekbalk_producten.pack(side=LEFT,
                                      padx=7,
                                      pady=10)

        knop_zoekbalk_producten = Button(master=frame_zoekbalk_producten,
                                         foreground=babyblauw,
                                         activeforeground="white",
                                         background=blauw2,
                                         activebackground=lichtblauw,
                                         width=8,
                                         text="Search",
                                         font=("helvetica", 10, "bold"),
                                         command=producten_tonen)
        knop_zoekbalk_producten.pack(side=LEFT)

        master.bind("<Return>", lambda *args: producten_tonen())

                # Sort by
        label_sort_by = Label(master=frame_zoekbalk_producten,
                              foreground=grijs,
                              background=navy,
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
        sort_by_optionmenu_waarde.trace("w", lambda *args: getoonde_producten_sorteren_en_filteren())

        optionmenu_sort_by = OptionMenu(frame_zoekbalk_producten,
                                        sort_by_optionmenu_waarde,
                                        *sort_by_opties)
        optionmenu_sort_by.configure(foreground=babyblauw,
                                     activeforeground="white",
                                     background=blauw2,
                                     activebackground=lichtblauw,
                                     font=("helvetica", 10, "bold"),
                                     width=21,
                                     highlightthickness=0)
        optionmenu_sort_by.pack(side=LEFT,
                                padx=10)



                # Listbox
        frame_listbox_producten = Frame(master=frame_store_producten,
                                        background=blauw)
        frame_listbox_producten.pack()

        listbox_producten = Listbox(master=frame_listbox_producten,
                                    foreground=lichtgrijs,
                                    background=donkerblauw,
                                    selectbackground=navy,
                                    height=48,
                                    width=99,
                                    font=("monaco", 12))
        listbox_producten.pack(side=LEFT)

        scroll_bar_y_listbox_producten = Scrollbar(master=frame_listbox_producten,
                                                   command=listbox_producten.yview)
        scroll_bar_y_listbox_producten.pack(side=RIGHT,
                                            fill=Y)

        listbox_producten.configure(yscrollcommand=scroll_bar_y_listbox_producten.set)

                # Filters
        frame_store_filters = Frame(master=frame_store,
                                    background=blauw)
        frame_store_filters.pack(side=LEFT)

                    # Scales
        maximum_price = 60

        frame_store_filters_price = FrameFilter(frame_store_filters)
        label_filter_narrow_by_price = LabelFilter(frame_store_filters_price.frame, "white", grijs, "Narrow by Price", W, 0)
        scale_filter_price = ScaleStore(frame_store_filters_price.frame, maximum_price, lambda *args: getoonde_producten_sorteren_en_filteren())
        label_gefilterde_price = LabelFilter(frame_store_filters_price.frame, blauw3, blauw, "Any Price", CENTER, 10)

        frame_store_filters_age = FrameFilter(frame_store_filters)
        label_filter_narrow_by_age = LabelFilter(frame_store_filters_age.frame, "white", grijs, "Narrow by Age", W, 0)
        scale_filter_age = ScaleStore(frame_store_filters_age.frame, 18, lambda *args: getoonde_producten_sorteren_en_filteren())
        label_gefilterde_age = LabelFilter(frame_store_filters_age.frame, blauw3, blauw, "Any Age", CENTER, 10)

                    # Check buttons
        frame_store_filters_tags = FrameFilter(frame_store_filters)
        label_filter_narrow_by_tag = LabelFilter(frame_store_filters_tags.frame, "white", grijs, "Narrow by Tag", W, 0)

        filter_tags = []

                        # Popular tags
        checkbutton_tags_singleplayer = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Single-player", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_multiplayer = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Multi-player", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_action = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Action", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_adventure = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Adventure", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_casual = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Casual", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_co_op = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Co-op", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_first_person = CheckKnopStoreOpties(frame_store_filters_tags.frame, "First-Person", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_fps = CheckKnopStoreOpties(frame_store_filters_tags.frame, "FPS", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_great_soundtrack = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Great Soundtrack", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_horror = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Horror", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_indie = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Indie", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_open_world = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Open World", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_racing = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Racing", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_rpg = CheckKnopStoreOpties(frame_store_filters_tags.frame, "RPG", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_simulation = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Simulation", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_sports = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Sports", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_story_rich = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Story Rich", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_strategy = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Strategy", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_2d = CheckKnopStoreOpties(frame_store_filters_tags.frame, "2D", getoonde_producten_sorteren_en_filteren)

                        # Platforms
        frame_store_filters_platforms = FrameFilter(frame_store_filters)
        label_filter_platforms = LabelFilter(frame_store_filters_platforms.frame, "white", grijs, "Narrow by OS", W, 0)
        checkbutton_tags_windows = CheckKnopStoreOpties(frame_store_filters_platforms.frame, "Windows", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_mac = CheckKnopStoreOpties(frame_store_filters_platforms.frame, "Mac", getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_linux = CheckKnopStoreOpties(frame_store_filters_platforms.frame, "Linux", getoonde_producten_sorteren_en_filteren)

        checkbuttons = [checkbutton_tags_singleplayer,
                        checkbutton_tags_multiplayer,
                        checkbutton_tags_action,
                        checkbutton_tags_adventure,
                        checkbutton_tags_casual,
                        checkbutton_tags_co_op,
                        checkbutton_tags_first_person,
                        checkbutton_tags_fps,
                        checkbutton_tags_great_soundtrack,
                        checkbutton_tags_horror,
                        checkbutton_tags_indie,
                        checkbutton_tags_open_world,
                        checkbutton_tags_racing,
                        checkbutton_tags_rpg,
                        checkbutton_tags_simulation,
                        checkbutton_tags_sports,
                        checkbutton_tags_story_rich,
                        checkbutton_tags_strategy,
                        checkbutton_tags_2d,
                        checkbutton_tags_windows,
                        checkbutton_tags_mac,
                        checkbutton_tags_linux]

                        # Languages
        frame_store_filters_language = FrameFilter(frame_store_filters)
        label_filter_language = LabelFilter(frame_store_filters_language.frame, "white", grijs, "Narrow by Language", W, 0)
        checkbutton_tags_english = CheckKnopStoreOpties(frame_store_filters_language.frame, "English", getoonde_producten_sorteren_en_filteren)

    # Store tonen bij het opstarten van de applicatie.
        store_scherm_tonen(knop_store, frame_store)


def main():
    data = DataBewerking.json_bestand_inlezen()
    DataBewerking.rating_en_rating_percentage_toevoegen_aan_data(data)

    root = Tk()
    steam_gui = SteamGUI(root, data)
    root.mainloop()


if __name__ == "__main__":
    main()

# To do:
    # Sorteren                                                                                                                                           DONE
        # Zorgen dat listbox bij default alle producten toont gesorteerd op rating                                                                       DONE
        # - Dropdown menu for Sort by                                                                                                                    DONE
        # - Scale for price                                                                                                                              DONE
        # - Scale for required_age                                                                                                                       DONE
        # - Check buttons for most common categories, genres, steamspy_tags,                                                                             DONE
        # - Check buttons for platforms                                                                                                                  DONE
        # - Check button for language "English"                                                                                                          DONE
        # - Rating system                                                                                                                                DONE
                # Functie schrijven om ratingspercentage van producten toe te voegen aan de data                                                         DONE
                # ratingspercentage koppelen aan rating en toevoegen aan data(Overwhelmingly positive, Positive, Mixed, Mostly Negative, etc...          DONE
                # Rating tonen bij zoeken van producten                                                                                                  DONE

    # Statistiek

    # Steam API (vrienden) ???
