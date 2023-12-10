from tkinter import ttk

class DamageTreeView(object):
    def __init__(self, widget1):
        self.headData = ["이름", "머리", "목", "어깨", "가슴", "가슴2", "상복부", "하복부", "위팔", "아래팔", "손", "허벅지", "종아리", "발"]
        self.headWidget = []
        self.childNameWidget = []
        self.childWidget = [[], [], [], [], [], []]

        self.scrollBar = ttk.Scrollbar(widget1)
        self.CreateTreeHead(widget1)

    def CreateTreeHead(self, widget):
        for i in range(len(self.headData)):
            self.headWidget.append(ttk.Label(widget, text=self.headData[i]))
            self.headWidget[i].place(x=50 * i, y=20)

    def CreateTreeChildName(self, widget, data):
        num = 0
        for type in range(len(data)):
            for index in range(len(data[type])):
                self.childNameWidget.append(ttk.Label(widget, text=data[type][index].getName()))
                self.childNameWidget[num].place(x=0, y=50 + num*25)
                num += 1


    def CreateTreeChild(self, widget, data, helmet, armor, armorB, distance,classList):
        #        머리   목    어깨    가슴  가슴2  상복부  하복부 위팔  아래팔  손    허벅지 종아리  발
        dmgDFT = [1.00, 0.75, 1.00, 1.10, 1.00, 0.95, 1.00, 0.60, 0.50, 0.30, 0.60, 0.50, 0.30]  # 기본 데미지
        dmgSET = [[2.35, 2.35, 1.00, 1.00, 1.00, 1.00, 1.00, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90],  # AR  보정치
                  [2.10, 2.10, 1.05, 1.05, 1.05, 1.05, 1.05, 1.30, 1.30, 1.30, 1.30, 1.30, 1.30],  # SMG 보정치
                  [2.30, 2.30, 1.05, 1.05, 1.05, 1.05, 1.00, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90],  # LMG 보정치
                  [1.50, 1.50, 0.90, 0.90, 0.90, 0.90, 0.90, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05],  # SG  보정치
                  [2.35, 2.35, 1.05, 1.05, 1.05, 1.05, 1.05, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95],  # DMR 보정치
                  [2.50, 2.50, 1.30, 1.30, 1.30, 1.30, 1.30, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95]]  # SR  보정치
        num = 0
        tempData = []
        for type in range(len(data)):
            for index in range(len(data[type])):
                num += 25
                tempData = []
                for i in range(13):
                    try:
                        tempData.append(round(data[type][index].getDamage() * dmgDFT[i] * dmgSET[type][i], 2))
                        self.childWidget[type][index].append(ttk.Label(widget, text=tempData[i]))
                        self.childWidget[type][index][i].place(x=50 * (i + 1), y=25 + num)
                    except:
                        tempData.append(round(data[type][index].getDamage() * dmgDFT[i] * dmgSET[type][i], 2))
                        self.childWidget[type].append([])
                        self.childWidget[type][index].append(ttk.Label(widget, text=tempData[i]))
                        self.childWidget[type][index][i].place(x=50 * (i + 1), y=25 + num)

    def CreateScrollBar(self, win, widget):
        self.scrollBar = ttk.Scrollbar(win, orient="vertical")
        self.scrollBar.place(x=680, y=0)

    def RefreshChildWidget(self, data, helmet, armor, armorB, distance):
        #        머리   목    어깨    가슴  가슴2  상복부  하복부 위팔  아래팔  손    허벅지 종아리  발
        dmgDFT = [1.00, 0.75, 1.00, 1.10, 1.00, 0.95, 1.00, 0.60, 0.50, 0.30, 0.60, 0.50, 0.30]  # 기본 데미지
        dmgSET = [[2.35, 2.35, 1.00, 1.00, 1.00, 1.00, 1.00, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90],  # AR  보정치
                  [2.10, 2.10, 1.05, 1.05, 1.05, 1.05, 1.05, 1.30, 1.30, 1.30, 1.30, 1.30, 1.30],  # SMG 보정치
                  [2.30, 2.30, 1.05, 1.05, 1.05, 1.05, 1.00, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90],  # LMG 보정치
                  [1.50, 1.50, 0.90, 0.90, 0.90, 0.90, 0.90, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05],  # SG  보정치
                  [2.35, 2.35, 1.05, 1.05, 1.05, 1.05, 1.05, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95],  # DMR 보정치
                  [2.50, 2.50, 1.30, 1.30, 1.30, 1.30, 1.30, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95]]  # SR  보정치

        for type in range(len(data)):
            tempData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for index in range(len(data[type])):
                for i in range(13):
                    tempData[i] = round(data[type][index].getDamage() * dmgDFT[i] * dmgSET[type][i], 2)

                #self.EditDamage(tempData, helmet, armor, armorB, distance, data)

                if helmet.get() == 1:
                    tempData[0] = tempData[0] * 0.7
                    tempData[1] = tempData[1] * 0.7
                elif helmet.get() == 2:
                    tempData[0] = tempData[0] * 0.6
                    tempData[1] = tempData[1] * 0.6
                elif helmet.get() == 3:
                    tempData[0] = tempData[0] * 0.45
                    tempData[1] = tempData[1] * 0.45

                if armor.get() != 0 and armorB.get():
                    for i in range(2, 7):
                        tempData[i] *= 0.8
                elif armor.get() == 1:
                    for i in range(2, 7):
                        tempData[i] *= 0.7
                elif armor.get() == 2:
                    for i in range(2, 7):
                        tempData[i] *= 0.6
                elif armor.get() == 3:
                    for i in range(2, 7):
                        tempData[i] *= 0.45

                if distance.get() >= data[type][index].getDstart() and distance.get() < data[type][index].getDend():
                    for i in range(len(tempData)):
                        tempData[i] = tempData[i] * (1 - ((distance.get() - data[type][index].getDstart()) / (data[type][index].getDend() - data[type][index].getDstart())) * data[type][index].getDecrease() / 100)
                elif distance.get() >= data[type][index].getDend():
                    for i in range(len(tempData)):
                        tempData[i] = tempData[i] * (1 - (data[type][index].getDecrease() / 100))

                #print(data[type][index].getName(), tempData)
                for i in range(13):
                    tempData[i] = round(tempData[i], 2)
                    self.childWidget[type][index][i].config(text=tempData[i])

