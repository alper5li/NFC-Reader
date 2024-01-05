def ATR_comment(): 
    """
    Example :
        
        ATR for MIFARE 1K = {3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 00 01 00 00 00 00 6Ah}
        
        3B = INITAL HEADER
            8Fh = T0
                80h = TD1
                    01h = TD2
                        80h = T1
                            4Fh = Tk
                                0Ch = Length
                                    [A0 00 00 03 06h] = RID 
                                        03h = Standard
                                            [00 01h] = Card Name
                                                [00 00 00 00h] = RFU
                                                    6Ah = TCK
            
        
        Where : 
            Length (YY) = 0Ch
                RID = A0 00 00 03 06h (PC/SC Workgroup)
                    Standard (SS) = 03h (ISO 14443A, Part 3)
                        Card Name (C0 .. C1) = [00 01h] (MIFARE Classic® 1K)
                            Where, Card Name (C0 .. C1)
                                00 01h: MIFARE Classic 1K
                                00 02h: MIFARE Classic 4K
                                00 03h: MIFARE® Ultralight®
                                00 26h: MIFARE Mini
                                F0 04h: Topaz and Jewel
                                F0 11h: FeliCa 212K
                                F0 12h: FeliCa 424K
                                FFh [SAK]: Undefined
    """ 
    pass

