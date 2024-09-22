from course import Course

class QualificationLevel : 

    def __init__(self, level, link, course=None) :
        self.level = level
        self.link = link
        self.course = [] if course is None else course

    def appendCourse(self, c : Course) : 
        self.course.append(c)
    
    # get based on label 
    def getCourse(self, label) :
        rList = []

        for c in self.course : 
            if c.isMatch(label) :
                rList.append(c)
        
        return rList
    
    def getRelatedCourse(self, label) :
        if self.level == "MASTER" and self.level == "PHD" :
            return self.course

        # spm - degree 
        cslist = [Course.COM_SC, Course.MATH, Course.SOFT_E]
        it = Course.INFO_T
        rlist = []

        if label in cslist : 
            for cs in cslist : 
                rlist = rlist + self.getCourse(cs) 
        else : 
            rlist = self.getCourse(it)
        
        return rlist
    
    def getTypeOfCourse(self) :
        # [Course, Course]
        rlist = []
        for c in self.course :
            if c.label not in rlist :  
                rlist.append(c.label)
        return rlist
    
    def getRelatedTypeOfCourse(self) : 
        return ["CS", "IT"]
    
    # check do it match the level pass in 
    def isMatch(self, level) -> bool :
        return self.level == level



