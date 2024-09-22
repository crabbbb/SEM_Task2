from json_access import JsonAccess

class Proxy : 

    # check the file 
    def __init__(self, country : str, filePath : str) : 
        self.PROXY_COUNTRY = country
        self.__json = JsonAccess(filePath)
        self.proxyList = None # Array
        self.current = None # Dict
        self.__getProxyList()
        self.__countryExist()

        self.proxyList = self.proxyList[self.PROXY_COUNTRY]
        if self.isProxyExist() : 
            # when not null and not empty then set starting 
            self.current = self.proxyList[0]

    def __countryExist(self) -> bool : 
        if self.proxyList.get(self.PROXY_COUNTRY) is None :
            raise Exception(f"Country doesnot exist. Country > {self.PROXY_COUNTRY}")

    def __getProxyList(self) : 
        if self.__json : 
            # filePath is correct and can get the content 
            self.proxyList = self.__json.readFile()
        else : 
            raise FileNotFoundError(f"File path provide is invalid. File path > {self.__json.getFilePath()}")
    
    # make the proxy become correct format 
    def __format(self, proxy : dict) : 
        return f"http://{proxy["IP"]}:{proxy["Port"]}"
    
    def __getIndex(self, proxy) : 
        return self.proxyList.index(proxy) 
    
    def __bool__(self) : 
        # check the proxyList have data or not
        return self.isProxyExist()
    
    def isProxyExist(self) -> bool : 
        return self.proxyList is not None and len(self.proxyList) > 0
    
    def getCurrentProxy(self) -> str : 
        if self.isProxyExist() : 
            return self.__format(self.current)
        
        return None
    
    def getNextProxy(self) :
        # check available 
        if self.isProxyExist() : 
            index = self.__getIndex(self.current)
            # if reach max then get the first again 
            # if not reach then get the next 
            if index < len(self.proxyList) - 1 : 
                # get next
                self.current = self.proxyList[index + 1]
            else : 
                # restart the list 
                self.current = self.proxyList[0]

            return self.__format(self.current)
        
        return None

    

