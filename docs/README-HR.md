# Infoeduka Scraper
### UPOZORENJE: Ovaj softver je napravljen za studente sveučilišta Algebre
###### Ako niste student Algebre, od ovog softvera nemate koristi

![GUI](GUI.png)

### **Ovaj skrejper dohvaća materijale sa algebrinog web portala (student.algebra.hr), poznatiji kao Infoeduka** <br>
Ovaj program dolazi u dvije varijacije: **GUI i CLI**, ako niste upoznati sa radom na terminalu, preporučeno je korsititi GUI verziju, kao na slici gore.

## Instalacija
GUI verzija je preporučena za neiskusne korisnike
1. Preuzmite GUI .exe datoteku sa *releases* stranice na Github repozitoriju ili iz bin direktorija direktno u samom repozitoriju
2. Pokrenite .exe datoteku i kliknite na 'Start' gumb <br>
CLI verzija prati isti princip instalacije <br>
**Isto tako, možete direktno pokrenuti .py datoteke, samo imajte na umu da morate instalirati sve potrebne pakete koji se nalaze u `requirements.txt` datoteci, tako što u terminalu pokrenete komandu `pip install -r requirements.txt`**


## CLI Upute
Možete pokrenuti program u terminalu na sljedeće načine: `python infoedukascrape.py --path "C:\Path\To\File\Outputs"` <br> ili direktno preko .exe datoteke `.\infoedukascrape-cli.exe --path "C:\Path\To\File\Outputs"` <br>
- Koristite: `-h` ili `--help` da ispišete informacije o programu <br>
- Koristite: `-p` ili `--path` da specificirate putanju gdje će se datoteke preuzeti **Ovo je nužno** <br>
- Koristite: `-c` ili `--cookie` da manualno specificirate kolačiće, umjesto da Vas program zatraži za login preko web preglednika<br>
Ako `-c` ili `--cookie` nisu bili specificirani, program će korisnika zatražiti login informaciju preko web preglednika, kako bi mogao dobiti ispravan kolačić<br>
- Koristite: `-s` ili `--show-cookie` da ispišete svoj kolačić u terminalu, prije samog početka preuzimanja datoteka, ovo je skriveno u normalnom radu<br>

## CLI Primjeri
`.\infoedukascrape-cli.exe -p "C:\Users\myuser\Downloads\"` <br>
`.\infoedukascrape-cli.exe --path "C:\Users\myuser\Downloads\" --cookie "6hdoaedhhbgc57lld1cpd0ifq7" --show-cookie`
