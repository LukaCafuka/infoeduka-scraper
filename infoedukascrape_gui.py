#---------------------------------------#
# Infoeduka Scraper GUI Variant         #
# By Luka Cafuka                        #
# Info can be found at z.com.hr         #
#---------------------------------------#

import time
import json
import threading
import queue
import requests
from utils.getcookie import *
import os
import tkinter as tk
from tkinter import ttk
from utils.gui import initWindow, chooseDir

class RedirectedConsole:
    def __init__(self, textWidget):
        self.textWidget = textWidget

    def write(self, text):
        self.textWidget.insert(tk.END, text)    # insert the text into the text widget
        self.textWidget.see(tk.END)             # scroll to the end

    def flush(self):
        pass  # required for compatibility with sys.stdout and sys.stderr


def fetchJSON(manualCookie=None, showCookie=False):
    # JSON file that contains file and study info
    url = f"https://student.algebra.hr/digitalnareferada/api/student/predmeti/?dodatno=materijali"

    if manualCookie is None:
        # call getCookie() in order to authorize access
        if showCookie is True:
            cookie = getCookie(showCookie=True)
        else:
            cookie = getCookie(showCookie=False)
    else:
        cookie = { 'PHPSESSID': manualCookie }

    try:  # make request to JSON file
        response = requests.get(url, cookies=cookie)
        response.raise_for_status()
        response = json.loads(response.text)
        return cookie, response
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"

# Function to count the number of files to be downloaded
def countFiles(fullData):
    totalFiles = 0

    for yearData in fullData:
        for godData in yearData.get('godine', []):
            predmeti = godData.get('predmeti', [])
            if isinstance(predmeti, list):  # Check if predmeti is a list
                for predmet in predmeti:
                    dodatno = predmet.get('dodatno', {})
                    materijali = dodatno.get('materijali', {})
                    kategorije = materijali.get('kategorije', [])

                    for kategorija in kategorije:
                        materials = kategorija.get('materijali', [])
                        totalFiles += len(materials)

    return totalFiles


# prep function to use multiple threads in order to make the GUI responsive
def scrapePrep():

    startBtn.config(state=tk.DISABLED)                          # disable the start button to prevent multiple starts
    q = queue.Queue()                                           # create a queue to communicate with the main thread
    threading.Thread(target=startScrape, args=(q,)).start()     # run the scraping function in a separate thread
    root.after(100, checkThread, q)                             # periodically check if the background task is done

def checkThread(q):
    try:
        result = q.get_nowait()                 # check if there's data in the queue
    except queue.Empty:
        root.after(100, checkThread, q)         # no data yet, check again after 100ms
    else:
        if result == "done":
            startBtn.config(state=tk.NORMAL)    # re-enable the start button when done


# main scraping function
def startScrape(q=None, path=None, automaticCookie=True, manualCookie=None, showCookie=False):
    if path is None:
        print("Enter the path to where you want the scraped data to be stored")
        try:
            path = chooseDir()

        except Exception as e:
            print(e)
    rootPath = os.path.join(path, 'InfoedukaScraper')
    print(f"Directory created at: {rootPath}")

    if automaticCookie:
        print("You will need to login in order to fetch the cookie and authorize with the server")
        cookie, response = fetchJSON(manualCookie, showCookie)
        fullData = response.get('data', [])
    else:
        cookie, response = fetchJSON(manualCookie, showCookie)
        fullData = response.get('data', [])

    totalFiles = countFiles(fullData)
    print(f"Total number of files to be downloaded: {totalFiles}")
    print("The download will start soon...")
    time.sleep(2)

    # navigate through the JSON structure
    for yearData in fullData:
        for godData in yearData.get('godine', []):
            predmeti = godData.get('predmeti', [])
            if isinstance(predmeti, list):  # check if studies are a list
                for predmet in predmeti:
                    # fetch subject name in order to create directory names
                    predmetName = predmet.get('predmet')

                    # join the root directory path with the subject name in order to create appropriate sub-dirs
                    predmetPath = os.path.join(rootPath, predmetName)
                    os.makedirs(predmetPath, exist_ok=True)

                    # navigate to 'dodatno' -> 'materijali' -> 'kategorije' -> 'materijali'
                    dodatno = predmet.get('dodatno', {})
                    materijali = dodatno.get('materijali', {})
                    kategorije = materijali.get('kategorije', [])

                    for kategorija in kategorije:
                        materials = kategorija.get('materijali', [])
                        kategorijaName = kategorija.get('kategorija')

                        kategorijaPath = os.path.join(predmetPath, kategorijaName)
                        os.makedirs(kategorijaPath, exist_ok=True)

                        for material in materials:

                            materialLink = material.get('link')

                            materialName = material.get('naziv')

                            if materialLink:
                                # construct the full URL
                                fullUrl = "https://student.algebra.hr/digitalnareferada/" + materialLink

                                try:
                                    # fetch the content from the URL
                                    response = requests.get(fullUrl, cookies=cookie)
                                    response.raise_for_status()  # Check for HTTP errors

                                    # determine the filename (e.g., extract from the URL or use material ID)
                                    filename = os.path.join(kategorijaPath, materialName)  # Save as PDF

                                    # save the content to a file
                                    with open(filename, 'wb') as file:
                                        file.write(response.content)

                                    print(f"Downloaded {materialName} from {predmetName}")
                                except requests.exceptions.RequestException as e:
                                    print(f"Failed to download {materialLink}: {e}")
    if q is not None:
        q.put("done")
    print("Finished!")


if __name__ == '__main__':
    # initialize the root window
    root = initWindow()

    # title text label
    titleLabel = ttk.Label(root, text="Infoeduka Scraper", font=("Arial", 20))
    titleLabel.grid(row=0, column=0, padx=10, pady=3)

    # copyright label
    descLabel = ttk.Label(root, text="by LukaCafuka - z.com.hr", font=("Arial", 12))
    descLabel.grid(row=1, column=0, padx=10, pady=3)

    # cookie retrieval info
    descLabel = ttk.Label(root, text="You will be asked to input a folder location for the downloaded data", font=("Arial", 10), foreground="black")
    descLabel.grid(row=4, column=0, padx=10, pady=3)

    # cookie retrieval info
    descLabel = ttk.Label(root, text="You will be prompted for login in order to authorize with the Infoeduka server",
                          font=("Arial", 10), foreground="red")
    descLabel.grid(row=5, column=0, padx=10, pady=3)


    # start scrape button
    startBtn = ttk.Button(root, text='Start', command=scrapePrep)
    startBtn.grid(row=6, column=0, padx=4, pady=0, sticky='ew')

    # quit app button
    btn = ttk.Button(root, text='Quit', command=root.quit)
    btn.grid(row=7, column=0, padx=4, pady=0, sticky='ew')

    # console label
    descLabel = ttk.Label(root, text="Console logs", font=("Arial", 8), foreground="gray")
    descLabel.grid(row=2, column=0)

    # console textbox
    consoleText = ttk.Text(root, wrap="word", height=12, state="normal")
    consoleText.grid(row=3, column=0, padx=10, pady=0, sticky="ew")

    # redirect stdout and stderr to the text widget
    sys.stdout = RedirectedConsole(consoleText)
    sys.stderr = RedirectedConsole(consoleText)


    root.grid_rowconfigure(4, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()

    # reset the stdout and stderr when the GUI exits
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__