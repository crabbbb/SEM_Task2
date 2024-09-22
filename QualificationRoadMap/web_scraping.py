import requests 
from bs4 import BeautifulSoup
from json_access import JsonAccess
from qualification import QualificationLevel
from course import Course

class WebScrap : 
    __POSTGRADUATE = "POSTGRADUATE"
    __MASTER = "MASTER"
    __PHD = "PHD"
    __BACHELOR = "BACHELOR DEGREE"
    __DIPLOMA = "DIPLOMA"
    __FOUNDATION = "FOUNDATION"
    __headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def __init__(self, filePath) :
        self.__filePath = filePath
        self.__json = JsonAccess(self.__filePath)
        self.__root = None
        if self.__json : 
            # json exist 
            self.__rootExist()
        else : 
            raise FileNotFoundError(f"File path provide is invalid. File path > {self.__json.getFilePath()}")
        self.qualificationList = {}

    def __rootExist(self) :
        content = self.__json.readFile()
        if content.get('rootLink') is None : 
            raise Exception(f"Root link doesnot exist")
        else : 
            self.root = content['rootLink']

    def scrapAll(self) :
        # set the procedure here and check the error here 
        link = self.root + "/programmes"

        response = requests.get(link, headers=self.__headers)

        # check status code 
        if response.status_code == 200 :
            # success get content 
            soup = BeautifulSoup(response.content, 'html.parser')

            # for bachelor and diploma can get all 
            self.__getQualification(soup)

            # acess to foundation page to get the foundation 
            linkF = self.qualificationList[self.__FOUNDATION].link
            
            responseF = requests.get(linkF, headers=self.__headers)
            if responseF.status_code == 200 : 
                soupF = BeautifulSoup(responseF.content, 'html.parser')
                lList = self.__getContentLink(soupF, 1)
                # access and get header 
                # lList[0] - foundation course page link 
                lList[0] = self.__checkRedirectLink(lList[0], self.__FOUNDATION)
                responseC = requests.get(lList[0], headers=self.__headers)
                if responseC.status_code == 200 : 
                    soupC = BeautifulSoup(responseC.content, 'html.parser')
                    # get course header
                    found = self.getFoundationHeader(soupC)
                    # set into foundation course 
                    self.appendCourse(self.__FOUNDATION, name=found, link=lList[0])
                else : 
                    raise Exception(f"Non-success status code for FOUNDATION: {response.status_code}")
            else : 
                raise Exception(f"Non-success status code for {self.__FOUNDATION}: {response.status_code}")

            # for master and phd, rewrite all the redirect link
            qualification = self.qualificationList.pop(self.__POSTGRADUATE)

            responsePost = requests.get(qualification.link, headers=self.__headers)

            if responsePost.status_code == 200 : 
                soupPost = BeautifulSoup(responsePost.content, 'html.parser')
                pmlist = self.__getContentLink(soupPost, 6)

                i = 0
                for pm in pmlist : 
                    label = ""
                    if "master" in pm :
                        label = "MASTER"
                    else : 
                        label = "PHD"
                    
                    pmlist[i] = self.__checkRedirectLink(pm, label)
                    i += 1
                
                # split master and phd 
                phd = pmlist[:3]
                master = pmlist[3:]

                self.appendQualificationList(level=self.__MASTER, link=qualification.link, courseList=self.buildCourseListByLink(master))

                self.appendQualificationList(level=self.__PHD, link=qualification.link, courseList=self.buildCourseListByLink(phd))
            else : 
                raise Exception(f"Non-success status code for {self.__POSTGRADUATE}: {response.status_code}")
        else : 
            raise Exception(f"Non-success status code: {response.status_code}")

    def __getQualification(self, soup) :
        # get the programme header
        allProgrammes = soup.find('div', class_="oGuwee jymhMd Mkt3Tc")

        if allProgrammes is not None : 
            # separate all programes become array list 
            separateProgrammes = allProgrammes.find_all('li', attrs={"data-nav-level" : 2})

            for p in separateProgrammes :
                # get programmes name 
                programme = p.find('a', class_='aJHbb hDrhEe HlqNPb', href=True)

                programmeName = programme.getText().upper()
                programmeLink = self.__formatLink(programme['href'])

                # only bachelor and diploma 
                clist = self.__getCourses(p)

                if len(clist) > 0 : 
                    # inside clist have data 
                    self.appendQualificationList(level=programmeName, link=programmeLink, courseList=clist)
                else : 
                    self.appendQualificationList(level=programmeName, link=programmeLink, courseList=[])
    
    def __getCourses(self, programe) : 
        clist = []

        allCourses = programe.find('ul', class_="VcS63b")

        if allCourses is not None : 
            seperateCourse = allCourses.find_all('li', attrs={"data-nav-level" : 3})
        
            for c in seperateCourse : 
                course = c.find('a', class_="aJHbb hDrhEe HlqNPb", href=True)
        
                courseName = course.getText().upper()
                courseLink = self.__formatLink(course['href'])
                # both have then put in course 
                clist.append(Course(name=courseName, link=courseLink))

        return clist
    
    # the yellow box below
    def __getContentLink(self, soup, limit : int) : 
        # get outer box
        content = soup.find_all(class_='tyJCtd baZpAe')
        count = 0
        lList = []
            
        for element in content:
            # second filter - find the link 
            link = element.find('a', class_='fqo2vd', href=True)
            if link != None : 
                lList.append(self.__formatLink(link['href']))
                count += 1
                if count == limit :
                    break
        return lList # filter not fulfill will have [] empty array
    
    def getHeader(self, soup : BeautifulSoup) :
        header = soup.find('span', class_='GJytX C9DxTc')

        return header.getText().upper()
    
    def getPostgraduateHeader(self, soup) -> str : 
        # header = soup.find('span', class_='puwcIf C9DxTc')
        name = soup.find('span', class_='puwcIf C9DxTc')

        # name = header.find()
        return name.getText().upper()
    
    def getFoundationHeader(self, soup) : 
        header = soup.find('div', class_='CjVfdc')

        return header.getText().upper()
    
    def __checkRedirectLink(self, link, level) : 
        redirect = 'https://www.google.com/url?'
        if redirect in link : 
            # is redirect link, access redirect page and take the real link 
            response = requests.get(link, headers=self.__headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            outerBox = soup.find('div', class_='fTk7vd')
            if outerBox is not None : 
                link = outerBox.find('a', href=True)
                return link['href']
            else : 
                newlink = soup.find('body').getText()
                index = newlink.index('https')
            
                return newlink[index:]
        else : 
            # no keyword consist
            return link

    def appendQualificationList(self, level, link, courseList) :
        self.qualificationList[level] = QualificationLevel(level=level, link=link, course=courseList)
    
    def appendCourse(self, level, name, link) :
        self.qualificationList[level].appendCourse(Course(name=name, link=link))
        
    def __formatLink(self, link):
        # if start with https then no need to rewrite 
        if not link.__contains__('https://') : 
            return self.root + link
        return link
    
    def buildCourseListByLink(self, linkList) : 
        clist = []
        for l in linkList :
            response = requests.get(l, headers=self.__headers)

            soup = BeautifulSoup(response.content, 'html.parser')

            name = self.getPostgraduateHeader(soup=soup)

            clist.append(Course(name=name.upper(), link=l))
        return clist
