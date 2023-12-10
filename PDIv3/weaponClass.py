class weaponData(object):
    def __init__(self, name, type, damage, rpm, dStart, dEnd, decrease, index):
        self.__name = name
        self.__type = type
        self.__damage = damage
        self.__rpm = rpm
        self.__dStart = dStart
        self.__dEnd = dEnd
        self.__decrease = decrease
        self.__index = index

    def getName(self):    #Weapon Name
        return self.__name
    def getType(self):    #Weapon Type
        return self.__type
    def getDamage(self):  #Damage
        return self.__damage
    def getRpm(self):     #Round Per Minute
        return self.__rpm
    def getDstart(self):  #Damage Decrease Start Position
        return self.__dStart
    def getDend(self):    #Damage Decrease End Position
        return self.__dEnd
    def getDecrease(self):
        return self.__decrease