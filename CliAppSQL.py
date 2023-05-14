from datetime import date
import datetime
import os
import os.path
#from os import path
import psutil
import subprocess as sp
import webbrowser
from haversine import haversine, Unit
from geopy.geocoders import Nominatim
import zipfile
import pathlib
from art import *
import sqlite3
import shutil
from shutil import make_archive
import PyPDF2
import matplotlib.pyplot as plt
import numpy as np
import winsound
import pandas as pd
import openpyxl



#globaalit muuttujat, että niitä voidaan käyttää metodeissa ilman
#esittelyä.
global current
current = datetime.datetime.now()
global formattime
formattime = current.strftime("%d.%m.%y %H:%M:%S ")



def title():
    #piirretään art-kirjaston avulla htos 1.0 kuvio
    print(tprint("Cli App "))
    print('Write Do.showcommands() to see available commands')

class Commands:
    
    def __init__(self,run):
        #ominaisuusmuuttuja
        self.run = run
        
        


        
#commands luokan metodit
    def opennote(self):
        sp.Popen("Notepad.exe")
    

    #halutun txt-tiedoston ja notepadin avaus,  startfile
    #komennolla toimii myös muut ohjelmat, esim. vlc
    def openapp(self,filename):
        #slashes = []
        #slash = re.sub(r'\\','/',filename)
        #final = slash.replace(" ","")
        #slashes.append(slash)
        #print(final)
        os.startfile(filename)

    
    def openbrowser(self,addr):
        webbrowser.open(addr)
        current = datetime.datetime.now()
        formattime = current.strftime("%d.%m.%y %H:%M:%S ")
        #tallennus tietokantaan
        connection = sqlite3.connect('htos.db')
        cursor = connection.execute('INSERT INTO LOG (LOGACT,TIME) VALUES (?,?)',(addr,formattime))
        
        connection.commit()
        

    #näytetään tietokannan sisältö
    def showlog(self):
        connection = sqlite3.connect('htos.db')
        cursor = connection.execute('SELECT IDNUM,LOGACT,TIME FROM LOG')
        #tietojen käynti läpi silmukalla, ilman silmukkaa eivät ole luettavassa muodossa.
        for row in cursor:
            print(row)
            
    #parametrina annettavan kansion tiedostojen zippaus
    def pack(self,zipname,folder):
        #kansio jonka sisältö zipataan
        directory = pathlib.Path(folder)
        #shutil.make_archive(zipname,"zip",folder)
          
        with zipfile.ZipFile(zipname,mode = "w") as archive:
            for filepath in directory.iterdir():
                archive.write(filepath, arcname = filepath.name)
                
        print('Zip file ', zipname, ' ready.')
                
    #unzippaus, folder param. kertoo mistä kansiosta puretaan zippi
    #where parametrilla kerrotaan sijainti johon zippi puretaan
    def unpack(self,folder,zipname,where):
        directory = pathlib.Path(folder)
        with zipfile.ZipFile(zipname, mode = 'r') as archive:
            for filepath in directory.iterdir():
                archive.extractall(where)

        print('Zip file ', zipname, ' unpack ready.')

    #vain valitun tiedoston pakkaus, toimii tällähetkellä vain samassa
    #kansiossa ohjelman kanssa olevien tiedoston osalta
    def packfile(self,folder,zipname,files):
        directory = pathlib.Path(folder)
        
        with zipfile.ZipFile(zipname, mode="w") as archive:
            archive.write(files)
            
        
                


#dirlist metodi ottaa path parametrin, eli käyttää syöttää polun
#metodin kutsussa.
    def dirlist(self,pathdir):
        print('Folder ',pathdir,' includes: ')
        print()
        for path in os.scandir(pathdir):
            if path.is_file():
                print(path.name)


    #split metodilla jaetaan / merkin kohdalta merkkijono osiin.
    #esim. c:/koodaus/testikansio polusta tulee osat c koodaus ja kansio
    #lisätään nämä listaan, käydään lista silmukassa läpi ja tulostetaan
    #listan viimeinen i[-1] alkio eli luodun kansion nimi ilman koko polkua
    def makedir(self,name):
        current = datetime.datetime.now()
        formattime = current.strftime("%d.%m.%y %H:%M:%S ")
        names = []
        if os.path.exists(name):
            print('folder is already exists! Choose a different name')
        else:
            os.mkdir(name)
            foldName = name.split("/")
            names.append(foldName)
    
        for i in names:
            print("Folder ",i[-1] , " created!" )

        #lisätään tietokantaa varten sana created muuttujaan
        name = name + ' created'
        
        
        connection = sqlite3.connect('htos.db')
        cursor = connection.execute('INSERT INTO LOG (LOGACT,TIME) VALUES (?,?)',(name,formattime))
        connection.commit()
        

    #kansion poistometodi
    def deldir(self,name):
        remname = []
        #varmistetaan poisto
        answer = input(print('Are you sure you want to delete',name, '? ','Y/N'))
        answer = answer.capitalize()
        #path.exist komennolla tarkistetaan onko parametrina annettu kansio olemassa.
        if answer == 'Y' and os.path.exists(name):
            os.rmdir(name)
            #jaetaan polun nimi osiin ja lisätään osat listaan
            foldName = name.split("/")
            remname.append(foldName)
            #näytetään listan viimeinen alkio eli pelkkä poistetun kansion nini
            for i in remname:
                print("Folder ",i[-1] , " removed!" )

            name = name + " removed"
            connection = sqlite3.connect('htos.db')
            cursor = connection.execute('INSERT INTO LOG (LOGACT,TIME) VALUES (?,?)',(name,formattime))
            connection.commit()

        elif answer != 'Y' or os.path.exists(name) == False:

            print("you answered no or path is not exists")

        

    def showcommands(self): 
        #sanakirja komennoille
        comms = {"Do.dirlist(path)":"Dir folders",
                 "Do.makeDir(path)": "Create folder",
                 "Do.deldir(path)":  "delete folder",
                 "Do.openapp(filename)":"start program",
                 "Do.openbrowser(url)":"open url in browser",
                 "Sys.info()" : "Cpu and disk information",
                 "Do.showdistanceByName(city name, city name)":"Show distance betwee two cities",
                 "Do.readcsv('csvname.csv',1,10)": "read first to rows from csv",
                 "Do.writecsv(csvname,csv,itemname,itemvalue)":"write to csv file",
                 "Do.readpdf('c:/path/filename.pdf')":"read pdf-file",
                 "Do.drawgraph(item name, value)": "Draw pie or bar charts",
                 "Do.readexcel('filename.xlsx','tablename',10)":"read firs 10 rows from excel file",

                 
                 }
        print(comms)
        
    #etäisyyden laskeminen koordinaateista
    def showdistance(self,start1:float,start2:float,end1:float,end2:float):
        start = (start1,start2)
        end = (end1,end2)
        Distance = haversine(start,end)
        print(round(Distance,2)," Kilometers")
        
    #etäisyyden lasku paikan nimellä
    def showdistanceByName(self,startCity,endCity):
        loc = Nominatim(user_agent="GetLoc")
        getLoc = loc.geocode(startCity)
        getLoc2 = loc.geocode(endCity)

        startLat = getLoc.latitude
        startLon = getLoc.longitude
        endLat =  getLoc2.latitude
        endLon = getLoc2.longitude

        start = (startLat,startLon)
        end = (endLat,endLon)

        dist = haversine(start,end)
        print('Distance between ', startCity, ' and ', endCity,  ' is ', round(dist,2),' kilometers')


        
        


    #pdf voi olla joko samassa kansiossa ohjelman kanssa tai kansio ja tiedosto annetaan parametrina. esim c:\koodaus\sample.dpf
    def readpdf(self,file):
        #directory = pathlib.Path(folder)
        pdfFileObj = open(file, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  
        # printing number of pages in pdf file
        print('Number of pages: ',pdfReader.numPages)
        pageObj = pdfReader.getPage(0)
        # extracting text from page
        print(pageObj.extractText()) 
        # closing the pdf file object
        pdfFileObj.close()

    #käyttäjän syöttämä csv-tiedosto parametrina, samoin aloitus ja lopetusrivit csv-tiedostosta
    #jotka halutaan tulostaa.
    def readcsv(self,file,start:int,stop:int):
        #poistetaan ylim. välilyönnit antamalla true arvo
        df = pd.read_csv(file,delim_whitespace = True)
        print(df.iloc[start:stop])

    def writecsv(self,filename,*argv):
        strdata = []
        numdata = []
        for item in argv:
            if type(item) == str:
                strdata.append(item)
            elif type(item) == int:
                numdata.append(item)
            elif type(item) == float:
                numdata.append(item)
                
        both = {'tuote':strdata,'hinta':numdata}
        df = pd.DataFrame(both)
        df.to_csv(filename,sep='\t',header=False, index=False)
        

    #excelin luku, parametrina tiedostonnimi ja luettava tiedoston välilehti +
    #rivimäärä joka halutaan lukea
    def readexcel(self,file,sheet,rows:int):
        df = pd.read_excel(file,sheet_name=sheet,nrows=rows)
        print(df)

    def writeexcel(self,*argv):
        rowValues=[]
        columnNames=[]
        for item in argv:
            columnNames.append(item)
            
            

        df = pd.DataFrame(columns=columnNames)
        df.to_excel('ekseli2.xlsx',sheet_name='Ekasivu')
        
        
      
        
    #*argv parametrilla metodi voi ottaa vastaan ennalta määräämättömän määrän arvoja.
    def drawgraph(self,*argv):
        mylabels = []
        values = []
        #läpikäynti silmukassa, ilman silmukaa argv:ja ei saa lisättyä listaan.
        #values = [item for item in argv]

        #käydään parametrina annetut arvot silmukassa läpi. jos arvon tyyppi
        # on str eli merkkijono, lisätään se mylabels taulukkoon. jos
        # arvo on int eli kokonaisluku tai float eli desimaali lisätään se values taulukkoon.
        for item in argv:
            
            if type(item) == str:
                mylabels.append(item)
            elif type(item) == int:
                values.append(item)
            elif type(item) == float:
                values.append(item)
                
        answer = input(' Do you want to draw pie or bar? : ')
        #käyttäjän syötteen muunnos pieniksi kirjaimiksi
        answer = answer.casefold()
        if answer == 'pie':
            plt.pie(values, labels = mylabels)
            plt.show()
            
        elif answer == 'bar':
            plt.bar(mylabels,values)
            plt.show()

    def copyfile(self,src,dst):
        #filepath = os.path.abspath(src)
        #os.path.abspath(dst)
        #source = src.replace(os.sep, '/')
        #dest = dst.replace(os.sep, '/')
        shutil.copy(src,dst)
        print('Done')

    #soitetaan beep-ääni kun käyttäjän syöttämä aika on sama kuin todellinen kellonaika, äänen kesto annetaan seconds parametrissa
    #tunnit hours ja minuutit minutes parametreissa
    def alarm(self,hours,minutes,seconds):
        while True:
            if hours == datetime.datetime.now().hour and minutes == datetime.datetime.now().minute:
                winsound.Beep(440,seconds)
                break

    #animoitu viivan piirto
    def animation(self,Range,minlimit,maxlimit,col):
        x = []
        y = []
        for i in range(Range):
            x.append(i)
            y.append(i)

            plt.xlim(minlimit,maxlimit)
            plt.ylim(minlimit,maxlimit)
	
	# Ploting graph
            plt.plot(x, y, color = col)
            plt.pause(0.01)

        plt.show()

    #tiedoston uudelleen nimeäminen
    def rename(self,current,new):
        os.rename(current,new)
        print('Rename ready ', current, ' is now ',new)

    #etsitään ja näytetään vain tiedostot joilla on haluttu pääte esim .txt
    def findonly(self,path,extension):
        for x in os.listdir(path):
            if x.endswith(extension):
                print(x)
    '''
    def findanddel(self,path,extension):
        for x in os.listdir(path):
            if x.endswith(extension):
                name = os.path.join(path,extension)
                os.remove(name)
                print('File ', x, ' deleted')
            else:
                print('file with ', extension, ' extension not found')
                '''

    def delfile(self,location):
        answer = input(print('Deleting ',location,' Are you sure? Y/N: '))
        answer = answer.capitalize()
        if answer == 'Y':
            os.remove(location)
            print('File ',location, 'deleted!')
        else:
            print('deletion aborted')
                
    #tekstitiedoston luonti ja tekstin lisäys tiedostoon
    def creatxttefile(self,fname,method,text):
        f = open(fname,method)
        f.write(text)

    def readtxtfile(self,fname):
        f = open(fname,'r')
        print(f.read())


    def asciiart(self,text):
        print(tprint(text))

            
            
        

                
            


class System:
    def __init__(self,sys):
        self.sys = sys
        
        
    def info(self):
        print(psutil.cpu_freq())
        print('CPU usage: ',psutil.cpu_percent(),' %')
        total, used, free = shutil.disk_usage("/")

        print("Total: %d GiB" % (total // (2**30)))
        print("Used: %d GiB" % (used // (2**30)))
        print("Free: %d GiB" % (free // (2**30)))


    
        
        
        
       

title()
# Help.run
# commands luokan olioita
Do = Commands("")
Help = Commands("")
# päivämäärämuotoilu strftimella
Today = Commands(date.today().strftime("%d.%m.%Y"))
Time = Commands(datetime.datetime.now().strftime("%H:%M:%S"))
#Cpu = Commands(psutil.cpu_freq())

Sys = System("")

