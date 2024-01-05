from rf import Reader

def Read(path=""):
        
    myReader = Reader()
        
    while(myReader.checkReaders()): 
        input("No Device Found.\nPlug your device first and press any key.")
    
    if(path!=""):
        myReader.Read(True,path)
    else:
        myReader.Read()
        
  
def Crack(keysPath="main\keys.txt",savePath =False):

    myReader = Reader()
         
    while(myReader.checkReaders()): 
        input("No Device Found.\nPlug your device first and press any key.")
    
    if savePath is not False:
        myReader.Crack(keysPath,savePath)
    else:
        myReader.Crack(keysPath)        
    
# TODO
def CrackSector(sector=1,keysPath="main\keys.txt"):
    myReader = Reader()
         
    while(myReader.checkReaders()): 
        input("No Device Found.\nPlug your device first and press any key.")
        
    myReader.crackSector(sector,keysPath)