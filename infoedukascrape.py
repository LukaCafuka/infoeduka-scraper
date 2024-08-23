#---------------------------------------#
# Infoeduka Scraper CLI Variant         #
# By Luka Cafuka                        #
# Info can be found at z.com.hr         #
#---------------------------------------#
import argparse
from infoedukascrape_gui import *

def startScrape(path, automaticCookie, manualCookie):
    savePath = path

    rootPath = os.path.join(path, 'InfoedukaScraper')
    print(f"Directory created at: {rootPath}")

    if automaticCookie:
        print("You will need to login in order to fetch the cookie and authorize with the server")
        cookie, response = fetchJSON()
        fullData = response.get('data', [])
    else:
        cookie, response = fetchJSON(manualCookie)
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
    print("Finished!")

def main():
    parser = argparse.ArgumentParser(
        prog='Infoeduka Scraper',
        description='Scrape study materials from Infoeduka',
    )

    parser.add_argument('-p', '--path', help='the path to where the files will be downloaded', required=True)
    parser.add_argument('-a', '--automatic-cookies', help=argparse.SUPPRESS, metavar='', type=bool, default=1, required=False)
    parser.add_argument('-c', '--cookie', help='manual cookie specification' , required=False)



    args = parser.parse_args()

    if args.cookie:
        args.automatic_cookies = False

    startScrape(args.path, args.automatic_cookies, args.cookie)


if __name__ == '__main__':
    main()