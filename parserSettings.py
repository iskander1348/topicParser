import json

class settings():

    def __init__(self, domain = None):
        self.loadSettingsFromFile(domain)
            

    def loadSettingsFromFile(self, domain):
        with open('settings.json', 'r') as file:
            fileText = file.read()
            data = json.loads(fileText)
            if domain in data.keys():
                self.filenameTemplate = data[domain]['filenameTemplate']
                self.encoding = data[domain]['encoding']
                self.textTag = data[domain]['textTag']
                self.headerTag = data[domain]['headerTag']
                self.headerClearTextList = data[domain]['headerClearTextList']
            else:
                self.filenameTemplate = "{path}{header}.txt"
                self.encoding = "utf-8"
                self.textTag = "p"
                self.headerTag = "h1"
                self.headerClearTextList = []