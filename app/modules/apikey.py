class API_Interface:
    __instance = None
    @staticmethod 
    def getInstance():
        if API_Interface.__instance == None:
            API_Interface()
        return API_Interface.__instance
    def __init__(self):
        if API_Interface.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            API_Interface.__instance = self
            self.key = 'EKO46GFZF2SFKBM7'