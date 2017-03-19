class Settings(object):

    def __init__(self, settingsPath):

        self.settingsPath = str(settingsPath)
        with open(self.settingsPath, 'r') as f:
            self.settings = f.readlines()
        self.dict = {x.split(' ')[0] : eval(x.split(' ')[1]) for x in self.settings}

    def write(self):
        with open(self.settingsPath, 'w') as f:
            for i in self.dict:
                f.write(str(i) + ' ' + str(self.dict[i]) + '\n')

        
        

if __name__ == '__main__':

    s = Settings('./settings.txt')

    print(s.dict, '\n')
    s.write()
    

        
