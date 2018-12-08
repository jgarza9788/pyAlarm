import os, json,datetime, re,time
from pathlib import Path

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

"""
import colorama
"""
from colorama import init,Fore, Back, Style
init()
# print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.BRIGHT + 'and in dim text')
# print(Style.RESET_ALL)
# print('back to normal now')
"""
"""


dir = os.path.dirname(__file__)
# print(dir)
settingsPath = os.path.join(dir,"alarmSettings.json").replace("\\","/")
settings = ""
alarmIndex = 0

# print(settingsPath)

def setSystemVolume(level):
    # from ctypes import cast, POINTER
    # from comtypes import CLSCTX_ALL
    # from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level,None)


def getSystemVolume():
    # from ctypes import cast, POINTER
    # from comtypes import CLSCTX_ALL
    # from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # print(volume.GetMasterVolumeLevelScalar())
    return round(volume.GetMasterVolumeLevelScalar(),4)



def createSettings():
    data = {}
    data["offTilNextDay"] = False
    data["offDay"] = ""
    data["PlayListOrSong"] = "Chop Suey!"
    data["alarms"] = []
    data["alarms"].append({
        "enable": True,
        "volume": 0.05,
        "time": 900,
        "SMTWRFS": "0111110",
        "exeDay": 0
    })
    data["alarms"].append({
        "enable": True,
        "volume": 0.05,
        "time": 915,
        "SMTWRFS": "0111110",
        "exeDay": 0
    })
    with open(settingsPath, 'w') as outfile:
        json.dump(data, outfile, indent=4)
        setSettings(data)


def getSettings():
        if os.path.isfile(settingsPath):
            with open(settingsPath) as json_file:  
                # print("allData:: \n" + str(settings) + "\n")
                return json.load(json_file)
        else:
            createSettings()
            with open(settingsPath) as f:
                return json.load(f)




def setSettings(data):
    # print("data: \n" + str(data))
    with open(settingsPath, 'w') as outfile:
        json.dump(data, outfile, indent=4)



def StartSpotify(_playList):
    os.system(os.path.join(dir,"Spotify_RunThis.vbs") + " " + _playList)



def printTimes():
    settings = getSettings()
    color = ""

    # print(Fore.LIGHTGREEN_EX + "PlayList: {item}".format(item=settings["PlayList"]))
    # print(Fore.LIGHTGREEN_EX + "File: {item}".format(item=settings["File"]))
    print(Style.RESET_ALL)

    print("#, time, SMTWRFS, enable")
    print("*******************************")

    # now = datetime.datetime.now()
    i = 0
    while i < len(settings["alarms"]):

        if settings["alarms"][i]["enable"] == False :
            color = Fore.RED
        elif settings["alarms"][i]["exeDay"] == getDay():
            color = Fore.LIGHTBLUE_EX
        else:
            color = Fore.RESET

        print(color +  "{index} | {time} | {SMTWRFS} | {enable}".format(
            index=i, time=settings["alarms"][i]["time"], SMTWRFS=settings["alarms"][i]["SMTWRFS"],enable = settings["alarms"][i]["enable"]
            ))
        i+=1
    print(Style.RESET_ALL)
    # print("\n")


def getTime(withColon = False):
    if withColon:
        return str(datetime.datetime.now().time())[:5]
    else:
        return int(str(datetime.datetime.now().time())[:5].replace(":",""))

def getDay():
    return int(str(datetime.datetime.now().date())[:10].replace("-",""))


def SMTWRFS(schedule):
    # print(schedule)
    dayOfTheWeek = datetime.date.isoweekday(datetime.datetime.now().date()) 
    # dayOfTheWeek += 1
    dayNumber = dayOfTheWeek % 7
    # print(dayNumber)
    char = schedule[dayNumber]
    # print(char)
    if char == "1":
        return True
    else:
        return False


def playAlarms():
    settings = getSettings()

    t = getTime()
    # print(t)

    d = getDay()
    # print(d)



    i = 0
    while i < len(settings["alarms"]):

        # print(SMTWRFS(settings["alarms"][i]["SMTWRFS"]) )

        #enabled and has not played today
        if settings["alarms"][i]["enable"] == True and SMTWRFS(settings["alarms"][i]["SMTWRFS"]) and settings["alarms"][i]["exeDay"] < d:
            if settings["alarms"][i]["time"] <= t and settings["alarms"][i]["time"] + 10 >= t:
                # StartSpotify("\"" + settings["PlayList"] + "\"")
                
                if re.match("[A-Z]:.*",settings["alarms"][i]["file"]):
                    os.startfile(settings["alarms"][i]["file"])
                else:
                    os.startfile(os.path.join(dir,settings["alarms"][i]["file"]))

                # os.startfile(os.path.join(dir,settings["alarms"][i]["file"]))
                settings["alarms"][i]["exeDay"] = d
                setSettings(settings)
                setSystemVolume(settings["alarms"][i]["volume"])
                print("*** playing Alarm" + str(i) + " ***")
        i+=1

def disableUntilTomorrow():
    settings = getSettings()
    t = getTime()
    d = getDay()
    i = 0
    while i < len(settings["alarms"]):
        settings["alarms"][i]["exeDay"] = d
        i+=1


def MainMenu():
    try:
        while True:
            os.system('cls')
            print( Back.LIGHTRED_EX + Fore.BLACK + Style.NORMAL + "***Press Ctrl+C to edit settings***")
            print(Back.WHITE + Fore.BLACK + Style.DIM + "CurrentTime: " + str(getTime(True)) + " ")
            print(Style.RESET_ALL)
            printTimes()
            print(Style.RESET_ALL)
            playAlarms()
            # print("string"[:2])
            time.sleep(5)
            
# print(datetime.datetime.now().time())
    except KeyboardInterrupt:
        i = 1
        os.startfile(settingsPath)
        MainMenu()

# createSettings()
MainMenu()
