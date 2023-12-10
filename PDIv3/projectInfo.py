from tkinter import ttk, PhotoImage

class ProjectInfo(object):
    def __init__(self, widget):
        self.easterImageList = []
        self.easterWidget = []
        self.easterMode = False

        for i in range(3):
            self.easterImageList.append(PhotoImage(file='Assets\easterImg{}'.format(i) + '.png'))

        self.initProjectInfo(widget)

    def initProjectInfo(self, widget):
        ttk.Label(widget, text="PDI v3").place(x=10, y=10)
        ttk.Label(widget, text="제작자").place(x=10, y=50)
        ttk.Label(widget, text="특별 출현").place(x=10, y=70)
        ttk.Label(widget, text="PUBG Damage Indicator | 20221218").place(x=70, y=10)
        ttk.Label(widget, text="GRstory | 2018139012 김준명").place(x=70, y=50)
        easter = ttk.Label(widget, text="아롱이")
        easter.place(x=70, y=70)
        easter.bind("<Button-1>", lambda e: self.easterArong2(widget))

        for i in range(3):
            self.easterWidget.append(ttk.Label(widget, image=self.easterImageList[i]))

    def easterArong2(self, widget):
        if self.easterMode:
            self.easterWidget[0].place(x=10, y=800)
            self.easterWidget[1].place(x=225, y=800)
            self.easterWidget[2].place(x=440, y=800)
            self.easterMode = False
        else:
            self.easterWidget[0].place(x=10, y=190)
            self.easterWidget[1].place(x=225, y=190)
            self.easterWidget[2].place(x=440, y=190)
            self.easterMode = True