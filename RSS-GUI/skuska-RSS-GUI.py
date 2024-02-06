import tkinter as tk
from tkinter import ttk

import urllib.request as REQ
import xml.etree.ElementTree as ET

def getRssText(paURL, paTitle):
    returnText = ''    
    root = ET.fromstring(REQ.urlopen(paURL).read())

    checkTitle = False
    for channel in root:
        for item in channel:
            if item.tag == "item":
                for i in item:
                    if i.tag == "title":
                        if i.text == paTitle:
                            checkTitle = True
                    if i.tag == "description":
                        if checkTitle == True:
                            returnText += "Popis itemu:\n {}\n".format(i.text)
                            checkTitle = False
                            return returnText    

def listOfVersions(paURL, comboBox):
    root = ET.fromstring(REQ.urlopen(paURL).read())

    for channel in root:
        for item in channel:
            if item.tag == "item":
                for i in item:
                    if i.tag == "title":
                        comboBox['values'] = (*comboBox['values'], i.text)

def setWindow(self):
    # URL adresa
    rss_url = "https://mikrotik.com/download.rss"

    # hlavne okno
    self.title("RSS - Mikrotik RouterOS ChangeLogs")
    self.geometry("800x600+200+200")
    self.resizable(True, True)

    # text
    labelVerzia = tk.Label(self, text="Dostupne verzie: ")
    labelVerzia.grid(row = 0, column = 0, sticky = "w", padx = 20, pady = 20)

    # vyber z menu
    comboBoxVerzie = ttk.Combobox(self, state='readonly')

    listOfVersions(rss_url, comboBoxVerzie)
    
    comboBoxVerzie.bind("<<ComboboxSelected>>", 
    lambda _ : (outputText.delete(1.0, tk.END),
                outputText.replace(tk.END, tk.END, getRssText(rss_url, comboBoxVerzie.get()))))    

    comboBoxVerzie.grid(row = 0, column = 0, sticky = "w", padx = 150, ipadx = "100")
    comboBoxVerzie.current(0)       

    # vystup
    outputText = tk.Text(self)
    outputText.grid(row = 2, column = 0, sticky = "w", padx = 20, pady = 10)
    outputText.place()

# PROGRAM
hlavnaObrazovka = tk.Tk()
setWindow(hlavnaObrazovka)
hlavnaObrazovka.mainloop()