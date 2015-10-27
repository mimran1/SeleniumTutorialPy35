from abc import ABCMeta, abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class Base(object):
    
    def __init__(self,driver):
        self.driver = driver
    
    def setSuccessor(self,successor):
        self.successor = successor
    
    #anyObject not really needed look into it
    def processRequest(self, anyObject):
        pass

#===============================================================================
# class WebDriverObject(object):
#     def __init__(self):
#         self.driver = webdriver.Firefox()
#===============================================================================
            
class NavigateToTranscript(Base):
    
    def __init__(self,username,password,driver):
        Base.__init__(self,driver)
        self.username = username
        self.password = password
        
    def processRequest(self,anyObject):
        self.startNavigation()
        self.successor.processRequest(self.getCurrentURL())
        
    
    def startNavigation(self):
        self.driver.get("https://ssb.cc.binghamton.edu/banner/twbkwbis.P_WWWLogin")
        self.driver.implicitly_wait(10)
        self.loginPaige()
        self.clickStudent()
        self.clickStudentRecords()
        self.clickOnlineAcademicTranscript()
        self.selectLevel()
        #self.endsession() 
        
    def loginPaige(self):
        #Begin - get credentials and login
        USERNAME = self.username
        PASSWORD = self.password #Get password from user input
        id = self.driver.find_element_by_id("UserID")
        passwrd = self.driver.find_element(By.NAME,"PIN")
        id.send_keys(USERNAME)
        passwrd.send_keys(PASSWORD)
        clickLogin = self.driver.find_element_by_xpath("//input[@type='submit']")
        clickLogin.click()
        #End login in
        self.driver.implicitly_wait(10)
    
    def clickStudent(self):
        #Begin - get to "Student" 
        studentTab = self.driver.find_element_by_link_text("Student")
        studentTab.click()
        #End
        self.driver.implicitly_wait(10)
     
    def clickStudentRecords(self):   
        #Begin - click "Student Records"
        studentRecords = self.driver.find_element_by_link_text("Student Records")
        studentRecords.click()
        #End
        self.driver.implicitly_wait(10)
    
    def clickOnlineAcademicTranscript(self):
        #Being - click "Online Academic Transcript"
        onlineAcademicTranscript = self.driver.find_element_by_link_text("Online Academic Transcript")
        onlineAcademicTranscript.click()
        #End
        self.driver.implicitly_wait(10)
    
   
    def selectLevel(self):
        #Begin - select Graduate then Unofficial
        transcriptLevel = self.driver.find_element_by_xpath("//select[@id='levl_id']/option[1]")
        transcriptLevel.click()
        transcriptType = self.driver.find_element_by_xpath("//select[@id='type_id']/option[1]")
        transcriptType.click()
        submit = self.driver.find_element_by_xpath("//input[@type='submit'][@value='Submit']")
        submit.click()
        #End
        self.driver.implicitly_wait(10)
    
    
    def getCurrentURL(self):
        return self.driver.current_url
    
    def endsession(self):
        self.driver.close()

class Parsing(Base):
    
    def __init__(self,driver):
        Base.__init__(self,driver)
    
    def processRequest(self,anyobject):
        self.parsePage()
        self.successor.processRequest(self.finalYearOption)
        
    
    def parsePage(self):
        table = self.driver.find_element_by_class_name("datadisplaytable")
        rows = table.find_elements_by_tag_name("tr")
        print("rows found: " ,len(rows))
        print("Extraction in progress...")
        oFile = open("writeParsedData.txt","w")
        key = ""
        termDict = {}
        courseDict = {}
        self.finalYearOption = ""
        for val in rows:
            line = val.text
            stringLine = line#.encode("utf-8")#
            wordsInline = stringLine.split()
            if len(wordsInline)!=0:
                if wordsInline[0] == "Term:":
                    key = wordsInline[1]+wordsInline[2]
                    termDict[key] = ""
                    courseDict = {}
                if wordsInline[0] == "CS" and wordsInline[1][0] == "5":
                    courseKey = wordsInline[0]+wordsInline[1]
                    if courseKey == "CS599" or courseKey == "CS595":
                        self.finalYearOption = courseKey
                    courseDict[courseKey] = ""
                    for i in range(2,len(wordsInline)):
                        courseDict[courseKey] += wordsInline[i] + " "
                    if termDict:
                        termDict[key] = courseDict
         
        for key,value in termDict.items():
            print(key + ": ")
            oFile.write(key + ": \n")
            if value:
                for key2,value2 in value.items():
                    print(key2 + ": ")
                    oFile.write(key2 + ": ")
                    print(value2)
                    oFile.write(value2 + "\n")
                print() 
                oFile.write("\n")
        
           
        oFile.close()

class NavigateToStuSchedule(Base):
    
    def __init__(self,driver):
        Base.__init__(self,driver)
    
    def processRequest(self, anyObject):
        self.termToSelect = anyObject
        self.startNavigation()
        print("Chain ends at NavigateToStuSchedule")
    
    def startNavigation(self):
        self.clickStudent()
        self.clickRegistration()
        self.clickSelectTerm()
    
    def clickStudent(self):
        #Begin - get to "Student" 
        studentTab = self.driver.find_element_by_link_text("Student")
        studentTab.click()
        #End
        self.driver.implicitly_wait(10)
    
    def clickRegistration(self):
        #Begin - get to "Registration" 
        registration = self.driver.find_element_by_link_text("Registration")
        registration.click()
        #End
        self.driver.implicitly_wait(10)
    
    def clickSelectTerm(self):
        selectTerm = self.driver.find_element_by_link_text("Select Term")
        selectTerm.click()
        self.driver.implicitly_wait(10)
    