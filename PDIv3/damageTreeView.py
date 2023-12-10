import tkinter as tk
from tkinter import ttk

class DamageTreeView(object):
    def __init__(self, widget):
        self.mainTree = ttk.Treeview(widget)
        self.mainTree.pack(side='left', fill='y')
        self.mainTree["column"] = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")

        self.treeData = []

        self.scroll = ttk.Scrollbar(widget, orient="vertical", command=self.mainTree.yview)
        self.scroll.pack(side='right', fill='y')
        self.treeHead()


    def treeHead(self):
        exData = ["총기", "머리", "목", "어깨", "가슴1", "가슴2", "상복부", "하복부", "위팔", "아래팔", "손", "허벅지", "종아리", "발"]

        for i in range(14):
            self.mainTree.heading("#{}".format(i), text=exData[i])
            if (i == 0):
                self.mainTree.column("#{}".format(i), width=70)
            else:
                self.mainTree.column("#{}".format(i), width=48)

    def addTree(self, name, data):
        self.mainTree.insert("", "end", text=name, values=data)

    def createTreeDate(self, data):
        #        머리   목    어깨    가슴  가슴2  상복부  하복부 위팔  아래팔  손    허벅지 종아리  발
        dmgDFT = [1.00, 0.75, 1.00, 1.10, 1.00, 0.95, 1.00, 0.60, 0.50, 0.30, 0.60, 0.50, 0.30]  # 기본 데미지
        dmgSET = [[2.35, 2.35, 1.00, 1.00, 1.00, 1.00, 1.00, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90],  # AR  보정치
                  [2.10, 2.10, 1.05, 1.05, 1.05, 1.05, 1.05, 1.30, 1.30, 1.30, 1.30, 1.30, 1.30],  # SMG 보정치
                  [2.30, 2.30, 1.05, 1.05, 1.05, 1.05, 1.00, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90],  # LMG 보정치
                  [1.50, 1.50, 0.90, 0.90, 0.90, 0.90, 0.90, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05],  # SG  보정치
                  [2.35, 2.35, 1.05, 1.05, 1.05, 1.05, 1.05, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95],  # DMR 보정치
                  [2.50, 2.50, 1.30, 1.30, 1.30, 1.30, 1.30, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95]]  # SR  보정치


        for i in range(6):
            try:
                for j in range(12):
                    name = data[i][j].getName()
                    dmg = data[i][j].getDamage()
                    dmgList = []

                    for k in range(13):
                        dmgList.append(round(dmg * dmgDFT[k] * dmgSET[i][k], 2))

                    self.addTree(name, dmgList)
                    self.treeData.append(dmgList)
            except:
                pass


    def refreshTreeData(self, helmet, armorA, armorB):
        num = 0
        for row in self.mainTree.get_children(): #한줄씩...
            fixData = self.treeData[num]
            #print(self.treeData[num])

            if(helmet.get() == 1):
                fixData[0] *= 0.7
                fixData[1] *= 0.7
            elif(helmet.get() == 2):
                fixData[0] *= 0.6
                fixData[1] *= 0.6
            elif(helmet.get() == 3):
                fixData[0] *= 0.45
                fixData[1] *= 0.45

            if armorA.get() != 0 and armorB.get():
                for i in range(2, 7):
                    fixData[i] *= 0.8
            elif armorA.get() == 1:
                for i in range(2, 7):
                    fixData[i] *= 0.7
            elif armorA.get() == 2:
                for i in range(2, 7):
                    fixData[i] *= 0.6
            elif armorA.get() == 3:
                for i in range(2, 7):
                    fixData[i] *= 0.45

            num += 1
            #print(fixData)
            self.mainTree.item(row)["values"] = fixData

    def asdf(self): #수정 테스트
        for row in self.mainTree.get_children():
            fixData = ("0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0")
            self.mainTree.item(row)["values"] = fixData
