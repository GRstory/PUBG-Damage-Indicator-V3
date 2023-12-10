import math, threading
import tkinter as tk
from tkinter import ttk, PhotoImage
import firebase_admin
from firebase_admin import credentials, firestore

import weaponClass
from damageView import DamageTreeView as DV
from damageTreeView import DamageTreeView as DV2
from vehicleView import VehicleView as VV
from pubgNow import PubgNow as PN
from projectInfo import ProjectInfo as PI

cred = credentials.Certificate('myKey.json')
firebase_admin.initialize_app(cred, {
  'projectId': 'python-pubg-dmg-db',
})

class PubgDamageIndicator:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Pubg Damage Indicator")
        self.win.iconbitmap("Assets\icon.ico")
        self.win.geometry("865x450+330+190")
        self.win.resizable(False, False)
        self.db = firestore.client()

        self.mainNoteBook = ttk.Notebook(self.win)
        self.dmgCalc = ttk.Frame(self.mainNoteBook, width=700, height=400)
        #self.dmgTree = ttk.Frame(self.mainNoteBook, width=700, height=400)
        self.dmgTree2 = ttk.Frame(self.mainNoteBook, width=700, height=400)
        self.dmgVehi = ttk.Frame(self.mainNoteBook, width=700, height=400)
        self.pubgNow = ttk.Frame(self.mainNoteBook, width=700, height=400)
        self.pjcInfo = ttk.Frame(self.mainNoteBook, width=700, height=400)

        self.mainNoteBook.add(self.dmgCalc, text="계산기")
        #self.mainNoteBook.add(self.dmgTree, text="트리")
        self.mainNoteBook.add(self.dmgTree2, text="트리")
        self.mainNoteBook.add(self.dmgVehi, text="차량")
        self.mainNoteBook.add(self.pubgNow, text="유틸")
        self.mainNoteBook.add(self.pjcInfo, text="정보")

        self.setBodyImage = tk.Label()

        self.humanBodyList = []                         #바디 이미지 리스트
        self.buttonImageList = [[], [], [], [], [], []] #버튼 이미지 리스트
        self.buttonList = [[], [], [], [], [], []]      #버튼 리스트
        self.classList = [[], [], [], [], [], []]       #클래스 리스트
        self.treeList = [[], [], [], [], [], []]        #전체무기 데미지 리스트

        self.showWidget = []  # 부위별 데이터 리스트
        self.nowList =   [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] #실시간 DMG / BTK / TTK / 초기 리스트

        self.nowWeapon = [0, 0] #현재 클릭되어있는 무기

        self.nowHelmet = tk.IntVar()      #헬멧 종류
        self.nowArmor = tk.IntVar()       #조끼 종류
        self.nowArmorB = tk.BooleanVar()  #조끼 파괴 유무
        self.nowDistance = tk.IntVar()    #거리
        self.nowMode = tk.IntVar()        #데미지 모드
        self.checkShotgun = tk.IntVar()
        self.nowMode.set(4)

        #self.treeView = DV(self.dmgTree)
        self.treeView2 = DV2(self.dmgTree2)
        self.vehiView = VV(self.dmgVehi)
        self.nowView = PN(self.pubgNow)
        self.infoView = PI(self.pjcInfo)

        self.weaponInfo1 = ttk.Label(self.dmgCalc, text="총기 이름: ")
        self.weaponInfo2 = ttk.Label(self.dmgCalc, text="총기 DPS: ")
        self.weaponInfo3 = ttk.Label(self.dmgCalc, text="최소 연사 간격: ")
        self.weaponInfo4 = ttk.Label(self.dmgCalc, text="피해 감소 거리: ")

        print("LOG: __init__() Launched")
        self.CreateWidget()

    def ChangeWeaponButtonFunc(self, type, index):
        self.buttonList[type][index].config(command=lambda : self.PressedButton(type, index))

    def ChangeBodyFunc(self, num):
        self.setBodyImage.config(image=self.humanBodyList[num])

    def AddTreeData(self):
        #        머리   목    어깨    가슴  가슴2  상복부  하복부 위팔  아래팔  손    허벅지 종아리  발
        dmgDFT = [1.00, 0.75, 1.00, 1.10, 1.00, 0.95, 1.00, 0.60, 0.50, 0.30, 0.60, 0.50, 0.30]  # 기본 데미지
        dmgSET = [[2.35, 2.35, 1.00, 1.00, 1.00, 1.00, 1.00, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90],  # AR  보정치
                  [2.10, 2.10, 1.05, 1.05, 1.05, 1.05, 1.05, 1.30, 1.30, 1.30, 1.30, 1.30, 1.30],  # SMG 보정치
                  [2.30, 2.30, 1.05, 1.05, 1.05, 1.05, 1.00, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90],  # LMG 보정치
                  [1.50, 1.50, 0.90, 0.90, 0.90, 0.90, 0.90, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05],  # SG  보정치
                  [2.35, 2.35, 1.05, 1.05, 1.05, 1.05, 1.05, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95],  # DMR 보정치
                  [2.50, 2.50, 1.30, 1.30, 1.30, 1.30, 1.30, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95]]  # SR  보정치

        for type in range(len(self.classList)):
            for index in range(len(self.classList[type])):
                for i in range(13):
                    self.treeList[type].append([])
                    self.treeList[type][index] = self.classList[type][index].getDamage() * dmgDFT[i] * dmgSET[type][index]
                    self.treeList[type][index] = self.classList[type][index].getDamage() * dmgDFT[i] * dmgSET[type][index]

    def CreateButton(self, type, document, tab): #클래스, 버튼 리스트에 저장
        num = 0
        for doc in document:
            testName = doc.to_dict()
            self.classList[type].append(weaponClass.weaponData(testName['name'], testName['type'], testName['damage'], testName['rpm'], testName['dStart'], testName['dEnd'], testName['decrease'], num))
            self.buttonList[type].append(tk.Button(tab, text=self.classList[type][num].getName(), relief="flat"))
            self.buttonList[type][num].config(width=64, height=64, image=self.buttonImageList[type][num], bd=0)
            self.buttonList[type][num].grid(column=num % 4, row=num // 4)

            #print("LOG: CreateButton()", type, "-", num)
            num += 1

    def PressedButton(self, type, index):
        #        머리   목    어깨    가슴  가슴2  상복부  하복부 위팔  아래팔  손    허벅지 종아리  발
        dmgDFT = [1.00, 0.75, 1.00, 1.10, 1.00, 0.95, 1.00, 0.60, 0.50, 0.30, 0.60, 0.50, 0.30]  # 기본 데미지
        dmgSET = [[2.35, 2.35, 1.00, 1.00, 1.00, 1.00, 1.00, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90],  # AR  보정치
                  [2.10, 2.10, 1.05, 1.05, 1.05, 1.05, 1.05, 1.30, 1.30, 1.30, 1.30, 1.30, 1.30],  # SMG 보정치
                  [2.30, 2.30, 1.05, 1.05, 1.05, 1.05, 1.00, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90],  # LMG 보정치
                  [1.50, 1.50, 0.90, 0.90, 0.90, 0.90, 0.90, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05],  # SG  보정치
                  [2.35, 2.35, 1.05, 1.05, 1.05, 1.05, 1.05, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95],  # DMR 보정치
                  [2.50, 2.50, 1.30, 1.30, 1.30, 1.30, 1.30, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95]]  # SR  보정치

        self.nowWeapon = [type, index]
        for i in range(13): #DMG calculate > save in nowList[0]
            self.nowList[0][i] = self.classList[type][index].getDamage() *dmgDFT[i] * dmgSET[type][i]

            if(self.checkShotgun.get() == 1 and self.nowWeapon[0] == 3 and self.nowWeapon[1] != 5):
                self.nowList[0][i] = self.nowList[0][i] / 9

        self.EditDamage(self.nowList[0], self.nowHelmet, self.nowArmor, self.nowArmorB, self.nowDistance, self.classList[type][index].getDstart(), self.classList[type][index].getDend(), self.classList[type][index].getDecrease())

        for i in range(13): #DMG to BTK, TTK in nowList[1], nowList[2]
            try:
                self.nowList[1][i] = math.ceil(100 / self.nowList[0][i])
                self.nowList[2][i] = round(math.ceil(self.nowList[1][i]) * 60 / self.classList[type][index].getRpm(), 2)

                if(self.nowList[1][i] == 1):
                    self.nowList[2][i] = 0
            except: #ERROR
                self.nowList[1][i] = 999
                self.nowList[2][i] = 999

        for i in range(13):
            self.nowList[0][i] = round(self.nowList[0][i], 2)
            self.nowList[1][i] = round(self.nowList[1][i], 2)

        #self.PrintStat(self.nowList[0], self.nowList[1], self.nowList[2], type, index)

    def EditDamage(self, list, helmet, armor, armorB, distance, dStart, dEnd, decrease):
        if helmet.get() == 1:
            list[0] = list[0] * 0.7
            list[1] = list[1] * 0.7
        elif helmet.get() == 2:
            list[0] = list[0] * 0.6
            list[1] = list[1] * 0.6
        elif helmet.get() == 3:
            list[0] = list[0] * 0.45
            list[1] = list[1] * 0.45

        if armor.get() != 0 and armorB.get():
            for i in range(2, 7):
                list[i] *= 0.8
        elif armor.get() == 1:
            for i in range(2, 7):
                list[i] *= 0.7
        elif armor.get() == 2:
            for i in range(2, 7):
                list[i] *= 0.6
        elif armor.get() == 3:
            for i in range(2, 7):
                list[i] *= 0.45


        if distance.get() >= dStart and distance.get() < dEnd:
            for i in range(len(list)):
                list[i] = list[i] * (1 - ((distance.get() - dStart) / (dEnd - dStart)) * decrease / 100)
        elif distance.get() >= dEnd:
            for i in range(len(list)):
                list[i] = list[i] * (1 - (decrease / 100))
        elif distance.get() < dStart:
            pass


    def PrintStat(self, dmgList, btkList, ttkList, type, index):
        print("LOG: PrintStat()")
        print("LOG: 헬멧:", self.nowHelmet.get(), " 조끼:", self.nowArmor.get(), " 파괴:", self.nowArmorB.get(), " 거리:", self.nowDistance.get())
        print("LOG: 번호:", type, "-", index, "이름:", self.classList[type][index].getName())
        print("LOG: DMG:", dmgList)
        print("LOG: BTK:", btkList)
        print("LOG: TTK:", ttkList)

    def FixZeroBug(self):
        while True:
            try:
                type(self.nowDistance.get()) != int
            except:
                self.nowDistance.set(0)

    def RefreshWidget(self): #모드 반영
        while True:
            self.PressedButton(self.nowWeapon[0], self.nowWeapon[1])

            for i in range(13):
                self.showWidget[i].config(text=self.nowList[self.nowMode.get() - 1][i])

            #self.treeView.RefreshChildWidget(self.classList,  self.nowHelmet, self.nowArmor, self.nowArmorB, self.nowDistance)
            #self.treeView2.refreshTreeData(self.nowHelmet, self.nowArmor, self.nowArmorB)

            self.vehiView.RefreshDmgWidget(self.classList[self.nowWeapon[0]][self.nowWeapon[1]].getDamage())
            self.vehiView.RefreshWeaponWidget(self.classList[self.nowWeapon[0]][self.nowWeapon[1]].getName())

            self.weaponInfo1.config(text="총기 이름: " + self.classList[self.nowWeapon[0]][self.nowWeapon[1]].getName())
            self.weaponInfo2.config(text="총기 DPS: " + str(round(
                self.classList[self.nowWeapon[0]][self.nowWeapon[1]].getDamage() * self.classList[self.nowWeapon[0]][
                    self.nowWeapon[1]].getRpm() / 60)))
            self.weaponInfo3.config(text="최소 연사 간격: " + str(round(60 / self.classList[self.nowWeapon[0]][self.nowWeapon[1]].getRpm(), 4)) + "(초)")
            self.weaponInfo4.config(text="피해 감소 거리: " + str(self.classList[self.nowWeapon[0]][self.nowWeapon[1]].getDstart()) + " ~ " + str(self.classList[self.nowWeapon[0]][self.nowWeapon[1]].getDend()) + "(m)")

    def CreateWidget(self):
        self.mainNoteBook.place(x=150, y=10)

        for i in range(14):
            self.humanBodyList.append(PhotoImage(file='Assets\HumanBody_{}'.format(i) + '.png'))
        for i in range(6):
            for j in range(12):
                try:
                    self.buttonImageList[i].append(PhotoImage(file='Assets\Button_{}'.format(i) + '_{}'.format(j) + '.png'))
                except:
                    pass

        textHelmet = tk.Label(self.win, text="헬멧:")
        textArmor = tk.Label(self.win, text="조끼:")
        textArmorB = tk.Label(self.win, text="파괴:")
        textDist = tk.Label(self.win, text="거리:")

        setHelmet = ttk.Combobox(self.win, textvariable=self.nowHelmet, state="readonly", width=9)
        setArmor = ttk.Combobox(self.win, textvariable=self.nowArmor, state="readonly", width=9)
        setArmorB = ttk.Checkbutton(self.win, variable=self.nowArmorB)
        setDist = ttk.Entry(self.win, textvariable=self.nowDistance, width=12)

        setHelmet['values'] = (0, 1, 2, 3)
        setArmor['values'] = (0, 1, 2, 3)
        setHelmet.current(0)
        setArmor.current(0)

        textHelmet.place(x=10, y=200)
        setHelmet.place(x=50, y=200)
        textArmor.place(x=10, y=225)
        setArmor.place(x=50, y=225)
        textArmorB.place(x=10, y=250)
        setArmorB.place(x=50, y=250)
        textDist.place(x=10, y=275)
        setDist.place(x=48, y=275)

        pLogo = tk.PhotoImage(file="Assets\MainLogo.png")
        pLogoWidget = tk.Label(self.win, text="asdf", image=pLogo)
        pLogoWidget.image = pLogo
        pLogoWidget.place(x=9, y=305)

        ########################################### dmgCalc

        self.setBodyImage = tk.Label(self.dmgCalc, image=self.humanBodyList[13])

        buttonTabControl = ttk.Notebook(self.dmgCalc)
        tab1 = ttk.Frame(buttonTabControl)
        tab2 = ttk.Frame(buttonTabControl)
        tab3 = ttk.Frame(buttonTabControl)
        tab4 = ttk.Frame(buttonTabControl)
        tab5 = ttk.Frame(buttonTabControl)
        tab6 = ttk.Frame(buttonTabControl)

        buttonTabControl.add(tab1, text=" A R ")
        buttonTabControl.add(tab2, text=" SMG ")
        buttonTabControl.add(tab3, text=" LMG ")
        buttonTabControl.add(tab4, text=" S G ")
        buttonTabControl.add(tab5, text=" DMR ")
        buttonTabControl.add(tab6, text=" S R ")

        self.setBodyImage.place(x=5, y=5)
        buttonTabControl.place(x=155, y=10)

        ttk.Radiobutton(self.dmgCalc, text="DMG", variable=self.nowMode, value=1).place(x=155, y=240)
        ttk.Radiobutton(self.dmgCalc, text="BTK", variable=self.nowMode, value=2).place(x=155, y=260)
        ttk.Radiobutton(self.dmgCalc, text="TTK", variable=self.nowMode, value=3).place(x=155, y=280)

        db = firestore.client()

        arSeries = db.collection(u'weaponAR')
        arDocs = arSeries.stream()
        smgSeries = db.collection('weaponSMG')
        smgDocs = smgSeries.stream()
        lmgSeries = db.collection('weaponLMG')
        lmgDocs = lmgSeries.stream()
        sgSeries = db.collection('weaponSG')
        sgDocs = sgSeries.stream()
        dmrSeries = db.collection('weaponDMR')
        dmrDocs = dmrSeries.stream()
        srSeries = db.collection('weaponSR')
        srDocs = srSeries.stream()

        self.CreateButton(0, arDocs, tab1)
        self.CreateButton(1, smgDocs, tab2)
        self.CreateButton(2, lmgDocs, tab3)
        self.CreateButton(3, sgDocs, tab4)
        self.CreateButton(4, dmrDocs, tab5)
        self.CreateButton(5, srDocs, tab6)

        exData = ["머리", "목", "어깨", "가슴1", "가슴2", "상복부", "하복부", "위팔", "아래팔", "손", "허벅지", "종아리", "발", "리셋"]
        exWidget = []   #부위별 버튼 리스트

        for i in range(14): #Body Image Change Button
            exWidget.append(ttk.Button(self.dmgCalc, text=exData[i], width=5))
            exWidget[i].place(x=10 + i * 48, y=335)

        for i in range(13): #DMG / BTK / TTK Show Label
            self.showWidget.append(tk.Label(self.dmgCalc, text="0", width=6))
            self.showWidget[i].place(x=8 + i * 48, y=360)

        ttk.Checkbutton(self.dmgCalc, variable=self.checkShotgun).place(x=155, y=300)
        ttk.Label(self.dmgCalc, text="샷건: 팰릿 당 데미지").place(x=175, y=300)

        self.weaponInfo1.place(x=320, y=240)
        self.weaponInfo2.place(x=320, y=260)
        self.weaponInfo3.place(x=320, y=280)
        self.weaponInfo4.place(x=320, y=300)

        exWidget[0].config(command=lambda: self.ChangeBodyFunc(0))
        exWidget[1].config(command=lambda: self.ChangeBodyFunc(1))
        exWidget[2].config(command=lambda: self.ChangeBodyFunc(2))
        exWidget[3].config(command=lambda: self.ChangeBodyFunc(3))
        exWidget[4].config(command=lambda: self.ChangeBodyFunc(4))
        exWidget[5].config(command=lambda: self.ChangeBodyFunc(5))
        exWidget[6].config(command=lambda: self.ChangeBodyFunc(6))
        exWidget[7].config(command=lambda: self.ChangeBodyFunc(7))
        exWidget[8].config(command=lambda: self.ChangeBodyFunc(8))
        exWidget[9].config(command=lambda: self.ChangeBodyFunc(9))
        exWidget[10].config(command=lambda: self.ChangeBodyFunc(10))
        exWidget[11].config(command=lambda: self.ChangeBodyFunc(11))
        exWidget[12].config(command=lambda: self.ChangeBodyFunc(12))
        exWidget[13].config(command=lambda: self.ChangeBodyFunc(13))

        self.buttonList[0][0].config(command=lambda: self.ChangeWeaponButtonFunc(0, 0))
        self.buttonList[0][1].config(command=lambda: self.ChangeWeaponButtonFunc(0, 1))
        self.buttonList[0][2].config(command=lambda: self.ChangeWeaponButtonFunc(0, 2))
        self.buttonList[0][3].config(command=lambda: self.ChangeWeaponButtonFunc(0, 3))
        self.buttonList[0][4].config(command=lambda: self.ChangeWeaponButtonFunc(0, 4))
        self.buttonList[0][5].config(command=lambda: self.ChangeWeaponButtonFunc(0, 5))
        self.buttonList[0][6].config(command=lambda: self.ChangeWeaponButtonFunc(0, 6))
        self.buttonList[0][7].config(command=lambda: self.ChangeWeaponButtonFunc(0, 7))
        self.buttonList[0][8].config(command=lambda: self.ChangeWeaponButtonFunc(0, 8))
        self.buttonList[0][9].config(command=lambda: self.ChangeWeaponButtonFunc(0, 9))
        self.buttonList[0][10].config(command=lambda: self.ChangeWeaponButtonFunc(0, 10))
        self.buttonList[0][11].config(command=lambda: self.ChangeWeaponButtonFunc(0, 11))

        self.buttonList[1][0].config(command=lambda: self.ChangeWeaponButtonFunc(1, 0))
        self.buttonList[1][1].config(command=lambda: self.ChangeWeaponButtonFunc(1, 1))
        self.buttonList[1][2].config(command=lambda: self.ChangeWeaponButtonFunc(1, 2))
        self.buttonList[1][3].config(command=lambda: self.ChangeWeaponButtonFunc(1, 3))
        self.buttonList[1][4].config(command=lambda: self.ChangeWeaponButtonFunc(1, 4))
        self.buttonList[1][5].config(command=lambda: self.ChangeWeaponButtonFunc(1, 5))
        self.buttonList[1][6].config(command=lambda: self.ChangeWeaponButtonFunc(1, 6))
        self.buttonList[1][7].config(command=lambda: self.ChangeWeaponButtonFunc(1, 7))

        self.buttonList[2][0].config(command=lambda: self.ChangeWeaponButtonFunc(2, 0))
        self.buttonList[2][1].config(command=lambda: self.ChangeWeaponButtonFunc(2, 1))
        self.buttonList[2][2].config(command=lambda: self.ChangeWeaponButtonFunc(2, 2))
        self.buttonList[2][3].config(command=lambda: self.ChangeWeaponButtonFunc(2, 3))

        self.buttonList[3][0].config(command=lambda: self.ChangeWeaponButtonFunc(3, 0))
        self.buttonList[3][1].config(command=lambda: self.ChangeWeaponButtonFunc(3, 1))
        self.buttonList[3][2].config(command=lambda: self.ChangeWeaponButtonFunc(3, 2))
        self.buttonList[3][3].config(command=lambda: self.ChangeWeaponButtonFunc(3, 3))
        self.buttonList[3][4].config(command=lambda: self.ChangeWeaponButtonFunc(3, 4))
        self.buttonList[3][5].config(command=lambda: self.ChangeWeaponButtonFunc(3, 5))

        self.buttonList[4][0].config(command=lambda: self.ChangeWeaponButtonFunc(4, 0))
        self.buttonList[4][1].config(command=lambda: self.ChangeWeaponButtonFunc(4, 1))
        self.buttonList[4][2].config(command=lambda: self.ChangeWeaponButtonFunc(4, 2))
        self.buttonList[4][3].config(command=lambda: self.ChangeWeaponButtonFunc(4, 3))
        self.buttonList[4][4].config(command=lambda: self.ChangeWeaponButtonFunc(4, 4))
        self.buttonList[4][5].config(command=lambda: self.ChangeWeaponButtonFunc(4, 5))
        self.buttonList[4][6].config(command=lambda: self.ChangeWeaponButtonFunc(4, 6))

        self.buttonList[5][0].config(command=lambda: self.ChangeWeaponButtonFunc(5, 0))
        self.buttonList[5][1].config(command=lambda: self.ChangeWeaponButtonFunc(5, 1))
        self.buttonList[5][2].config(command=lambda: self.ChangeWeaponButtonFunc(5, 2))
        self.buttonList[5][3].config(command=lambda: self.ChangeWeaponButtonFunc(5, 3))
        self.buttonList[5][4].config(command=lambda: self.ChangeWeaponButtonFunc(5, 4))
        self.buttonList[5][5].config(command=lambda: self.ChangeWeaponButtonFunc(5, 5))

        ########################################### dmgTree

        #self.treeView.CreateTreeChild(self.dmgTree, self.classList,  self.nowHelmet, self.nowArmor, self.nowArmorB, self.nowDistance, self.classList)
        #self.treeView.CreateTreeChildName(self.dmgTree, self.classList)

        self.treeView2.createTreeDate(self.classList)

if __name__ == '__main__':
    PDI = PubgDamageIndicator()

    refreshWidgetThread = threading.Thread(target=PDI.RefreshWidget)
    refreshWidgetThread.daemon = True
    refreshWidgetThread.start()

    fixZeroBugThread = threading.Thread(target=PDI.FixZeroBug)
    fixZeroBugThread.daemon = True
    fixZeroBugThread.start()

    PDI.win.mainloop()