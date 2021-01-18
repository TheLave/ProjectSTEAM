from tkinter import *
import json
import urllib.request, json
from time import *
from datetime import datetime
from tkinter import messagebox


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
        Returnt de gesorteerde meegegeven lijst volgens het merge sort algoritme gebaseerd op de meegegeven zoekterm.
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

        def producten_zoeken_op_naam():
            """
            Zoekt naar producten waarvan de naam overeenkomt met de gegeven zoekterm en returnt een lijst hiervan.
            """
            lijst_temp.clear()

            for product in data:
                if entry_zoekbalk_producten.get().lower() in product['name'].lower():
                    lijst_temp.append(product)

        def lijst_sorteren_op_optie():
            """
            Sorteert en returnt de meegegeven lijst gebaseerd op de gekozen "sort by" keuze.
            """
            sortering = sort_by_optionmenu_waarde.get()

            if sortering == sort_by_opties[0] or sortering == sort_by_opties[1]:
                zoekterm = "release_date"
            elif sortering == sort_by_opties[2] or sortering == sort_by_opties[3]:
                zoekterm = "name"
            elif sortering == sort_by_opties[4] or sortering == sort_by_opties[5]:
                zoekterm = "price"
            elif sortering == sort_by_opties[6] or sortering == sort_by_opties[7]:
                zoekterm = "rating_percentage"

            lijst = Sorteren.merge_sort(lijst_temp, zoekterm)
            lijst_omgekeerde_sortering = [sort_by_opties[0], sort_by_opties[3], sort_by_opties[5], sort_by_opties[6]]

            if sortering in lijst_omgekeerde_sortering:
                lijst = Sorteren.lijst_omkeren(lijst_temp)

            return lijst

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
            lijst = lijst_sorteren_op_optie()
            lijst = producten_filteren_op_price(lijst)
            lijst = producten_filteren_op_age(lijst)
            lijst = producten_filteren_op_language(lijst, checkbutton_tags_english)

            for checkbutton in checkbuttons:
                lijst = producten_filteren_op_tag(lijst, checkbutton, checkbutton.checkbutton["text"])

            inhoud_listbox_aanpassen(lijst)

        def producten_tonen():
            producten_zoeken_op_naam()
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

        def stats_scherm_tonen(geklikte_knop, gekozen_pagina):
            geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen_menubalk2)
            applicatie_pagina_tonen(gekozen_pagina, applicatie_paginas)

        def raspi_scherm_tonen(geklikte_knop, gekozen_pagina):
            geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen_menubalk2)
            applicatie_pagina_tonen(gekozen_pagina, applicatie_paginas)

            try:
                import RPi.GPIO as GPIO
                import I2C_LCD_driver
            except ModuleNotFoundError:
                messagebox.showerror(title='Geen raspberry Pi', message='het lijkt erop dat u niet op een raspberry'
                                                                        ' Pi bezig bent dus heeft dit tablad geen '
                                                                        'functionaliteit voor u. U wordt terug'
                                                                        'gestuurd naar de store')
                store_scherm_tonen(knop_store, frame_store)
                return

            mylcd = I2C_LCD_driver.lcd()
            shift_clock_pin = 5
            latch_clock_pin = 6
            data_pin = 13
            servo = 25
            neo_clock_pin = 19
            neo_data_pin = 26
            switch = 23
            switch2 = 24

            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(0)
            GPIO.setup(data_pin, GPIO.OUT)
            GPIO.setup(shift_clock_pin, GPIO.OUT)
            GPIO.setup(latch_clock_pin, GPIO.OUT)
            GPIO.setup(servo, GPIO.OUT)
            GPIO.setup(neo_clock_pin, GPIO.OUT)
            GPIO.setup(neo_data_pin, GPIO.OUT)

            textEntries = ['personaname', 'realname', 'personastate', 'lastlogoff', 'timecreated', 'steamid',
                           'loccountrycode']
            textNameEntries = ['Nickname', 'Realname', 'Status', 'Last log off', 'Created on', 'Steam ID',
                               'Nationality']
            personaStatusEntries = ['Offline', 'Online', 'Busy', 'Away', 'Snooze', 'Looking to trade',
                                    'Looking to play']
            str_pad = " " * 16

            # neopixels
            def apa102_send_bytes(clock_pin, data_pin, bytes):
                for byte in bytes:
                    for bits in byte:
                        if bits == 1:
                            GPIO.output(data_pin, GPIO.HIGH)
                        else:
                            GPIO.output(data_pin, GPIO.LOW)

                        GPIO.output(clock_pin, GPIO.HIGH)
                        GPIO.output(clock_pin, GPIO.LOW)

            def apa102(clock_pin, data_pin, color):
                byte0 = [0, 0, 0, 0, 0, 0, 0, 0]
                byte1 = [1, 1, 1, 1, 1, 1, 1, 1]
                nummertjes = []
                data = []

                for byte in range(4):
                    byte = 8
                    for bits in range(byte):
                        apa102_send_bytes(clock_pin, data_pin, [byte0])

                for i in range(8):
                    for bits in range(1):
                        apa102_send_bytes(clock_pin, data_pin, [byte1])

                    for value in color:
                        if value == 0:
                            for i in range(8):
                                nummertjes.append(0)

                        while value >= 1:
                            if (value % 2) == 1:
                                nummertjes.append(1)
                            else:
                                nummertjes.append(0)

                            value = value // 2

                        while len(nummertjes) < 8:
                            nummertjes.append(0)

                        nummertjes.reverse()
                        data.append(nummertjes)
                        apa102_send_bytes(clock_pin, data_pin, data)
                        nummertjes.clear()
                        data.clear()

                for byte in range(4):
                    byte = 8

                    for bits in range(byte):
                        apa102_send_bytes(clock_pin, data_pin, [byte1])

            def check_personstate(steamid):
                kleuren = {
                    'blue': [255, 0, 0],
                    'green': [0, 255, 0],
                    'red': [0, 0, 255],
                    'yellow': [0, 146, 190],
                    'orange': [0, 106, 255],
                    'pink': [50, 50, 200],
                    'purple': [200, 0, 100]}

                with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key"
                                            f"=948437B690B388BBEFF1D07D68AB2553&steamids={steamid}") as url:
                    rawData = json.loads(url.read().decode())
                    dataProfiel = rawData["response"]["players"]

                if dataProfiel[0]['personastate'] == 0:
                    print('offline')
                    apa102(neo_clock_pin, neo_data_pin, kleuren['red'])

                elif dataProfiel[0]['personastate'] == 1:
                    print('online')
                    apa102(neo_clock_pin, neo_data_pin, kleuren['green'])

                elif dataProfiel[0]['personastate'] == 2:
                    print('busy')
                    apa102(neo_clock_pin, neo_data_pin, kleuren['yellow'])

                elif dataProfiel[0]['personastate'] == 3:
                    print('away')
                    apa102(neo_clock_pin, neo_data_pin, kleuren['orange'])

                elif dataProfiel[0]['personastate'] == 4:
                    print('snooze')
                    apa102(neo_clock_pin, neo_data_pin, kleuren['blue'])

                elif dataProfiel[0]['personastate'] == 5:
                    print('Looking to trade')
                    apa102(neo_clock_pin, neo_data_pin, kleuren['pink'])

                elif dataProfiel[0]['personastate'] == 6:
                    print('Looking to play')
                    apa102(neo_clock_pin, neo_data_pin, kleuren['purple'])

            # servo
            def pulse(pin, delay1, delay2):
                GPIO.output(pin, GPIO.HIGH)
                sleep(delay1)
                GPIO.output(pin, GPIO.LOW)
                sleep(delay2)

            def servo_pulse(pin_nr, position):
                delay = 0.0005 + (0.00002 * position)

                pulse(pin_nr, delay, 0.02)

            def check_state(steamid):
                with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key"
                                            f"=948437B690B388BBEFF1D07D68AB2553&steamids={steamid}") as url:
                    rawData = json.loads(url.read().decode())
                    data = rawData["response"]["players"]

                if data[0]['personastate'] == 0:
                    print('offline links')

                    for i in range(0, 30, 1):
                        servo_pulse(servo, 100)

                elif data[0]['personastate'] in [1, 5, 6]:
                    print('online rechts')

                    for i in range(0, 30, 1):
                        servo_pulse(servo, 0)

                elif data[0]['personastate'] in [2, 3, 4]:
                    print('away midden')
                    servo_pulse(servo, 50)

            # schuifregister
            def check_achievments(data):
                voltooid = 0

                for achievements in data:
                    if achievements['achieved'] == 1:
                        voltooid += 1

                print('aantal achievements behaald: ' + str(voltooid))
                return voltooid

            def bereken_lampjes(aantalAchievements, data):
                aantalLampjes = -1
                keer = 1
                voltooid = check_achievments(data)

                while aantalLampjes == -1:
                    # kijkt hoeveel lampjes er aan moeten (max 8)
                    if ((aantalAchievements / 8) * keer) < voltooid and keer < 8:
                        keer += 1

                    if ((aantalAchievements / 8) * keer) > voltooid:
                        aantalLampjes = keer - 1

                    if ((aantalAchievements / 8) * keer) == voltooid:
                        aantalLampjes = keer

                uit = 8 - aantalLampjes
                return uit, aantalLampjes

            def zet_lampjes_aan(steamid2, appid):
                with urllib.request.urlopen(
                        f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}"
                        f"&key=248E21AEC4B9E0FA386209D67BF7AC5F&steamid={steamid2}") as url:
                    rawData = json.loads(url.read().decode())
                    data = rawData["playerstats"]['achievements']
                    spel = rawData["playerstats"]['gameName']
                    print('Spel: ' + spel)
                    print('Aantal achievements: ' + str(len(data)))

                aantalAchievements = len(data)
                uit, aantalLampjes = bereken_lampjes(aantalAchievements, data)

                for i in range(8):
                    GPIO.output(data_pin, GPIO.LOW)
                    GPIO.output(shift_clock_pin, GPIO.HIGH)
                    GPIO.output(shift_clock_pin, GPIO.LOW)

                for i in range(uit):
                    GPIO.output(data_pin, GPIO.LOW)
                    GPIO.output(shift_clock_pin, GPIO.HIGH)
                    GPIO.output(shift_clock_pin, GPIO.LOW)

                for i in range(aantalLampjes):
                    GPIO.output(data_pin, GPIO.HIGH)
                    GPIO.output(shift_clock_pin, GPIO.HIGH)
                    GPIO.output(shift_clock_pin, GPIO.LOW)

                GPIO.output(latch_clock_pin, GPIO.HIGH)
                GPIO.output(latch_clock_pin, GPIO.LOW)

            def start_display(steamid):
                entryIndex = 0
                pressed = False

                with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key"
                                            f"=948437B690B388BBEFF1D07D68AB2553&steamids={steamid}") as url:
                    rawData = json.loads(url.read().decode())

                    if rawData["response"]["players"]:
                        data = rawData["response"]["players"][0]
                        print('Data read successful')
                    else:
                        print('Data read failed. Is the steamID correct?')

                mylcd.lcd_clear()
                mylcd.lcd_display_string('Druk op de knop', 1)
                mylcd.lcd_display_string('voor informatie', 2)

                GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
                GPIO.setup(switch2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

                while True:
                    if GPIO.input(switch2):
                        if not pressed:
                            mylcd.lcd_clear()
                            mylcd.lcd_display_string('Steam GUI', 1)
                            mylcd.lcd_display_string('SG23 Groep A', 2)
                            break

                    if GPIO.input(switch):
                        if pressed == False:
                            pressed = not pressed
                            mylcd.lcd_clear()
                            mylcd.lcd_display_string(textNameEntries[entryIndex], 1)
                            steamDataEntry = data[textEntries[entryIndex]]

                            if textEntries[entryIndex] == 'lastlogoff' or textEntries[entryIndex] == 'timecreated':
                                steamDataEntry = datetime.utcfromtimestamp(steamDataEntry).strftime('%d-%m-%Y %H:%M')
                            elif textEntries[entryIndex] == 'personastate':
                                steamDataEntry = personaStatusEntries[steamDataEntry]

                            if len(steamDataEntry) > 16:
                                for i in range(0, len(steamDataEntry)):
                                    lcd_text = steamDataEntry[i:(i + 16)]
                                    mylcd.lcd_display_string(lcd_text, 2)
                                    sleep(0.3)
                                    mylcd.lcd_display_string(str_pad, 2)
                                mylcd.lcd_display_string(str(steamDataEntry), 2)
                            else:
                                mylcd.lcd_display_string(str(steamDataEntry), 2)
                            entryIndex += 1

                            if entryIndex > len(textEntries) - 1:
                                entryIndex = 0
                    else:
                        pressed = False
                    sleep(0.1)

            knop_servo = Button(frame_servo_neopixels,
                                foreground=babyblauw,
                                activeforeground="white",
                                background=blauw2,
                                activebackground=lichtblauw,
                                width=8,
                                text="start servo",
                                font=("Helvetica", 10, "bold"),
                                command=lambda: check_state(steamid_box.get()))

            knop_neopixels = Button(frame_servo_neopixels,
                                    foreground=babyblauw,
                                    activeforeground="white",
                                    background=blauw2,
                                    activebackground=lichtblauw,
                                    text="start led strip",
                                    font=("Helvetica", 10, "bold"),
                                    command=lambda: check_personstate(steamid_box.get()))

            knop_schuifregister = Button(frame_schuifregister,
                                         foreground=babyblauw,
                                         activeforeground="white",
                                         background=blauw2,
                                         activebackground=lichtblauw,
                                         width=8,
                                         text="start",
                                         font=("Helvetica", 10, "bold"),
                                         command=lambda: zet_lampjes_aan(steamid_box.get(), appid_box.get()))

            knop_display = Button(frame_schermpje,
                                  foreground=babyblauw,
                                  activeforeground="white",
                                  background=blauw2,
                                  activebackground=lichtblauw,
                                  width=8,
                                  text="start",
                                  font=("Helvetica", 10, "bold"),
                                  command=lambda: start_display(steamid_box.get()))

            geklikte_knop_menubalk2_highlighten(geklikte_knop, knoppen_menubalk2)
            applicatie_pagina_tonen(gekozen_pagina, applicatie_paginas)
            scherm_ti_conf(knop_servo, knop_neopixels, knop_schuifregister, knop_display)

        def scherm_ti_conf(knop1, knop2, knop3, knop4):
            frame_servo_neopixels.pack(side=LEFT,
                                       padx=50,
                                       pady=(70, 400))
            frame_servo_neopixels.pack_propagate(False)

            frame_schermpje.pack(side=RIGHT,
                                 padx=50,
                                 pady=(70, 400))
            frame_schermpje.pack_propagate(False)

            frame_schuifregister.pack(side=TOP,
                                      anchor=CENTER,
                                      pady=20)
            frame_schuifregister.pack_propagate(False)

            frame_header1.place(anchor=N,
                                x=200)
            frame_header1.pack_propagate(False)

            frame_header2.place(anchor=N,
                                x=200)
            frame_header2.pack_propagate(False)

            frame_header3.place(anchor=N,
                                x=200)
            frame_header3.pack_propagate(False)

            header_1.pack(pady=5)
            header_2.pack(pady=5)
            header_3.pack(pady=5)

            steamid_label2.pack(side=TOP,
                                pady=(55, 15))
            steamid_box.pack(side=TOP,
                             pady=0)

            appid_label.pack(side=TOP,
                             pady=(25, 15))
            appid_box.pack(side=TOP,
                           pady=0)

            knop1.pack(side=BOTTOM,
                       anchor=W,
                       pady=(20, 0),
                       padx=(160, 0))

            knop2.pack(side=BOTTOM,
                       anchor=W,
                       pady=(55, 0),
                       padx=(150, 0))

            knop3.pack(side=BOTTOM,
                       pady=20)

            knop4.pack(side=BOTTOM,
                       pady=20)

            uitleg_neopixels.pack(side=LEFT,
                                  anchor=N,
                                  padx=(30, 0),
                                  pady=(50, 0))

            uitleg_servo.pack(side=RIGHT,
                              anchor=N,
                              padx=(0, 10),
                              pady=(50, 0))

            uitleg_schuifregister.pack(side=TOP,
                                       pady=(30, 0))

            uitleg_display.pack(side=TOP,
                                pady=(60, 0))

        def statistiek_kwantitatief():
            """
            Vraagt om invoering van game genre en berekent & toont het percentage van het totaal aantal games met dat genre.
            """
            zoek_term = []

            for i in range(len(data)):
                if genre_entry.get().lower() in data[i]['genres'].lower():
                    zoek_term.append(data[i]['name'])

            percentage = (len(zoek_term) / len(data)) * 100

            tekst_kwantitatief = "Er zijn {} games met '{}' als genre. \nDat is {:<.1f}% van alle {} games."
            label_kwantitatief["text"] = tekst_kwantitatief.format(len(zoek_term), genre_entry.get(), percentage,
                                                                   len(data))

        def statistiek_kwalitatief():
            """
            Toont de average playtime bij de price.
            """
            range_gratis = []
            range_0_10 = []
            range_10_30 = []
            range_30_45 = []
            range_45_60 = []
            range_boven_60 = []

            for i in range(len(data)):
                if data[i]['price'] == 0:
                    range_gratis.append(data[i]['average_playtime'])
                    gemiddelde_1 = sum(range_gratis) / len(range_gratis)

                elif data[i]['price'] > 0 and data[i]['price'] < 10:
                    range_0_10.append(data[i]['average_playtime'])
                    gemiddelde_2 = sum(range_0_10) / len(range_0_10)

                elif data[i]['price'] > 10 and data[i]['price'] < 30:
                    range_10_30.append(data[i]['average_playtime'])
                    gemiddelde_3 = sum(range_10_30) / len(range_10_30)

                elif data[i]['price'] > 30 and data[i]['price'] < 45:
                    range_30_45.append(data[i]['average_playtime'])
                    gemiddelde_4 = sum(range_30_45) / len(range_30_45)

                elif data[i]['price'] > 45 and data[i]['price'] < 60:
                    range_45_60.append(data[i]['average_playtime'])
                    gemiddelde_5 = sum(range_45_60) / len(range_45_60)

                elif data[i]['price'] >= 60:
                    range_boven_60.append(data[i]['average_playtime'])
                    gemiddelde_6 = sum(range_boven_60) / len(range_boven_60)

            tekst_kwalitatief = (
                f"Er zijn {len(range_gratis)} games in de prijs range: 'gratis'. "
                f"Deze hebben een gemiddelde speeltijd van: {gemiddelde_1:<.0f}uur"
                f"\nEr zijn {len(range_0_10)} games in de prijs range: €0.01<€10. "
                f"Deze hebben een gemiddelde speeltijd van: {gemiddelde_2:<.0f}uur "
                f"\nEr zijn {len(range_10_30)} games in de prijs range: €10<€30. "
                f"Deze hebben een gemiddelde speeltijd van: {gemiddelde_3:<.0f}uur "
                f"\nEr zijn {len(range_30_45)} games in de prijs range: €30<€45. "
                f"Deze hebben een gemiddelde speeltijd van: {gemiddelde_4:<.0f}uur "
                f"\nEr zijn {len(range_45_60)} games in de prijs range: €45<€60. "
                f"Deze hebben een gemiddelde speeltijd van: {gemiddelde_5:<.0f}uur "
                f"\nEr zijn {len(range_boven_60)} games in de prijs range: >€60. "
                f"Deze hebben een gemiddelde speeltijd van: {gemiddelde_6:<.0f}uur ")
            label_kwalitatief["text"] = tekst_kwalitatief

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
                                     highlightthickness=0,
                                     text=text,
                                     font=("Helvetica", 12, "bold"),
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
                                     highlightthickness=0,
                                     text=text,
                                     font=("Helvetica", 18),
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
                                   font=("Helvetica", 10),
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
                                               highlightthickness=0,
                                               text=text,
                                               font=("Helvetica", 10),
                                               variable=self.var,
                                               command=command,
                                               anchor=W)
                self.checkbutton.pack(padx=(10, 0))
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
        knop_stats = KnopMenubalk2(frame_menubalk2.frame, "STATS", lambda: stats_scherm_tonen(knop_stats, frame_stats))
        knop_raspi = KnopMenubalk2(frame_menubalk2.frame, "RASPI", lambda: raspi_scherm_tonen(knop_raspi, frame_raspi))

        # Applicatie pagina's
        applicatie_paginas = []

        # Store scherm
        frame_store = Frame(master=hoofdframe,
                            background=blauw)

        frame_store_producten = Frame(master=frame_store,
                                      background=blauw)
        frame_store_producten.pack(side=LEFT,
                                   padx=(240, 10))



        # Stats scherm
        frame_stats = Frame(master=hoofdframe,
                            background=blauw)

        # Raspi scherm
        frame_raspi = Frame(master=hoofdframe,
                         background=blauw)

        # Widgets op Raspi scherm
        # frame 1 servo en neopixels
        frame_servo_neopixels = Frame(frame_raspi,
                                      bg=donkerblauw,
                                      height=400,
                                      width=400)

        frame_header1 = LabelFrame(frame_servo_neopixels,
                                   bg=navy,
                                   height=40,
                                   width=400)

        header_1 = Label(frame_header1,
                         text='online/offline en personastate',
                         bg=navy,
                         font=("Helvetica", 14, "italic"),
                         fg='white')

        # frame 2 schuifregister
        frame_schuifregister = Frame(frame_raspi,
                                     bg=donkerblauw,
                                     height=400,
                                     width=400)

        frame_header2 = LabelFrame(frame_schuifregister,
                                   bg=navy,
                                   height=40,
                                   width=400)

        header_2 = Label(frame_header2,
                         text='achievement progress',
                         bg=navy,
                         font=("Helvetica", 14, "italic"),
                         fg='white')

        # frame 3 schermpje en knop
        frame_schermpje = Frame(frame_raspi,
                                bg=donkerblauw,
                                height=400,
                                width=400)

        frame_header3 = LabelFrame(frame_schermpje,
                                   bg=navy,
                                   height=40,
                                   width=400)

        header_3 = Label(frame_header3,
                         text='Steam profiel informatie',
                         bg=navy,
                         font=("Helvetica", 14, "italic"),
                         fg='white')

        # knoppen, labels en entry's frame 2
        steamid_box = Entry(frame_schuifregister,
                            foreground="white",
                            background=blauw2,
                            width=30,
                            font=("Helvetica", 14))

        steamid_label2 = Label(frame_schuifregister,
                               fg=blauw3,
                               background=donkerblauw,
                               font=("Helvetica", 14),
                               text='voer hier het steamid van iemand in')

        appid_box = Entry(frame_schuifregister,
                          foreground="white",
                          background=blauw2,
                          width=30,
                          font=("Helvetica", 14))

        appid_label = Label(frame_schuifregister,
                            fg=blauw3,
                            background=donkerblauw,
                            font=("Helvetica", 14),
                            text='voer hier het appid van een spel in')

        uitleg_servo = Label(frame_servo_neopixels,
                             fg=blauw3,
                             background=donkerblauw,
                             justify=LEFT,
                             font=("Helvetica", 11),
                             text='Het servo motortje geeft aan \n'
                                  'of iemand online is of niet: \n'
                                  'Links: offline \n'
                                  'Rechts: online \n'
                                  'Midden: away')

        uitleg_neopixels = Label(frame_servo_neopixels,
                                 fg=blauw3,
                                 justify=LEFT,
                                 background=donkerblauw,
                                 font=("Helvetica", 11),
                                 text='De led strip geeft de\n'
                                      'personastate weer: \n'
                                      'Rood:    offline\n'
                                      'Oranje: away\n'
                                      'Groen:  online\n'
                                      'Geel:     busy\n'
                                      'Blauw:  snooze\n'
                                      'Paars:  looking to play\n'
                                      'Roze:   looking to trade\n')

        uitleg_display = Label(frame_schermpje,
                               fg=blauw3,
                               justify=LEFT,
                               background=donkerblauw,
                               font=("Helvetica", 14),
                               text='Op het display komt Steam acount informatie.\n'
                                    'Gebruik de knoppen om te navigeren:\n'
                                    'Geel:   Volgende\n'
                                    'Zwart:  Stop\n')

        uitleg_schuifregister = Label(frame_schuifregister,
                                      fg=blauw3,
                                      background=donkerblauw,
                                      font=("Helvetica", 14),
                                      text='De lampjes geven weer hoeveel procent \n '
                                           'van de achievements je voor het \n '
                                           'gegeven spel hebt gehaald')

        applicatie_paginas.extend([frame_store,
                                   frame_stats,
                                   frame_raspi])

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
                                         font=("Helvetica", 14))
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
                                         font=("Helvetica", 10, "bold"),
                                         command=producten_tonen)
        knop_zoekbalk_producten.pack(side=LEFT)

        master.bind("<Return>", lambda *args: producten_tonen())

        # Sort by
        label_sort_by = Label(master=frame_zoekbalk_producten,
                              foreground=grijs,
                              background=navy,
                              text="Sort by",
                              font=("Helvetica", 10))
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
                                     font=("Helvetica", 10, "bold"),
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
                                    selectforeground=lichtgrijs,
                                    selectbackground=navy,
                                    height=48,
                                    width=99,
                                    font=("Courier", 12))
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
        label_filter_narrow_by_price = LabelFilter(frame_store_filters_price.frame, "white", grijs, "Narrow by Price",
                                                   W, 0)
        scale_filter_price = ScaleStore(frame_store_filters_price.frame, maximum_price,
                                        lambda *args: getoonde_producten_sorteren_en_filteren())
        label_gefilterde_price = LabelFilter(frame_store_filters_price.frame, blauw3, blauw, "Any Price", CENTER, 10)

        frame_store_filters_age = FrameFilter(frame_store_filters)
        label_filter_narrow_by_age = LabelFilter(frame_store_filters_age.frame, "white", grijs, "Narrow by Age", W, 0)
        scale_filter_age = ScaleStore(frame_store_filters_age.frame, 18,
                                      lambda *args: getoonde_producten_sorteren_en_filteren())
        label_gefilterde_age = LabelFilter(frame_store_filters_age.frame, blauw3, blauw, "Any Age", CENTER, 10)

        # Check buttons
        frame_store_filters_tags = FrameFilter(frame_store_filters)
        label_filter_narrow_by_tag = LabelFilter(frame_store_filters_tags.frame, "white", grijs, "Narrow by Tag", W, 0)

        filter_tags = []

        # Popular tags
        checkbutton_tags_singleplayer = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Single-player",
                                                             getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_multiplayer = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Multi-player",
                                                            getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_action = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Action",
                                                       getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_adventure = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Adventure",
                                                          getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_casual = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Casual",
                                                       getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_co_op = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Co-op",
                                                      getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_first_person = CheckKnopStoreOpties(frame_store_filters_tags.frame, "First-Person",
                                                             getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_fps = CheckKnopStoreOpties(frame_store_filters_tags.frame, "FPS",
                                                    getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_great_soundtrack = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Great Soundtrack",
                                                                 getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_horror = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Horror",
                                                       getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_indie = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Indie",
                                                      getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_open_world = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Open World",
                                                           getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_racing = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Racing",
                                                       getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_rpg = CheckKnopStoreOpties(frame_store_filters_tags.frame, "RPG",
                                                    getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_simulation = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Simulation",
                                                           getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_sports = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Sports",
                                                       getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_story_rich = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Story Rich",
                                                           getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_strategy = CheckKnopStoreOpties(frame_store_filters_tags.frame, "Strategy",
                                                         getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_2d = CheckKnopStoreOpties(frame_store_filters_tags.frame, "2D",
                                                   getoonde_producten_sorteren_en_filteren)

        # Platforms
        frame_store_filters_platforms = FrameFilter(frame_store_filters)
        label_filter_platforms = LabelFilter(frame_store_filters_platforms.frame, "white", grijs, "Narrow by OS", W, 0)
        checkbutton_tags_windows = CheckKnopStoreOpties(frame_store_filters_platforms.frame, "Windows",
                                                        getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_mac = CheckKnopStoreOpties(frame_store_filters_platforms.frame, "Mac",
                                                    getoonde_producten_sorteren_en_filteren)
        checkbutton_tags_linux = CheckKnopStoreOpties(frame_store_filters_platforms.frame, "Linux",
                                                      getoonde_producten_sorteren_en_filteren)

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
        label_filter_language = LabelFilter(frame_store_filters_language.frame, "white", grijs, "Narrow by Language", W,
                                            0)
        checkbutton_tags_english = CheckKnopStoreOpties(frame_store_filters_language.frame, "English",
                                                        getoonde_producten_sorteren_en_filteren)

        # Store tonen bij het opstarten van de applicatie.
        store_scherm_tonen(knop_store, frame_store)

        #Stats Pagina
        #Widgets op Stats pagina
        totaal_frame = Frame(master=frame_stats,
                             background=blauw,
                             height=500,
                             width=800)
        totaal_frame.pack(side=TOP,
                          anchor=W)

        intro_label = Label(master=totaal_frame,
                            text='Statistieken',
                            bg=blauw,
                            fg='white',
                            font=("Helvetica", 14, "bold"))
        intro_label.pack(side=TOP,
                         fill=X,
                         pady=10)

        genre_label = Label(master=totaal_frame,
                            text='Van welk genre wil je het percentage games weten?: ',
                            bg=blauw,
                            foreground='white',
                            font=("Helvetica", 14, ""))
        genre_label.pack(pady=5)

        genre_entry = Entry(master=totaal_frame)
        genre_entry.pack(padx=10,
                         pady=10)

        test_button = Button(master=totaal_frame,
                             text='druk hier',
                             command=statistiek_kwantitatief)
        test_button.pack(pady=10)

        kwantitatief_frame = Frame(master=totaal_frame,
                                   bg=blauw)
        kwantitatief_frame.pack(fill='both',
                                expand=True,
                                pady=5)

        label_kwantitatief = Label(master=totaal_frame,
                                   bg=blauw,
                                   fg='white',
                                   font=("Helvetica", 10, "bold"))
        label_kwantitatief.pack(pady=5)

        kwalitatief_frame = Frame(master=totaal_frame,
                                  bg=blauw)
        kwalitatief_frame.pack(fill='both',
                               expand=True,
                               pady=5)

        kwalitatief_info = Label(master=totaal_frame,
                                 bg=blauw,
                                 fg='white',
                                 font=("Helvetica", 10, "bold"),
                                 text="Vergelijkingen prijs met speeltijd: ")
        kwalitatief_info.pack()

        label_kwalitatief = Label(master=totaal_frame,
                                  bg=blauw,
                                  fg='white',
                                  font=("Helvetica", 10, "bold"))
        label_kwalitatief.pack(pady=5)

        statistiek_kwalitatief()


def main():
    data = DataBewerking.json_bestand_inlezen()
    DataBewerking.rating_en_rating_percentage_toevoegen_aan_data(data)

    root = Tk()
    steam_gui = SteamGUI(root, data)
    root.mainloop()


if __name__ == "__main__":
    main()
