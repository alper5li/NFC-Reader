def printEnum(list):
    for index, list in enumerate(list, start=0):
        if(list):
            print(f"[{index}] - {list}")
            
class colors:
    RED = '\033[91m'
    GREEN = '\033[32m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'  # Reset color to defaul
    
    
    
def Welcome():
    return "Smart Card Programming using pcsc library"