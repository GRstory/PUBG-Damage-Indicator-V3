from tkinter import ttk
import webbrowser, json, requests

class PubgNow(object):
    def __init__(self, widget):
        with open("webData.json", "r", encoding='UTF8') as f:
            self.webData = json.load(f)

        self.labelList = []
        self.initPubgNow(widget)

    def initPubgNow(self, widget):
        ttk.Label(widget, text="글씨를 누르면 해당 웹 페이지가 열립니다.").place(x=10, y=10)

        ccu = self.conCurrentUser()
        ccuWidget = ttk.Label(widget, text="배틀그라운드 현재 동접자: " + ccu)
        ccuWidget.place(x=10, y=50)
        ccuWidget.bind("<Button-1>", lambda e: self.openWeb('https://steamdb.info/app/578080/graphs/'))

        ttk.Button(widget, text="갱신", command=lambda: self.refreshCCU(ccuWidget), width=5).place(x=460, y=48)

        for i in range(3):
            self.labelList.append(ttk.Label(widget, text=self.webData[str(i)]['mark']))
            self.labelList[i].bind("<Button-1>", lambda e: self.openWeb(self.webData[str(i)]['url']))
            self.labelList[i].place(x=10, y=70 + i * 20)


    def openWeb(self, url):
        webbrowser.open_new(url)

    def conCurrentUser(self):
        header = {"Client-ID": "5DEC666ED39DCB4199BE7E7D169E09EB"} #StamAPI 키
        myQuery = 'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=578080' #요청
        myRequest = requests.get(myQuery, headers=header)
        #https://partner.steamgames.com/doc/webapi/ISteamUserStats#GetNumberOfCurrentPlayers

        if str(myRequest) == "<Response [200]>": #접속 성공
            return str(myRequest.json()['response']['player_count']) + "명     (해당 정보는 steamAPI 기준입니다.)"
        else:
            return "steamAPI와 접속을 실패했습니다."

    def refreshCCU(self, label):
        ccu = self.conCurrentUser()
        label.config(text="배틀그라운드 현재 동접자: " + ccu)