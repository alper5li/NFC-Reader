import ATR_info
import argparse
from Operation import Read,Crack,CrackSector
from helpers import Welcome

parser = argparse.ArgumentParser(description=Welcome())
parser.add_argument("--atr-info",action="store_true",help="Prints ATR information of current device")
parser.add_argument("-r", action="store", dest="save_path", const="default_value", nargs="?", help="Reads the card")
parser.add_argument("--crack",action="store",dest="keylist_path", const="default_value", nargs="?",help="Bruteforce the card with keys\n")
parser.add_argument("--crack-sector",action="store",dest="sector", const="default_value", nargs="?",help="Bruteforce specified sector with keys\n")

args = parser.parse_args()

if args.atr_info:
    ATR_info.getInfo()
    exit()
    
if args.save_path:
    if args.save_path == "default_value":
        Read()
        exit()
    else:
        print(args.save_path)
        Read(args.save_path)
        exit()

if args.keylist_path:
    if args.keylist_path == "default_value":
        Crack()
        exit()
    else:
        Crack(args.keylist_path)
        exit()    

if args.sector:
    if args.sector == "default_value":
        print("You need to specify sector number.")
        exit()
    else:
        CrackSector(args.sector)
        exit() 









    


