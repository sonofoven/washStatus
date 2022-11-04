import requests
from bs4 import BeautifulSoup

class Laundry:
    """Represents a laundry room with its link to the Wash Alert Site
    and its name"""

    def __init__(self, area: str, link: str):
        self.area = area
        self.link = link

    def __str__(self):
        print(f"Area: {self.area} | Link: {self.link}")

    def __eq__(self, other):
        return (other is self or
                type(other) == Laundry and
                other.area == self.area and
                other.link == self.link)

def getStatusList(laundry: Laundry) -> list[str]:
    response = requests.get(laundry.link)
    soup = BeautifulSoup(response.text, "html.parser")
    statuses = soup.find_all(class_="status")
    statusList = []
    for status in statuses:
        currentStatus = list(status)
        statusList.append(currentStatus[0])
    return statusList

def getTypeList(laundry: Laundry) -> list[str]:
    response = requests.get(laundry.link)
    soup = BeautifulSoup(response.text, "html.parser")
    types = soup.find_all(class_="type")
    typeList = []
    for tipe in types:
        currentType = list(tipe)
        typeList.append(currentType[0])
    return typeList

def getTimeList(laundry: Laundry) -> list[str]:
    response = requests.get(laundry.link)
    soup = BeautifulSoup(response.text, "html.parser")
    times = soup.find_all(class_="time")
    timeList = []
    for time in times:
        currentTime = time.text 
        currentTime = currentTime.replace(u'\xa0', u'0')
        currentTimeNoMin = currentTime.replace(" minutes left", "")
        currentTimeInt = int(currentTimeNoMin)
        timeList.append(currentTimeInt)
    return timeList

def mapStatType(types: list[str], statuses: list[str], times: list[str]) -> list[list]:
    mappedList = []
    for index in range(len(types)):
        group = [types[index], statuses[index], times[index]]
        mappedList.append(group)
    return mappedList

def formatList(mappedList: list[list]) -> str:
    washerAmount = 0
    dryerAmount = 0
    for machines in mappedList:
        if (machines[0] == "Dryer"):
            dryerAmount += 1
        else:
            washerAmount += 1
    mappedDuplicate = mappedList[:]
    mappedWashers = mappedDuplicate[:washerAmount]
    mappedDryers = mappedDuplicate[washerAmount:]
    print("\nWashers: ")
    washerNum = 1
    for machines in mappedWashers:
        print("Washer #", washerNum, " -> Status: ", machines[1]," Time Left: ", machines[2])
        washerNum += 1
    print("\nDryers: ")
    dryerNum = 1
    for machines in mappedDryers:
        print("Dryer #", dryerNum, " -> Status: ", machines[1]," Time Left: ", machines[2])
        dryerNum += 1
            
def formatListAlt(mappedList: list[list]) -> str:
    washerAmount = 0
    dryerAmount = 0
    for machines in mappedList:
        if (machines[0] == "Dryer"):
            dryerAmount += 1
        else:
            washerAmount += 1
    mappedDuplicate = mappedList[:]
    mappedWashers = mappedDuplicate[:washerAmount]
    mappedDryers = mappedDuplicate[washerAmount:]
    minLeftListW = []
    washerAvalNum = 0
    washerEndNum = 0
    washerInNum = 0

    for machines in mappedWashers:
        if (machines[1] == "Available"):
            washerAvalNum += 1
        elif (machines[1] == "End of cycle"):
            washerEndNum += 1
        else:
            washerInNum += 1
            minLeftListW.append(machines[2])
    try:    
        currentMinW = minLeftListW[0]
    except:
        currentMinW = 0

    for mins in minLeftListW:
        currentMinW = min(currentMinW, mins)
    waList = [washerAvalNum, currentMinW]
        

    minLeftListD = []
    dryerAvalNum = 0
    dryerEndNum = 0
    dryerInNum = 0

    for machines in mappedDryers:
        if (machines[1] == "Available"):
            dryerAvalNum += 1
        elif (machines[1] == "End of cycle"):
            dryerEndNum += 1
        else:
            dryerInNum += 1
            minLeftListD.append(machines[2])
    try:    
        currentMinD = minLeftListD[0]
    except:
        currentMinD = 0
    for mins in minLeftListD:
        currentMinD = min(currentMinD, mins)
    dryList = [dryerAvalNum,currentMinD]      

    return [waList, dryList]


SequoiaS = Laundry("SequoiaS", "http://washalert.washlaundry.com/washalertweb/calpoly/WASHALERtweb.aspx?location=b7263c32-7628-48c3-8729-8f1fc7e29492")
SequoiaN = Laundry("SequoiaN", "http://washalert.washlaundry.com/washalertweb/calpoly/WASHALERtweb.aspx?location=2a173c6c-076e-4c6e-afb5-3f747b67cd58")




def washOutput(Laundromat: Laundry) -> str:
    typeList = getTypeList(Laundromat)
    statusList = getStatusList(Laundromat)
    timeList = getTimeList(Laundromat)
    fullList = mapStatType(typeList, statusList, timeList) 
    final = formatListAlt(fullList)
    return final

def finalFormat(sumS: list[list[int]], sumN: list[list[int]]) -> str:
    if (sumS[0][0] == 0):
        seqSOptW = f"#{sumS[0][1]}#"
    else:
        seqSOptW = f"|{sumS[0][0]}|" 

    if (sumS[1][0] == 0):
        seqSOptD = f"#{sumS[1][1]}#"
    else:
        seqSOptD = f"|{sumS[1][0]}|" 

    if (sumN[0][0] == 0):
        seqNOptW = f"#{sumN[0][1]}#"
    else:
        seqNOptW = f"|{sumN[0][0]}|" 

    if (sumN[1][0] == 0):
        seqNOptD = f"#{sumN[1][1]}#"
    else:
        seqNOptD = f"|{sumN[1][0]}|" 

    return "S:" + seqSOptW + seqSOptD + " N:" + seqNOptW + seqNOptD

seqS = washOutput(SequoiaS)
seqN = washOutput(SequoiaN)
finalForm = finalFormat(seqS, seqN)
print(finalForm)












