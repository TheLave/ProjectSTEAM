import I2C_LCD_driver
from time import *
import RPi.GPIO as GPIO
import urllib.request, json
from datetime import datetime

mylcd = I2C_LCD_driver.lcd()
switch = 23

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( 0 )

textEntries = ['personaname', 'realname', 'personastate', 'lastlogoff', 'timecreated', 'steamid', 'loccountrycode']
textNameEntries = ['Nickname', 'Realname', 'Status', 'Last log off', 'Created on', 'Steam ID', 'Nationality']
entryIndex = 0
str_pad = " " * 16

with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=948437B690B388BBEFF1D07D68AB2553&steamids=76561198103986437") as url:
    rawData = json.loads(url.read().decode())
    data = rawData["response"]["players"]
    print(data)

GPIO.setup( switch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
while True:
   if( GPIO.input( switch ) ):
        mylcd.lcd_clear()
        mylcd.lcd_display_string(textNameEntries[entryIndex], 1)
        steamDataEntry = data[0][textEntries[entryIndex]]
        if textEntries[entryIndex] == 'lastlogoff' or textEntries[entryIndex] == 'timecreated':
           steamDataEntry = datetime.utcfromtimestamp(steamDataEntry).strftime('%d-%m-%Y %H:%M')
        elif textEntries[entryIndex] == 'personastate':
           if steamDataEntry == 0: steamDataEntry = 'Offline'
           elif steamDataEntry == 1: steamDataEntry = 'Online'
           elif steamDataEntry == 2: steamDataEntry = 'Busy'
           elif steamDataEntry == 3: steamDataEntry = 'Away'
           elif steamDataEntry == 4: steamDataEntry = 'Snooze'
           elif steamDataEntry == 5: steamDataEntry = 'Looking to trade'
           elif steamDataEntry == 6: steamDataEntry = 'Looking to play'
        if len(steamDataEntry) > 16:
            for i in range (0, len(steamDataEntry)):
                    lcd_text = steamDataEntry[i:(i+16)]
                    mylcd.lcd_display_string(lcd_text,2)
                    sleep(0.3)
                    mylcd.lcd_display_string(str_pad,2)
        else:
           mylcd.lcd_display_string(str(steamDataEntry), 2)
        entryIndex += 1
        if entryIndex > len(textEntries) - 1:
            entryIndex = 0
   sleep( 0.1 )