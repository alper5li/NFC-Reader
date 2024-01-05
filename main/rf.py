from helpers import colors
from Constants import InstructionCode
from Authenticate import Authenticate, Keys, KeyStructure, KeyTypes, Version
from comments import ATR_comment
from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest


class Reader:
    default_key = []
    GET_RESPONSE = [0xFF, 0, 00, 00]

    CLA = 0xFF  # CLASS  = MIFARE 1K
    INS_CODE = 0xCA  # INS
    P1 = 0x00  # P1   00h , 01h
    P2 = 0x00  # P2   00h
    Le = 0x00  # Length 00h (Full Length)

    #        [  CLA | INSTRUCTION CODE | P1 | P2  ]
    SELECT = [CLA, INS_CODE, P1, P2, Le]

    DF_TELECOM = [0x7F, 0x10]

    def checkReaders(self):
        if readers():
            return False
        return True

    def handleCard(self):
        cardtype = AnyCardType()
        cardrequest = CardRequest(timeout=1, cardType=cardtype)
        print("Waiting for smartcard...")
        while True:
            try:
                cardservice = cardrequest.waitforcard()
                break
            except:  # noqa: E722
                continue
        cardservice.connection.connect()

        return cardservice

    def printReader(self, cardservice):
        print(colors.YELLOW + "\nInfo:")
        print(
            "Using = ["
            + colors.GREEN
            + f"{cardservice.connection.getReader()}"
            + colors.YELLOW
            + "]"
            + colors.RESET
        )

    def printATR(self, cardservice):
        ATR = self.getATR(cardservice)
        print(
            colors.YELLOW
            + "ATR: ["
            + colors.BLUE
            + f"{toHexString(ATR)}"
            + colors.YELLOW
            + "]"
            + colors.RESET
        )

    def getATR(self, cardservice):
        ATR = cardservice.connection.getATR()
        return ATR

    def printUID(self, response):
        print(
            colors.YELLOW
            + "UID = ["
            + colors.GREEN
            + f"{toHexString(response)}"
            + colors.YELLOW
            + "]"
            + colors.RESET
        )

    def Read(self, saveOpt=False, savePath=""):
        cardservice = self.handleCard()
        self.printReader(cardservice)
        self.printATR(cardservice)
        self.checkATR(self.getATR(cardservice))

        APDU = self.SELECT
        response, sw1, sw2 = cardservice.connection.transmit(APDU)

        if sw1 == 0x90 and sw2 == 0x0:
            self.printUID(response)
            if saveOpt:
                self.readInsideAll(cardservice, savePath)
            else:
                self.readInsideAll(cardservice)

        else:
            print(
                colors.RED
                + f"Error Code [sw1: {hex(sw1)} sw2: {hex(sw2)}]"
                + colors.RESET
            )
            for _ in response:
                print(hex(_))

    def checkATR(self, ATR):
        ATR_comment()  # Hover your mosue on method to see examples

        list = toHexString(ATR).split()

        # BURAYA ATR CLASSIFICATION YAPILIP , BU DEGER DONDURULECEK
        # print(list[0])

    def printLoadingInfo(self):
        print(colors.YELLOW + "Loading Key...\n" + colors.RESET)

    def printSendingAPDUInformation(self, data):
        print(
            colors.YELLOW
            + "Sending APDU ["
            + colors.RED
            + f"{toHexString(data)}"
            + colors.YELLOW
            + "]"
            + colors.RESET
        )

    def readInsideAll(
        self,
        cardservice,
        savePath=False,
        keyTypeA=KeyTypes.KeyA,  # Optional
        keyTypeB=KeyTypes.KeyB,  # Optional
        keyA=Keys.default_Key,  # Optional
        keyB=Keys.default_Key,  # Optional
    ):
        GET_DATA = [0xFF, 0xCA, 0x00, 0x00, 0x00]

        response, sw1, sw2 = cardservice.connection.transmit(GET_DATA)

        self.printLoadingInfo()
        self.printSendingAPDUInformation(GET_DATA)
        if sw1 == 0x90 and sw2 == 0x0:
            # Switch case eklenecek ve ATR sonrasi degiskenler degistirilecek.
            dataArray = []
            for i in range(16):
                # MIFARE 1K CONT
                BLOCK_NUMBER = i * 4
                self.LoadKey(KeyStructure.VolatileMemory, 0x00, 0x06, keyA, cardservice)
                # BLOCK i   loading KEY B
                self.LoadKey(KeyStructure.VolatileMemory, 0x01, 0x06, keyB, cardservice)
                # BLOCK i   AUTHENTICATING KEY A
                self.auth(
                    Authenticate.MSB,
                    BLOCK_NUMBER,  # BLOCK NUMBER
                    0x00,  # KEY LOCATION A
                    keyTypeA,  # KEY TYPE A
                    cardservice,
                )
                # BLOCK i   AUTHENTICATING KEY B
                self.auth(
                    Authenticate.MSB,
                    BLOCK_NUMBER,  # BLOCK NUMBER
                    0x01,  # KEY LOCATION   B
                    keyTypeB,  # KEY TYPE B
                    cardservice,
                )

                self.readBinary(BLOCK_NUMBER, cardservice, dataArray)
            if savePath is not False:
                with open(savePath, "w") as file:
                    for binary in dataArray:
                        file.write(f"{binary}\n")

        else:
            print(
                colors.RED
                + f"Error Code [sw1: {hex(sw1)} sw2: {hex(sw2)}]"
                + colors.RESET
            )

    def LoadKey(self, KeyStructure, keyNumber, LC, key, cardservice):
        CLA = self.CLA
        Ins = InstructionCode.ExternalAuthenticate
        P1 = KeyStructure
        P2 = keyNumber
        Lc = LC
        Data = key
        LOAD_KEY = [CLA, Ins, P1, P2, Lc] + Data
        response, sw1, sw2 = cardservice.connection.transmit(LOAD_KEY)
        if sw1 == 0x90 and sw2 == 0x0:
            # print(f"Key Succesfully loaded for Key Number [{(P2)}]. \nKey = [{toHexString(Data)}]")
            pass
        else:
            print(
                colors.RED
                + f"Error Loading Key [sw1: {hex(sw1)} sw2: {hex(sw2)}]"
                + colors.RESET
            )

    def auth(self, msb, lsb, keyNumber, keyType, cardservice):
        CLA = self.CLA
        INS = InstructionCode.InternalAuthenticate
        P1 = 0x00
        P2 = 0x00
        Lc = 0x05

        VER = Version.version
        MSB = msb
        LSB = lsb  # Block Number
        KeyType = keyType  # KeyA , KeyB
        KeyNumber = keyNumber  # Key Location 00 - 01

        DATA = [VER, MSB, LSB, KeyType, KeyNumber]

        AUTH = [CLA, INS, P1, P2, Lc] + DATA
        response, sw1, sw2 = cardservice.connection.transmit(AUTH)

        if sw1 == 0x90 and sw2 == 0x0:
            pass
        else:
            # not authorized
            pass

    def authforCrack(self, msb, lsb, keyNumber, keyType, cardservice):
        CLA = self.CLA
        INS = InstructionCode.InternalAuthenticate
        P1 = 0x00
        P2 = 0x00
        Lc = 0x05

        VER = Version.version
        MSB = msb
        LSB = lsb               # Block Number
        KeyType = keyType       # KeyA , KeyB
        KeyNumber = keyNumber   # Key Location 00 - 01

        DATA = [VER, MSB, LSB, KeyType, KeyNumber]

        AUTH = [CLA, INS, P1, P2, Lc] + DATA
        response, sw1, sw2 = cardservice.connection.transmit(AUTH)

        if sw1 == 0x90 and sw2 == 0x0:
            return True
        else:
            return False

    def readBinary(self, blockNumber, cardservice, dataArray):
        CLA = 0xFF
        INS = InstructionCode.ReadBinary
        P1 = 0x00
        P2 = blockNumber - 1
        Le = 0x10

        notAuth = "?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??"

        for _ in range(4):
            P2 = P2 + 1
            BIN = [CLA, INS, P1, P2, Le]

            response, sw1, sw2 = cardservice.connection.transmit(BIN)
            if sw1 == 0x90 and sw2 == 0x0:
                self.printBinary(P2, response)
                dataArray.append(toHexString(response))
                pass
            else:
                self.printBinaryErr(P2, notAuth)
                dataArray.append(notAuth)

    def printBinary(self, P2, response):
        print(
            f"[{P2}] : \t"
            + colors.GREEN
            + f"{toHexString(response)} \t {self.responseRaw(response)}"
            + colors.RESET
        )

    def printBinaryErr(self, P2, notAuth):
        print(f"[{P2}] : \t" + colors.RED + f"{notAuth}" + colors.RESET)

    def responseRaw(self, resp):
        r = ""
        for i in resp:
            r += f"{i} "
        return r

    def Crack(self, keysPath):
        keys = self.getDocument(keysPath)
        cardservice = self.handleCard()
        self.printReader(cardservice)
        self.printATR(cardservice)
        self.checkATR(self.getATR(cardservice))
        print("\nStarting to brute force sector by sector ... ")
        GET_DATA = [0xFF, 0xCA, 0x00, 0x00, 0x00]

        response, sw1, sw2 = cardservice.connection.transmit(GET_DATA)
        self.printLoadingInfo()
        self.printSendingAPDUInformation(GET_DATA)
        self.printUID(response)
        if sw1 == 0x90 and sw2 == 0x0:
            for i in range(len(keys)):
                keyA = self.toDecimalList(keys[i])
                keyB = self.toDecimalList(keys[i])
                print(f"KEY A = {toHexString(keyA)}")
                print(f"KEY B = {toHexString(keyB)}")
                self.crackInsideAll(
                    cardservice, sw1, sw2, "main\save.txt", keyA, keyB
                )

        else:
            pass

    def toDecimalList(self, string):
        decimal_list = [int(string[i : i + 2], 16) for i in range(0, len(string), 2)]
        return decimal_list

    def readBinaryforCrack(self, blockNumber, cardservice, dataArray):
        CLA = 0xFF
        INS = InstructionCode.ReadBinary
        P1 = 0x00
        P2 = blockNumber - 1
        Le = 0x10

        for _ in range(4):
            P2 = P2 + 1
            # p2 = 1
            BIN = [CLA, INS, P1, P2, Le]

            response, sw1, sw2 = cardservice.connection.transmit(BIN)

            if sw1 == 0x90 and sw2 == 0x0:
                print(
                    f"[{P2}] : \t"
                    + colors.GREEN
                    + f"{toHexString(response)} \t {self.responseRaw(response)}"
                    + colors.RESET
                )
                dataArray.append(toHexString(response))
            else:
                pass

    def crackInsideAll(
        self,
        cardservice,
        sw1,
        sw2,
        savePath=False,
        keyB=Keys.default_Key,  # Optional , needs to be set in loop
        keyA=Keys.default_Key,  # Optional , needs to be set in loop
        keyTypeA=KeyTypes.KeyA,  # Optional
        keyTypeB=KeyTypes.KeyB,  # Optional
    ):
        # Switch case eklenecek ve ATR sonrasi degiskenler degistirilecek.
        dataArray = []
        for i in range(16):
            # MIFARE 1K CONT
            checkA = False
            checkB = False
            BLOCK_NUMBER = i * 4
            # BLOCK BLOCK_NUMBER   loading KEY A
            self.LoadKey(KeyStructure.VolatileMemory, 0x00, 0x06, keyA, cardservice)
            # BLOCK BLOCK_NUMBER   loading KEY B
            self.LoadKey(KeyStructure.VolatileMemory, 0x01, 0x06, keyB, cardservice)
            # BLOCK BLOCK_NUMBER   AUTHENTICATING KEY A
            checkA = self.authforCrack(
                Authenticate.MSB,
                BLOCK_NUMBER,  # BLOCK NUMBER
                0x00,  # KEY LOCATION A
                keyTypeA,  # KEY TYPE A
                cardservice,
            )
            # BLOCK BLOCK_NUMBER   AUTHENTICATING KEY B
            checkB = self.authforCrack(
                Authenticate.MSB,
                BLOCK_NUMBER,  # BLOCK NUMBER
                0x01,  # KEY LOCATION   B
                keyTypeB,  # KEY TYPE B
                cardservice,
            )
            if checkA is True and checkB is True:
                self.readBinaryforCrack(BLOCK_NUMBER, cardservice, dataArray)
                if savePath is not False:
                    with open(savePath, "w") as file:
                        for binary in dataArray:
                            file.write(f"{binary}\n")

    def crackSector(self, sector, keysPath):
        keys = self.getDocument(keysPath)
        cardservice = self.handleCard()
        self.printReader(cardservice)
        self.printATR(cardservice)
        self.checkATR(self.getATR(cardservice))
        print(f"\nStarting to brute force sector {sector} ... ")
        GET_DATA = [0xFF, 0xCA, 0x00, 0x00, 0x00]

        response, sw1, sw2 = cardservice.connection.transmit(GET_DATA)
        self.printLoadingInfo()
        self.printSendingAPDUInformation(GET_DATA)
        self.printUID(response)
        if sw1 == 0x90 and sw2 == 0x0:
            for i in range(len(keys)):
                keyA = self.toDecimalList(keys[i])
                keyB = self.toDecimalList(keys[i])
                print(f"KEY A = {toHexString(keyA)}")
                print(f"KEY B = {toHexString(keyB)}")
                self.crackInsideSector(
                    sector,cardservice,"main\save.txt", keyA, keyB
                )

        else:
            pass

    def crackInsideSector(
        self,
        sector,
        cardservice,
        savePath=False,
        keyB=Keys.default_Key,  # Optional , needs to be set in loop
        keyA=Keys.default_Key,  # Optional , needs to be set in loop
        keyTypeA=KeyTypes.KeyA,  # Optional
        keyTypeB=KeyTypes.KeyB,  # Optional
    ):
        # Switch case eklenecek ve ATR sonrasi degiskenler degistirilecek.
        dataArray = []
        # MIFARE 1K CONT
        checkA = False
        checkB = False
        BLOCK_NUMBER =  0x06
        # BLOCK BLOCK_NUMBER   loading KEY A
        self.LoadKey(KeyStructure.VolatileMemory, 0x00, 0x06, keyA, cardservice)
        # BLOCK BLOCK_NUMBER   loading KEY B
        self.LoadKey(KeyStructure.VolatileMemory, 0x01, 0x06, keyB, cardservice)
        # BLOCK BLOCK_NUMBER   AUTHENTICATING KEY A
        checkA = self.authforCrack(
            Authenticate.MSB,
            BLOCK_NUMBER,  # BLOCK NUMBER
            0x00,  # KEY LOCATION A
            keyTypeA,  # KEY TYPE A
            cardservice,
        )
        # BLOCK BLOCK_NUMBER   AUTHENTICATING KEY B
        checkB = self.authforCrack(
            Authenticate.MSB,
            BLOCK_NUMBER,  # BLOCK NUMBER
            0x01,  # KEY LOCATION   B
            keyTypeB,  # KEY TYPE B
            cardservice,
        )
        if checkA is True and checkB is True:
            self.readBinaryforCrack(BLOCK_NUMBER, cardservice, dataArray)
            if savePath is not  False:
                with open(savePath, "w") as file:
                    for binary in dataArray:
                        file.write(f"{binary}\n")

    def getDocument(self, path):
        with open(path, "r") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
        return lines
