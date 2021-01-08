from tkinter import *
import json


class KnopMenubalk1:
    def __init__(self, master, text, command):
        self.button = Button(master=master,
                             foreground="#a1aab8",
                             activeforeground="#c4ccd8",
                             background="#1f2124",
                             activebackground="#1f2124",
                             borderwidth=0,
                             text=text,
                             font=("helvetica", 15, "bold"),
                             command=command)
        self.button.pack(side=RIGHT,
                         padx=15)


class KnopMenubalk2:
    def __init__(self, master, text, command):
        self.button = Button(master=master,
                             foreground="#a1aab8",
                             activeforeground="#c4ccd8",
                             background="#1f2124",
                             activebackground="#1f2124",
                             borderwidth=0,
                             text=text,
                             font=("helvetica", 25, "bold"),
                             command=command)
        self.button.pack(side=LEFT,
                         padx=10,
                         pady=5)


class SteamGUI:
    def __init__(self, master):
        def store_pagina_tonen():
            knop_store.button.configure(foreground="#FFFFFF")
            knop_1.button.configure(foreground="#a1aab8")
            knop_2.button.configure(foreground="#a1aab8")
            knop_3.button.configure(foreground="#a1aab8")

            frame_knop_1.forget()
            frame_knop_2.forget()
            frame_knop_3.forget()
            frame_store.pack(fill=BOTH,
                             expand=TRUE)


        def knop_1_pagina_tonen():
            knop_1.button.configure(foreground="#FFFFFF")
            knop_2.button.configure(foreground="#a1aab8")
            knop_3.button.configure(foreground="#a1aab8")
            knop_store.button.configure(foreground="#a1aab8")

            frame_knop_2.forget()
            frame_knop_3.forget()
            frame_store.forget()
            frame_knop_1.pack(fill=BOTH,
                              expand=TRUE)


        def knop_2_pagina_tonen():
            knop_2.button.configure(foreground="#FFFFFF")
            knop_1.button.configure(foreground="#a1aab8")
            knop_3.button.configure(foreground="#a1aab8")
            knop_store.button.configure(foreground="#a1aab8")

            frame_knop_1.forget()
            frame_knop_3.forget()
            frame_store.forget()
            frame_knop_2.pack(fill=BOTH,
                              expand=TRUE)


        def knop_3_pagina_tonen():
            knop_3.button.configure(foreground="#FFFFFF")
            knop_1.button.configure(foreground="#a1aab8")
            knop_2.button.configure(foreground="#a1aab8")
            knop_store.button.configure(foreground="#a1aab8")

            frame_knop_1.forget()
            frame_knop_2.forget()
            frame_store.forget()
            frame_knop_3.pack(fill=BOTH,
                              expand=TRUE)


    # Widgets
        hoofdframe = Frame(master=master,
                           background="#194761")
        hoofdframe.pack(fill=BOTH,
                        expand=TRUE)

        # Menubalk1
        frame_menubalk1 = Frame(master=hoofdframe,
                                background="#1f2124")
        frame_menubalk1.pack(fill=X)

        knop_programma_sluiten = KnopMenubalk1(frame_menubalk1, "x", master.quit)
        knop_programma_minimaliseren = KnopMenubalk1(frame_menubalk1, "-", master.iconify)

        # Menubalk2
        frame_menubalk2 = Frame(master=hoofdframe,
                                background="#1f2124")
        frame_menubalk2.pack(fill=X)

        knop_store = KnopMenubalk2(frame_menubalk2, "Store", store_pagina_tonen)
        knop_1 = KnopMenubalk2(frame_menubalk2, "Knop1", knop_1_pagina_tonen)
        knop_2 = KnopMenubalk2(frame_menubalk2, "Knop2", knop_2_pagina_tonen)
        knop_3 = KnopMenubalk2(frame_menubalk2, "Knop3", knop_3_pagina_tonen)

        # Store pagina
        frame_store = Frame(master=hoofdframe,
                            background="red")

        # Knop 1 pagina
        frame_knop_1 = Frame(master=hoofdframe,
                            background="green")

        # Knop 2 pagina
        frame_knop_2 = Frame(master=hoofdframe,
                            background="blue")

        # Knop 3 pagina
        frame_knop_3 = Frame(master=hoofdframe,
                            background="yellow")

        #TEST AREA
        # menu = Menu(master=master)
        # menu2 = Menubutton(master=master)

def json_bestand_inlezen():
    with open("steam.json", "r") as json_file:
        return json.load(json_file)


def main():
    root = Tk()

    root.title("Steam")
    root.bind("<Escape>", lambda self: root.destroy())
    root.attributes("-fullscreen", True)

    steam_gui = SteamGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
