from smartcard.ATR import ATR
from smartcard.util import toHexString
from helpers import colors

def getInfo():
    atr = ATR([0x3B, 0x9E, 0x95, 0x80, 0x1F, 0xC3, 0x80, 0x31, 0xA0, 0x73,
            0xBE, 0x21, 0x13, 0x67, 0x29, 0x02, 0x01, 0x01, 0x81,
            0xCD, 0xB9])

    printWColor('ATR',atr)    
    printWColor('Historical bytes: ', toHexString(atr.getHistoricalBytes()))
    printWColor('Checksum: ', "0x%X" % atr.getChecksum())
    printWColor('Checksum OK: ', atr.checksumOK)
    printWColor('T0  supported: ', atr.isT0Supported())
    printWColor('T1  supported: ', atr.isT1Supported())
    printWColor('T15 supported: ', atr.isT15Supported())
    printWColor('TA1',atr.getTA1())
    printWColor('TB1',atr.getTB1())
    printWColor('TC1',atr.getTC1())
    printWColor('TD1',atr.getTD1())
    printWColor('Programming Voltage', atr.getProgrammingVoltage())
    
def printWColor(text,element):
        if element == False or element == None:
                print(colors.YELLOW,text,"= ["+colors.RED,element,colors.YELLOW+"]"+colors.RESET)
        else:
                print(colors.YELLOW,text,"= ["+colors.GREEN,element,colors.YELLOW+"]"+colors.RESET)
