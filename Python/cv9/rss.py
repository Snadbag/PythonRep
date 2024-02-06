import urllib.request
import xml.etree.ElementTree as ET

import tkinter as tk
from win32api import GetSystemMetrics

def getRSSText(paURL):
    returnText = ""

    raw_page = urllib.request.urlopen(paURL)
    page = raw_page.read()

    root = ET.fromstring(page)

    for channel in root:
        for item in channel:
            if item.tag == "title":
                returnText += "Nadpis: {}\n".format(item.text)
            if item.tag == "description":
                returnText += "Popis: {}\n".format(item.text)
            if item.tag == "item":
                for i in item:
                    if i.tag == "title":
                        returnText += " Nadpis itemu: {}\n".format(i.text)
                    if i.tag == "description":
                        returnText += "    Popis itemu: {}\n".format(i.text)
    return returnText

url = "https://www.sme.sk/rss-title"
url2 = "http://www.dsl.sk/export/rss_articles.php"


# print(getRSSText(url))

def nastavOkno(paOkno):
    paOkno.title("RSS reader")

    paOkno.geometry("750x350+20+20")
    paOkno.resizable(True, True)

    labelURL = tk.Label(paOkno, text = "Zadaj URL: ")
    labelURL.grid(row = 0, column = 0, sticky = "w", padx = 10)

    entryURL = tk.Entry(paOkno)
    entryURL.grid(row = 1, column = 0, sticky = "w", padx = 10, ipadx = 260)
    entryURL.insert(0, "https://www.sme.sk/rss-title")

    outputText = tk.Text(paOkno)
    outputText.grid(row = 2, column = 0, sticky = "w", padx = 10)

    buttonUrob = tk.Button(paOkno, text = "Urob!", command = lambda : outputText.insert(tk.END, getRSSText(entryURL.get())))
    buttonUrob.grid(row = 1, column = 1, sticky = "w", padx = 10)

    return True

if __name__ == "__main__":
    okno = tk.Tk()

    nastavOkno(okno)

    okno.mainloop()