from web_scraping import WebScrap
from anytree import Node, RenderTree
from course import Course
from qualification import QualificationLevel

class NodeData :
    def __init__(self, name, label, level) :
        self.name = name 
        self.label = label
        self.level = level

class Tree :
    __POSTGRADUATE = "POSTGRADUATE"
    __MASTER = "MASTER"
    __PHD = "PHD"
    __BACHELOR = "BACHELOR DEGREE"
    __DIPLOMA = "DIPLOMA"
    __FOUNDATION = "FOUNDATION"

    def __init__(self, edLevel, qLevel, ws : WebScrap, edqLevel=None, domain=None) :
        self.edLevel = edLevel # min
        self.qLevel = qLevel # max
        self.ws = ws
        self.edqLevel = edqLevel if edqLevel is not None else None
        self.domain = domain if domain is not None else None
        self.root = None
        self.__setRoot()


    # init root 
    def __setRoot(self) : 
        title = self.edLevel
        # if domain not none, add domain
        if self.domain is not None : 
            title += f"\n{self.edqLevel}"
        
        self.root = Node(title, data=None)
    
    def setChild(self, level, parentNode) : 
        if level == self.qLevel :
            return

        # spm -> diploma, foundation 
        nextLevel = self.checkPossibleNextLevel(level)
        # 2
        if len(nextLevel) == 0 :
            return 

        # degree
        if self.qLevel in nextLevel :
            # in same level exist, remove other only left this qLevel
            nextLevel = [self.qLevel]

        # diploma (1)
        for level in nextLevel :
            # diploma 
            q = self.ws.qualificationList[level] # diploma qualification instance 
            
            cType = []
            if parentNode == self.root and self.domain is not None : 
                cType = [self.domain]
            else :
                cType = q.getRelatedTypeOfCourse() # CS IT  

            # CS
            for ct in cType : 
                # diploma in cs, diploma in se
                ctCourse = q.getRelatedCourse(ct)
                print(f'{ct} > {ctCourse}')
                for c in ctCourse : 
                    childNode = Node(f"{c.name}", parent=parentNode, data=NodeData(c.name, ct, level))

                    # recursive 
                    self.setChild(level, childNode)

    def checkPossibleNextLevel(self, edLevel) : 
        getFoundation = ["SPM"]
        getDiploma = ["SPM", "STPM"]
        getDegree = ["FOUNDATION", "DIPLOMA", "STPM"]
        getMaster = ["BACHELOR DEGREE"]
        getPhD = ["MASTER"]

        nextlevel = []
        if edLevel in getFoundation :
            nextlevel.append("FOUNDATION")
        if edLevel in getDiploma :
            nextlevel.append("DIPLOMA")
        if edLevel in getDegree :
            nextlevel.append("BACHELOR DEGREE")
        if edLevel in getMaster :
            nextlevel.append("MASTER")
        if edLevel in getPhD :
            nextlevel.append("PHD")
        return nextlevel
