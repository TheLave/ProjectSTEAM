from tkinter import *
import json


class FrameMenubalk:
    def __init__(self, master):
        self.frame = Frame(master=master,
                           background="#1f2124")
        self.frame.pack(fill=X)


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
        def store_scherm_tonen():
            knop_store.button.configure(foreground="#FFFFFF")
            knop1.button.configure(foreground="#a1aab8")
            knop2.button.configure(foreground="#a1aab8")
            knop3.button.configure(foreground="#a1aab8")

            frame_knop1.forget()
            frame_knop2.forget()
            frame_knop3.forget()
            frame_store.pack(fill=BOTH,
                             expand=TRUE)


        def knop_1_scherm_tonen():
            knop1.button.configure(foreground="#FFFFFF")
            knop2.button.configure(foreground="#a1aab8")
            knop3.button.configure(foreground="#a1aab8")
            knop_store.button.configure(foreground="#a1aab8")

            frame_knop2.forget()
            frame_knop3.forget()
            frame_store.forget()
            frame_knop1.pack(fill=BOTH,
                              expand=TRUE)


        def knop_2_scherm_tonen():
            knop2.button.configure(foreground="#FFFFFF")
            knop1.button.configure(foreground="#a1aab8")
            knop3.button.configure(foreground="#a1aab8")
            knop_store.button.configure(foreground="#a1aab8")

            frame_knop1.forget()
            frame_knop3.forget()
            frame_store.forget()
            frame_knop2.pack(fill=BOTH,
                             expand=TRUE)


        def knop_3_scherm_tonen():
            knop3.button.configure(foreground="#FFFFFF")
            knop1.button.configure(foreground="#a1aab8")
            knop2.button.configure(foreground="#a1aab8")
            knop_store.button.configure(foreground="#a1aab8")

            frame_knop1.forget()
            frame_knop2.forget()
            frame_store.forget()
            frame_knop3.pack(fill=BOTH,
                             expand=TRUE)


# Widgets
        hoofdframe = Frame(master=master,
                           background="#194761")
        hoofdframe.pack(fill=BOTH,
                        expand=TRUE)

        # Menubalk1
        frame_menubalk1 = FrameMenubalk(hoofdframe)
        knop_programma_sluiten = KnopMenubalk1(frame_menubalk1.frame, "x", master.quit)
        knop_programma_minimaliseren = KnopMenubalk1(frame_menubalk1.frame, "-", master.iconify)

        # Menubalk2
        frame_menubalk2 = FrameMenubalk(hoofdframe)
        knop_store = KnopMenubalk2(frame_menubalk2.frame, "Store", store_scherm_tonen)
        knop1 = KnopMenubalk2(frame_menubalk2.frame, "Knop1", knop_1_scherm_tonen)
        knop2 = KnopMenubalk2(frame_menubalk2.frame, "Knop2", knop_2_scherm_tonen)
        knop3 = KnopMenubalk2(frame_menubalk2.frame, "Knop3", knop_3_scherm_tonen)

    # Schermen
        # Store scherm
        frame_store = Frame(master=hoofdframe,
                            background="red")

        # Knop1 scherm
        frame_knop1 = Frame(master=hoofdframe,
                            background="green")

        # Knop2 scherm
        frame_knop2 = Frame(master=hoofdframe,
                            background="blue")

        # Knop3 scherm
        frame_knop3 = Frame(master=hoofdframe,
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
