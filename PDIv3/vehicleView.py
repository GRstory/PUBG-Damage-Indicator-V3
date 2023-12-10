import tkinter as tk
from tkinter import ttk, PhotoImage
from firebase_admin import firestore

class VehicleView(object):
    def __init__(self, widget):
        self.carNameData = []
        self.carHPData1 = []
        self.carHPData2 = []
        self.carHPData3 = []
        self.carImageList = []
        self.carWidgetList = []
        self.carNameWidgetList = []
        self.carDmgWidgetList = []

        self.vvWeapon = tk.Label(widget, text="현재 선택된 무기가 없습니다.")

        self.vvMode = tk.IntVar()
        self.vvMode.set(4)

        db = firestore.client()
        carSeries = db.collection(u'carData')
        carDocs = carSeries.stream()

        for doc in carDocs:
            testName = doc.to_dict()
            self.carNameData.append(testName['name'])
            self.carHPData1.append(testName['hp1'])
            self.carHPData2.append(testName['hp2'])
            self.carHPData3.append(testName['hp3'])

        for i in range(len(self.carNameData)):
            try:
                self.carImageList.append(PhotoImage(file='Assets\car_{}'.format(i) + '.png'))
            except:
                self.carImageList.append(PhotoImage(file='Assets\car_error.png'))

        self.InitVehicleView(widget)

    def InitVehicleView(self, widget):
        self.CreateImgWidget(widget)
        self.CreateDmgWidget(widget)
        tk.Label(widget, text="BRDM은 게임 모드별로 체력이 다릅니다").place(x=10, y=10)

        self.vvWeapon.place(x=250, y=50)

        ttk.Radiobutton(widget, text="솔로", variable=self.vvMode, value=1).place(x=10, y=50)
        ttk.Radiobutton(widget, text="듀오", variable=self.vvMode, value=2).place(x=70, y=50)
        ttk.Radiobutton(widget, text="스쿼드", variable=self.vvMode, value=3).place(x=130, y=50)

    def CreateImgWidget(self, widget): #차량 이미지, 이름 위젯 생성
        for i in range(len(self.carNameData)):
            self.carWidgetList.append(tk.Label(widget, image=self.carImageList[i]))
            self.carWidgetList[i].place(x=10 + (i % 9) * 75, y=80 + (i // 9) * 105)
            self.carNameWidgetList.append(tk.Label(widget, text=self.carNameData[i]))
            self.carNameWidgetList[i].place(x=10 + (i % 9) * 75, y=145 + (i // 9) * 105)

    def CreateDmgWidget(self, widget): #차량 데미지 위젯 생성
        for i in range(len(self.carNameData)):
            self.carDmgWidgetList.append(tk.Label(widget, text="0"))
            self.carDmgWidgetList[i].place(x=10 + (i % 9) * 75, y=165 + (i // 9) * 105)

    def RefreshDmgWidget(self, weaponDMG): #차량 데미지 갱신
        for i in range(len(self.carNameData)):
            if(self.vvMode.get() == 1):
                self.carDmgWidgetList[i].config(text=str(round(self.carHPData1[i] / weaponDMG)) + "발")
            elif(self.vvMode.get() == 2):
                self.carDmgWidgetList[i].config(text=str(round(self.carHPData2[i] / weaponDMG)) + "발")
            elif(self.vvMode.get() == 3):
                self.carDmgWidgetList[i].config(text=str(round(self.carHPData3[i] / weaponDMG)) + "발")
            elif(self.vvMode.get() == 4):
                pass

    def RefreshWeaponWidget(self, weaponName): #무기 갱신
        self.vvWeapon.config(text="현재 선택된 무기: " + weaponName)