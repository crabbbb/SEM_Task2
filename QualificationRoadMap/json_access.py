import json
import os

class JsonAccess : 
    
    def __init__(self, filePath = None):
        # private variable
        self.__filePath = filePath if self.isValid(filePath) == True else None

    def setFilePath(self, filePath : str) : 
        if not filePath and self.isValid(filePath) :
            # the filePath enter is not null and the file is exist  
            self.__filePath = filePath

    def getFilePath(self) : 
        return self.__filePath
    
    def isJsonFile(self, filePath) :
        # split to fileName and fileExtension 
        _, ext = os.path.splitext(filePath)

        return ext.lower() == '.json' # check must be json file 
    
    def createFile(self, fileName : str) : 
        # if exist then return true without create 
        if not fileName : 
            if not self.__checkExist(filePath=f'JsonLibrary/{fileName}.json') :
                # create the file in our directory

                self.__filePath = f'JsonLibrary/{fileName}.json'

                # put empty value into json file 
                self.writeFile({})

                return True # show success 
            
        return False # unsuccess 
        
    def readFile(self) : 
        if self.isValid(self.__filePath) : 
            # file exist and filePath is valid
            with open(self.__filePath, 'r') as file :
                content = json.load(file)
            return content 
        else : 
            return None

    def writeFile(self, newData : dict) : 
        if self.isValid(self.__filePath) : 
            # file exist and filePath is valid 
            with open(self.__filePath, 'w') as file : 
                json.dump(newData, file, indent=4)
            
            return True
        else : 
            return False

    # check exist of the file
    def __checkExist(self, filePath) -> bool : 
        if filePath != None :
            return os.path.isfile(filePath) 
        else :
            # filePath is empty  
            return False
    
    def isValid(self, filePath) -> bool : 
        # false when : 
        # not json
        # filePath is empty 
        # file is not exist ( wrong file path )
        return self.__checkExist(filePath) and self.isJsonFile(filePath)
    
    def __bool__(self) : 
        return True if self.__filePath is not None else False