from sys import argv
import requests
import os
from bs4 import BeautifulSoup
from parserSettings import settings



class pageParser():

    def __init__(self, url):
        self.url = url
        self.rawData = ""
        self.path = ""
        self.parsedText = ""
        self.header = ""

    def setUrl(self, url):
        self.url = url
    
    def getRawData(self):
        self.rawData = requests.get(self.url).text

    def createPath(self):
        if self.url.startswith("http://"):
            self.path = self.url.replace("http://", "")
        if self.url.startswith("https://"):
            self.path = self.url.replace("https://", "")
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path))
        
    
    def getSettings(self):
        domain = self.path.split('/')[0]
        self.settings = settings(domain)

    def parseRawData(self):
        if self.rawData == "":
            self.getRawData()
        soup = BeautifulSoup(self.rawData, 'lxml')
        textTags = soup.find_all(
            self.settings.textTag)
        for textTag in textTags:
            self.parsedText += textTag.text
        headerTag = soup.find(
            self.settings.headerTag)
        self.header = headerTag.text
        #print(textTags)

    def saveParsedData(self):
        if self.path == "":
            self.createPath()
        self.getSettings()

        if self.parsedText == "":
            self.parseRawData()
        
        filename = self.settings.filenameTemplate.format(
                    **{"header": self.header,
                        "path": self.path}
                )     
        for headerClearText in self.settings.headerClearTextList:
            filename = filename.replace(headerClearText, "")
        with open(filename, 'w', encoding=self.settings.encoding) as outputFile:
            outputFile.write(self.parsedText)


if __name__ == "__main__":
    url = argv[1]
    topic = pageParser(url)
    try:
        topic.saveParsedData()
        result = 'статья {} сохранена в папку {}'
        result = result.format(topic.header, topic.path)        
    except Exception:
        result = 'при сохранении статьи возникла ошибка {}'
        result = result.format(Exception)
    print(result)