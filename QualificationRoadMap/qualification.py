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
    
    # check do it match the level pass in 
    def isMatch(self, level) -> bool :
        return self.level == level



