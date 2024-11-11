import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog, Toplevel, Label, Button
import json
#ovan: importerar Tkinter-biblioteket och ger det en kortare alias(tk)
#Tkinter är ett standardbibliotek i Python för att skapa grafiska användargränssnitt.
#importerar specifika moduler från Tkinter. messagebox används för att visa dialogrutor med meddelanden
#simpledialog används för att skapa enkla inmatningsrutor för användaren

#Importerar JSON-biblioteket som möjliggör sparandet och laddningen av data i JSON-format.




class Artist: #klassen representerar en artist och har attribut för namn, instrument och en lista över band
    
    #def används för att definiera en funktion(eller en metod, när den finns inuti en klass)
    #__init__ metod som kallas en konstruktör. Använder för att initialisera ett nytt Artist-objekt när vi skapar det.
    #self är en referens till det aktuella objektet. Ger objekten unika attribut och värden
    #name är ett argument som vi skickar in för att representera artistens namn
    #instrument=None betyder att intrument är valfritt och sätts till None. Behöver inte ange instrument
    #när en artist skapas.
    #None är ett särskillt värde i Python som ofta används för att indikera att en varibel är tom eller inte har ngt värde
    #constructor: 
    def __init__(self,name, instrument=None):

        #skapar ett attribut "name" för artist-objektet.
        #self.name betyder att "name" hör till det specifika artist-objektet(inta alla artist-objekt)
        #Sätter self.name till värdet som skickas in genom argumentet "name" när objekt skapas
        self.name = name

        #skapar ett attribut "instrument" för att hålla artistens instrument. 
        #kan vara None om inget instrument angivs
        self.instrument = instrument

        #self.bands skapar en lsita som ska hålla info om de band som artisten är medlem i
        #[] betyder tom lista . fylls i när band läggs till artisten
        self.bands = []
        
        #definierar en metod. Används för att lägga till ett band till artistens bandlista
        #specifierar vilket instrument artisten spelar i det bandet.
        #self hänvisar återigen till det specifika artist-obj
        #band är ett argument som representerar banden som artisten är med i
        #instrument är ett argument som representerar vilket instrument artisten spelar i det specifika bandet
    def add_band(self, band, instrument):
        
        #lägger till ett nytt element till bands-listan
        #Inuti append-metoden skapas en dictionary
        #{'band' : band, 'instrument' : instrument} är en dictionary(nyckel-värde-par)
        #sparar två saker: bandet och instrumentet artisten spelar i det skapade bandet.
        #'band' : band innebär att nyckeln 'band' fåår värdet band(som skickas in som arg)
        #samma för 'instrument' instrument
        #dictionary {'band' : band, 'instrument' : instrument} lagras i bands-listan
        #på detta sätt kan vi hålla reda på varhe band som artisten är med i och vilket instrument de spelar där
        self.bands.append({'band' : band, 'instrument' : instrument})
    
    #klass för att representera ett band med namn och medlemmar, kopplar varje artist till ett instrument
class Band:

    #initialiserar ett band med ett namn och en tom dictionary för medlammar
    #name: (str) Bandets namn
    def __init__(self, name):
        self.name = name #sätter atributet 'name' till bandets namn
        self.members ={} #skapar en tom dictionary för bandets medlammar

    def add_member(self, artist, instrument):
        #lägger till en artist och det instrument artisten spelar till bandets medlammar

        #self.members är en dictionary där varje medlem(artist) är en nyckel och instrument är värdet.
        self.members[artist.name] = instrument #lägger till artsten i members-dictionary med instrument

#klass för att representera ett album med namn, släppår och koppling till en artist eller ett band
#klassen representerar en artist och har attribut för namn.
#har en koppling till en artist eller ett band
class Album:
    #initialiserar albumet med namn, släppår och koppling till artist eller band

    def __init__(self, name, release_year=None, artist_or_band=None):
        #name: (str) Albumets namn
        #release_year: ((init, optional) Släppåret för albumet. Standardvärde är None
        #artist_or_band: Artist eller Band, optional. Kopplingen till artist eller band. Standardvärde är None
        #Sätter lite alias till attributer
        self.name = name
        self.release_year = release_year
        self.artist_or_band = artist_or_band
def custom_confirmation(message):
    confirmation_window = Toplevel()
    confirmation_window.title('Bekräftelse')
    confirmation_window.geometry('400x200')

    Label(confirmation_window, text=message, font=('Arial' ,12)).pack(pady=20)
    Button(confirmation_window, text='OK', command=confirmation_window.destroy).pack(pady=10)

#en klass för att hantera ett bibliotek av artister, band och album
#använder library för att organisera data: håller reda på artister, band och album i form av dictionaries.
#Den har separata dictionaries för varje kategori(self.artists, self.bands, self.albums)
#central hantering: library gör att allt kan hanteras centralt. Istället för att ha separata variabler för artister, band och album, har vi ett centralt objekt som samlar all data och funktioner relaterade till
#lagra och ladda data: innehåller funktioner(save_data och load_data) som sparar datan till en JSON-fil när användaren lägger till eller ändrar ngt.

class ArtistInfoLibrary:

    def __init__(self):
        
        #initialiserar ArtistInfoLibrary med tomma dictionaries för artister, band och album
        self.artists = {}
        self.bands = {}
        self.albums ={}
        self.load_data() #laddar data när programmet startas

    #denne metod skapar en data-dictionary som strukturerar all info om artister, band och album.
    #sparar datan till data.json med json.dump
    #JSON stöder dictionary och listor
    def save_data(self):
        print('Sparar data till JSON')
        #sparar data om artister
        data = {
            'artists': {name: {'instrument': artist.instrument, 'bands': [{'band': band['band'].name, 'instrument': band['instrument']} for band in artist.bands]} for name, artist in self.artists.items()},
            'bands': {name: {'members':band.members} for name, band in self.bands.items()},
            'albums': {name: {'release_year': album.release_year, 'artist_or_band': album.artist_or_band.name if album.artist_or_band else None} for name, album in self.albums.items()}
        }
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
            print('data sparad')

    #öppnar och laddar data.json om den finns och återskapar objekten för artister, badn och album
    def load_data(self):
        #laddar data om artister, band och album från en JSON-fil om den finns.
        try:
            with open('data.json', 'r') as file:
                data = json.load(file)
                print(f'data laddad från json {data}' )

                #Återskapa artister
                for name, info in data.get('artists', {}).items():
                    print(f'laddar artist: {name} med instrument {info['instrument']}')
                    artist = Artist(name, info['instrument'])
                    self.artists[name] = artist
                #Återskapa band och kopplingar till artister
                for name, info in data.get('bands', {}).items():
                    print(f'Laddar band: {name}')
                    band = Band(name)
                    for member_name, instrument in info['members'].items():
                        if member_name in self.artists:
                            artist = self.artists[member_name]
                            band.add_member(artist, instrument)
                            artist.add_band(band, instrument)
                    self.bands[name] = band

                #Återskapa album
                for name, info in data.get('albums', {}).items():
                    print(f'Laddar album {name}')
                    release_year = info["release_year"]
                    artist_or_band_name = info["artist_or_band"]
                    artist_or_band = self.artists.get(artist_or_band_name) or self.bands.get(artist_or_band_name)
                    album = Album(name, release_year, artist_or_band)
                    self.albums[name] = album

        except FileNotFoundError:
            pass #Om filen inte finns, fortsätter vi utan att ladda ngt


    def add_artist(self, name, instrument=None):

        #Lägger till en ny artist till artists-dictionary om artisten inte redan finns
        #Artistens namn - instrument
        if name in self.artists:
            custom_confirmation(f' Fel: - Artisten {name} finns redan')
            
        else:
            self.artists[name] = Artist(name, instrument) #skapar och lägger till artist
            self.save_data()#Sparar data efter att artisten har lagts till
            custom_confirmation(f'Bekräftelse Artisten {name} har lagts till')

    def add_band(self, name):
        #lägger til ett nytt band till bands-dictionary om bandet inte finns redan

        if name in self.bands:
            messagebox.showerror(f'Fel Bandet{name} finns redan')
        else:
            self.bands[name] = Band(name)#skapar och lägger till band
            self.save_data()#sparar data efter att bandet har lagts till

            messagebox.showinfo(f'Bekräftelse Bandet{name} har lagts till')

    def remove_artist(self,name):
        if name in self.artists:
            del self.artists[name]
            self.save_data()#Sparar data efter att artisten har tagits bort
            messagebox.showinfo(f'Bekräftelse Artisten {name} har tagits bort' )
        else: 
            messagebox.showinfo(f'Fel Artisten {name} finns inte')

    def add_artist_to_band(self, artist_name, band_name, instrument):
        #Lägger til enn artist till ett band och specificerar instrumentet artisten spelar

        if artist_name in self.artists and band_name in self.bands:
            artist = self.artists[artist_name]
            band = self.bands[band_name] 
            artist.add_band(band, instrument) #Lägger till band till artisten
            band.add_member(artist, instrument)# lägger till artist till bandet
        else:
            print(f'Artisten eller bandet finns inte')

    def add_album(self, name, release_year=None, artist_or_band_name=None):
        #lägger till ett album kopplat till en artist eller ett band.

        if artist_or_band_name:
            if artist_or_band_name in self.artists:
                artist_or_band = self.artists[artist_or_band_name]
            elif artist_or_band_name in self.bands:
                artist_or_band = self.bands[artist_or_band_name]
            else:
                print('Artisten eller bandet finns inte')
                return
        else:
            artist_or_band = None
            self.albums[name] = Album(name, release_year, artist_or_band)
    
    def search_bands(self):
        #skriv ut alla band och deras medlemmar.

        for band_name, band in self.bands.items():
            print(f'Band {band_name}')
            for member_name, instrument in band.members.items():
                print(f - '{member_name} : {instrument}')

    def search_artists(self):
        #skriv ut alla artister och deras band
        for artist_name, artist in self.artists.items():
            print(f'Artist: {artist_name}')
            for band_info in artist.bands:
                band = band_info['band']
                instrument = band_info['instrument'] 
                print(f' - {band.name}: {instrument}')

    def search_albums(self):
        # skriv ut alla album och deras kopplade artist eller band
        for album_name, album in self.albums.items():
            if album.artist_or_band:
                print(f'Album: {album_name} ({album.release_year}) - Artist/Band: {album.artist_or_band.name}')
            else:
                print(f'Album: {album_name} ({album.release_year})')     

    def list_artists(self):
        return list(self.artists.keys()) 

    

#GUI-funktioner
def add_artist(library):
    name = simpledialog.askstring('Lägg till Artist', 'Ange artistens namn:')
    if not name:
        return
    instrument = simpledialog.askstring('Lägg till Artist', 'Ange instrument (valfritt):')
    library.add_artist(name, instrument)
    

def add_band(library):
    name = simpledialog.askstring('Lägg till band', 'Ange bandets namn')
    if not name:
        return
    library.add_band(name)
    

def add_artist_to_band(library):
    artist_name = simpledialog.askstring("Lägg till Artist till Band", "Ange artistens namn:")
    band_name = simpledialog.askstring("Lägg till Artist till Band", "Ange bandets namn:")
    instrument = simpledialog.askstring("Lägg till Artist till Band", "Ange instrument:")

    if artist_name and band_name and instrument:
        library.add_artist_to_band(artist_name, band_name, instrument)
        messagebox.showinfo("Bekräftelse", f"Artisten '{artist_name}' har lagts till i bandet '{band_name}' som '{instrument}'.")
    else:
        messagebox.showerror("Fel", "Alla fält måste fyllas i.")

def add_album(library):
    name = simpledialog.askstring("Lägg till Album", "Ange albumets namn:")
    release_year = simpledialog.askinteger("Lägg till Album", "Ange släppår (valfritt):")
    artist_or_band = simpledialog.askstring("Lägg till Album", "Ange artist- eller bandnamn:")
    
    if name:
        library.add_album(name, release_year, artist_or_band)
        messagebox.showinfo("Bekräftelse", f"Albumet '{name}' har lagts till.")
    else:
        messagebox.showerror("Fel", "Albumnamnet måste anges.")

def search_bands(library):
    result = "Band och medlemmar:\n"
    for band_name, band in library.bands.items():
        result += f"\n{band_name}:\n"
        for member, instrument in band.members.items():
            result += f"  - {member}: {instrument}\n"
    messagebox.showinfo("Sök Band", result)

def search_artists(library):
    result = "Artister och band:\n"
    for artist_name, artist in library.artists.items():
        result += f"\n{artist_name} spelar:\n"
        for band_info in artist.bands:
            band = band_info['band']
            instrument = band_info['instrument']
            result += f"  - {band.name} som {instrument}\n"
    messagebox.showinfo("Sök Artister", result)

def search_albums(library):
    result = 'Album och artist/band: \n'
    for album_name, album in library.albums.items():
        if album.artist_or_band:
            result += f'\n{album_name} ({album.release_year}) - Artist/Band: {album.artist_or_band.name}\n'
        else:

            result += f'\n{album_name} ({album.release_year}) \n'
        messagebox.showinfo('Sök Album', result)

def remove_artist(library):
    name = simpledialog.askstring('Ta bort Artist', 'Ange artistens namn: ' )
    if not name:
        return
    library.remove_artist(name) #anropar metoden för att ta bort artisten

def show_artists(library):
    artists = library.list_artists()
    if artists:
        messagebox.showinfo('Lista över artister', '\n'.join(artists))
    else:
        messagebox.showinfo('Lista över artister', 'Inga artister har lagts till ännu')





 #skapar huvudfönster
root = tk.Tk() #skapar ett huvudfönster för applikationen
root.title('Artist Info Library')#sätter titteln
root.geometry('800x600')#sätter storleken på fönstret  

#skapar en instans av ArtistInfoLibrary
library = ArtistInfoLibrary()

#Lägg till knappar för att interagera med systemet
#lambda: i programmet används lmabda för att skicka funktioner som argument till command-parametern i Tkinter-knapparna
#lambda: lambda skapar en anonym funktion som anropar add_artist funktionen och skcikar med library som argument.
#lambda: command=: I Tkinter kan vi tilldela en funktion till command parametern för att bestämma vad som ska hända när knappen klickas
#lambda: utan lambda skulle det vara svårt att skicka med librar som argument eftersom Ktinker endast accepterar en funktion utan arg för command-param
tk.Button(root, text='Lägg till Artist', command=lambda: add_artist(library)).pack(pady=5)
tk.Button(root, text="Lägg till Band", command=lambda: add_band(library)).pack(pady=5)
tk.Button(root, text="Lägg till Artist till Band", command=lambda: add_artist_to_band(library)).pack(pady=5)
tk.Button(root, text="Lägg till Album", command=lambda: add_album(library)).pack(pady=5)
tk.Button(root, text="Sök Band", command=lambda: search_bands(library)).pack(pady=5)
tk.Button(root, text="Sök Artister", command=lambda: search_artists(library)).pack(pady=5)
tk.Button(root, text="Sök Album", command=lambda: search_albums(library)).pack(pady=5)
tk.Button(root, text='Visa Artister', command=lambda: show_artists(library)).pack(pady=5)
tk.Button(root, text="Ta bort Artist", command=lambda: remove_artist(library)).pack(pady=5)


#startar Tkinter-huvudloop
root.mainloop()
        


        


        
