from bs4 import BeautifulSoup

class Course :
    COM_SC = 'CS'
    INFO_T = 'IT'
    SOFT_E = 'SE'
    MATH = 'M'

    __labelDict = {
        "Computer Science" : COM_SC,
        "Information Technology" : INFO_T,
        "Information System" : INFO_T,
        "Software Engineering" : SOFT_E,
        "Computing" : COM_SC,
        "Math" : MATH
    }

    def __init__(self, name, link, soup=None) :
        self.name = name
        self.link = link 
        self.soup = soup if soup is not None else None
        self.label = None
        self.__setLabel()

    def __setLabel(self) -> str :
        for key in self.__labelDict :
            if key.upper() in self.name :
                self.label = self.__labelDict[key]
                break

    def isMatch(self, label) -> bool :
        return self.label == label