from __future__ import with_statement
from datetime import datetime
import os
import math 
from Tkinter import *
import tkMessageBox
import tkSimpleDialog 
from eventBasedAnimationClass import EventBasedAnimationClass
import csv 

class Patient(object):
    #This class takes in information from both the Excel Spreadsheet and the
    #AddPatientButton and loads them into the Patient Class
    def __init__(self, name,age,height,weight,firmicuteConcentration,
                     bacterioditesConcentration,lactoBascillusConcentration):
        self.name = name
        self.age = age
        self.height = height 
        self.weight = weight
        self.firmicuteConcentration = firmicuteConcentration
        self.bacterioditesConcentration = bacterioditesConcentration
        self.lactoBascillusConcentration = lactoBascillusConcentration
        self.healthyPoints = 0
        self.unhealthyPoints = 0
        self.getHealthyandUnhealthyValues()
        self.healthy = float(self.healthyPoints)/6*100
        self.unhealthy = float(self.unhealthyPoints)/6*100
        self.BMI = self.calculateBMI()
        self.doctorsNotesString = ""

    def getHealthyandUnhealthyValues(self):
        #In order to determine % Healthyness and % Unhealthyness given the 
        #dynamic variable for IBS (test condition), I created healthy ranges
        #If the patient value fell inbetween the healthy range I added a value
        #to a healthy cournt, otherwise that same value was added to an 
        #unhealthy count, these counts were then divided by a total number
        #in this particular case 6) to determine the % healthyness, unheathyness
        #These values per bacterial concentration were weighted based on 
        #importance of that bacteris in the human system. The ranges were made
        #after reading this research paper: 
        #http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3448089/
        if 10 < self.firmicuteConcentration < 50:
            self.healthyPoints +=  1
        else: 
            self.unhealthyPoints +=  1
        if 5 < self.bacterioditesConcentration < 30:
            self.healthyPoints +=  2
        else: 
            self.unhealthyPoints +=  2
        if 20 < self.lactoBascillusConcentration < 60:
            self.healthyPoints +=  3
        else: 
            self.unhealthyPoints +=  3

    def calculateBMI(self):
        #calculates BMI based of equation from this website:
        #http://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/
        #index.html?s_cid=tw_ob064
        return round(703*float(self.weight/((self.height*12)**2)),2)

    def getName(self):
        #gets specific patient's name
        return self.name

    def __str__(self):
        return "%s" % (self.name)

    def __repr__(self):
        return str(self)

#Dialog Boxes were created for LogIn, AddingPatients, and DeltingPatients
#I read this source: http://www.java2s.com/Code/Python/GUI-Tk/
#UseEntrywidgetsdirectlyandlayoutbyrows.htm to learn how to create a 
#dialog box, however, getting information from dialogbox, and associating
#functions with these values was done by me

class LoginPopUp(object):
    #Get Username and Password input, compares it to legal values
    #1. If userinput is legal he/she can have access to Doctor&Patient Screen    
    #2. Else the program returns back to the log in, and the user does not 
    #have access to the Doctor and Patient Screens
    def __init__(self, parent):
        self.parent = parent
        self.fields = ('Username', 'Password')

    def isValidLogin(self, userName, password):
        #determines if login is valid
        checkUsername = userName
        checkPassword = password
        if ("Ruchi" == checkUsername and "ruchiisawesome" == checkPassword
            or "Robert" == checkUsername and "robertisawesome" == checkPassword):
            return True 
        else:
            return False 

    def getUserNameAndPassword(self,entries, root):
        #gets user input to determine validity
        userName = entries['Username'].get()
        password = entries['Password'].get()
        self.userEntry = (userName, password)
        if self.isValidLogin(userName, password):
            self.parent.ChangetoDoctorMode()
        root.destroy()
        
    def makeform(self, root, fields):
        #creates the dialog box
        entries = {}
        for field in self.fields:
            row = Frame(root)
            lab = Label(row, width= 22, text= field+": ", anchor = 'w')
            if field == "Username":
                ent = Entry(row, show = "")
                ent.insert(0,"")
                row.pack(side=TOP, fill=X, padx=5, pady=5)
                lab.pack(side=LEFT)
                ent.pack(side=RIGHT, expand=YES, fill=X)
                entries[field] = ent
            elif field == "Password":
                ent.insert(0,"")
                ent = Entry(row, show = "*") #prevents user from seeing pswd.
                row.pack(side=TOP, fill=X, padx=5, pady=5)
                lab.pack(side=LEFT)
                ent.pack(side=RIGHT, expand=YES, fill=X)
                entries[field] = ent
        return entries

    def run(self):
        #runs dialogbox, to get information from userinput
        root = Tk()
        root.update_idletasks()
        ents = self.makeform(root, self.fields)
        b2 = Button(root, text='Submit',
             command=(lambda e=ents: self.getUserNameAndPassword(e,root)))
        b2.pack(side=LEFT, padx=5, pady=5)
        root.mainloop()
        
class AddPatientPopUp(object):
    #When the Add Patient button is clicked in the patient mode of my program
    #This dialog box will pop with various fields, allowing the user to 
    #insert patient specific data. This data will then be saved into the program
    #When the window is close and reopened, the patient information will have 
    #been stored along with its appropriate visuals

   def __init__(self,parent):
       # parent to Animation class allows this class to inherit all methods
       #written in the EMR Animation class
       #Init also extablishes the fields for user input
       self.parent= parent 
       self.fields = ('Name','Age','Height','Weight','FirmicuteConcentration', 
        'BacterioditesConcentration', 'LactoBascillusConcentration')
      
   def addInfo(self, entries,root):
    #Gets user input and saves it as and instance of a self.patients list
    #as well as a list inside a dataList
       name = entries['Name'].get()
       #values converted to floats for subsequent caluclations and graphics
       age = float(entries['Age'].get())
       height = float(entries['Height'].get())
       weight = float(entries['Weight'].get())
       FirmicuteConcentration = float(entries['FirmicuteConcentration'].get())
       BacterioditesConcentration=float(
        entries['BacterioditesConcentration'].get())
       LactoBascillusConcentration = float(
        entries['LactoBascillusConcentration'].get())
       newPatient = Patient(name, age, height, weight, 
        FirmicuteConcentration, BacterioditesConcentration, 
        LactoBascillusConcentration)
       newData = [name, age, height, weight, FirmicuteConcentration, 
       BacterioditesConcentration, LactoBascillusConcentration ]
       self.newPatient = newPatient
       self.newData = newData
       self.parent.saveNewPatientInfo(newPatient, newData)
       root.destroy()

   def getPatient(self):
       return self.newPatient
    
   def makeform(self, root, fields):
    #creates the dialog box
      entries = {}
      for field in self.fields:
         row = Frame(root)
         lab = Label(row, width=22, text=field+": ", anchor='w')
         ent = Entry(row)
         ent.insert(0,"0")
         row.pack(side=TOP, fill=X, padx=5, pady=5)
         lab.pack(side=LEFT)
         ent.pack(side=RIGHT, expand=YES, fill=X)
         entries[field] = ent
      return entries

   def run(self):
    #runs dialogbox, to get information from userinput
      root = Tk() #Toplevel(self.parentroot)
      ents = self.makeform(root, self.fields)
      b2 = Button(root, text='Save',
             command=(lambda e=ents: self.addInfo(e,root)))
      b2.pack(side=LEFT, padx=5, pady=5)
      root.mainloop()

class DeletePatientPopUp(object):
    #This function takes in the Name of the patient that is going to be deleted
    #It then makes modifications to the self.patients list and the self.dataList
    #So that when the program is rerun, the patient instance is deleted from
    #the program enitrely
    def __init__(self,parent):
        #establishes the field of input 
        #uses the EMRAnimation class as a parent to deleter patient instance
        #for the self.patients list
        self.parent= parent 
        self.fields = ('Name',)

    def deleteInfo(self, entries,root):
        #gets the name of the patient to be deletd and deletes that instance
        name = entries['Name'].get()
        self.parent.deletePatient(name)
        root.destroy()

    def getPatient(self):
        return self.newPatient
      
    def makeform(self, root, fields):
        #makes the dialog box
        entries = {}
        for field in self.fields:
           row = Frame(root)
           lab = Label(row, width=22, text=field+": ", anchor='w')
           ent = Entry(row)
           ent.insert(0,"")
           row.pack(side=TOP, fill=X, padx=5, pady=5)
           lab.pack(side=LEFT)
           ent.pack(side=RIGHT, expand=YES, fill=X)
           entries[field] = ent
        return entries

    def run(self):
        #runs dialog box to get information
        root = Tk() #Toplevel(self.panrentroot)
        ents = self.makeform(root, self.fields)
        b2 = Button(root, text='Save',
               command=(lambda e=ents: self.deleteInfo(e,root)))
        b2.pack(side=LEFT, padx=5, pady=5)
        root.mainloop()


class EMRAnimation(EventBasedAnimationClass):
    def __init__(self):
        self.loadPatients()
        self.width = 700
        self.height = 600
        self.loginSuccessful = False 
        super(EMRAnimation,self).__init__(self.width, self.height)
    
    def loadPatients(self):
        #This takes values from an Excel file and saves them as variables
        #of the Patient instance in the EMRAnimation class so they can be 
        #used for subsequent calculations and graphics
        #I read this source to learn how to write into an ExcelSpreadsheet
        #using Python: https://docs.python.org/2/library/csv.html
        #However, the method of parsing is origional
        with open('/Users/DejaDvD/Desktop/AsthanaTP3/testcvs.csv', 'rU') as csvfile:
            patients = []
            patientsNames = []
            newDataList = []
            patientInfo = (csv.reader(csvfile, delimiter = ' ', quotechar='|', 
                dialect=csv.excel_tab))
            for row in patientInfo:
                result = row[0]
                for char in xrange(len(result)):
                    if result[char] == ',':
                        newResult = result.replace(',',' ')
                        newResult = result.replace('"', '')
                dataList = newResult.split(',')
                newDataList.append(dataList)
                name = dataList[0]
                age = float(dataList[1])
                height = float(dataList[2]) 
                weight = float(dataList[3]) 
                firmicuteConcentration = float(dataList[4])
                bacterioditesConcentration = float(dataList[5])
                lactoBascillusConcentration = float(dataList[6])
                patients.append(Patient(name,age,height,weight,
                    firmicuteConcentration,
                    bacterioditesConcentration,
                    lactoBascillusConcentration))
        self.patients = patients
        self.dataList = newDataList
        

    def ChangetoDoctorMode(self):
        #method to change mode to doctorMode, and load Doctor'sScreen
        self.mode = "doctorMode"

    def drawDate(self):
        #draws the date using notes on stringFormatting
        #read notes here: https://docs.python.org/2/library/datetime.html
        getDate= datetime.now()
        if self.mode == "doctorMode":
            self.Date = getDate.strftime('%A \n %B %d, %Y')
            self.canvas.create_text(500,50,text = self.Date, 
                font="Times 20 bold")

    def loadHelpScreen(self):
        return '''
Welcome to the Doctor's Screen of EasyMed. Included in this page
are (1) a description of the test condition, (2) a Scrollbar 
containing patients' names, (3) an AddPatient Button, (4) a 
LogOut button, and (5) a Next button. Start by Choosing a Patient 
from the Scrollbar on the bottom of the Doctor's Screen. Next, press
the GO button to view that patient's profile on a specific Patient 
Screen. Information about this patient was loaded from one of two 
locations: (1) an EXCEL spreadsheet or (2) the Add Patients from
(attained by clicking the Add Patints button on the Doctor's Screen
and entering patint information). In the Patient's Screen, you can see
values for (1) static variables (eg. name, age, height, or weight) or 
(2) dynamic data (eg. BodyMassIdex, FirmicuteConcentration, 
BacterioditesConcentration, and LactoBascillusConcentration). In the 
Doctor's Notes section you can add messages that will be saved and
reappear if you close the window and run the program again. Lastly, you 
can click on the Back button to return to the Doctor's screen or the LogOut 
button to exit the program. Please note if you are on the Doctor's Screen 
you can only press the Next button (to access Patient Specific Screen) only 
after you have chosen the patient and pressed the GO button. This is 
because the selected Patient Instance has to be established before you 
can switch between the Patient's Screen and the Doctor's Screen.
'''
    def drawHelpScreen(self):
        self.canvas.create_rectangle(100,100,600,500, fill = "light cyan")
        self.canvas.create_text(360,300, text = self.loadHelpScreen(), 
            font = "BellMT 15")

    def ChangeToPatientMode(self):
        #This method switches from any mode to the patient mode
        #It is used when the "Next" Button is pressed
        self.mode = "patientMode"

    def switchHelpScreen(self):
        #This method is used when mouse is pressed in the help screen
        #it switches the mode between the help screen and the Doctor'sScreen
        if self.mode == "doctorMode":
            self.mode = "helpScreenMode"
        elif self.mode == "helpScreenMode":
            self.mode = 'doctorMode'


    def addPatient(self,newPerson):
        #adds new patent to the self.patients list
        self.patients.append(newPerson)

    def onButtonPressed(self,patient):
        #In the doctorsNotes section of the program, this fucntions allows
        #the user input text specific to that patient and save this text
        #for the next time that the program is run
        self.patient = patient
        self.mode = "patientMode"
        path = "PatientFiles" + os.sep + "%s's Doctor's Note.txt"%(self.patient)
        if (not os.path.exists("PatientFiles")):
            os.makedirs("PatientFiles")
            contents = "None"
            self.writeFile(path, contents)
            self.patient.doctorsNotesString = self.readFile(path)
        elif (os.path.exists(path)):
            self.patient.doctorsNotesString = self.readFile(path)
        self.redrawAll()

    def updateNote(self):
        #This method allows the user to update and save the updats to the 
        #Doctor's notes section of the patient mode   
        path = "PatientFiles" + os.sep + "%s's Doctor's Note.txt"%(self.patient)
        self.writeFile(path, self.patient.doctorsNotesString)

    def saveNewPatientInfo(self, patient, data):
        #This function takes input from the dialog box and saves the variables
        #by writing the infomation into the ExcelSpreadSheet
        self.patients.append(patient)
        self.dataList.append(data)
        dataEntry = self.dataList   
        with open('/Users/DejaDvD/Desktop/AsthanaTP3/testcvs.csv', 'wb') as csvfile:
            spamwriter= csv.writer(csvfile, delimiter = ',')
            for i in xrange(len(dataEntry)):
                spamwriter.writerow(dataEntry[i])

    def deletePatient(self,name):
        #This function allows the user to delete patients by getting the name
        #of the patient to be deleted and removing the instance and the data
        #associated with that patient 
        for i in self.patients:
            if str(i) == name:
                self.patients.remove(i)
        for patientInfo in xrange(len(self.dataList)):
          if name in self.dataList[patientInfo]:
            removePatient = self.dataList[patientInfo]
            self.dataList.remove(removePatient)
            dataEntry = self.dataList 
            with open('/Users/DejaDvD/Desktop/AsthanaTP3/testcvs.csv', 'wb') as csvfile:
                spamwriter= csv.writer(csvfile, delimiter = ',')
                for i in xrange(len(dataEntry)):
                    spamwriter.writerow(dataEntry[i])
    
    def onMousePressed(self, event):
        #MousePressed serves many functions in my code
        #1. It is used in logIn screen to activate the dialog box in which
        #the Username and Password can be entered
        #It is used in the DoctorScreen to (1) view instructions and 
        #(2) add or delete patients, and (3) log out
        #Finally it is used in the PatientScreen to view the barGraphs and 
        #pieCharts as well access the aforementioned buttons
        (x,y) = (event.x ,  event.y)
        if self.mode == "loginMode":
            if 560 < x < 650 and 460 < y < 500:
                self.LoginPopUp.run()
        elif self.mode == "doctorMode" or self.mode == "helpScreenMode":
            if 300 < x< 420 and 515 < y < 545:
                self.addPPopup.run()
            elif 300 < x< 420 and 555 < y < 585:
                self.deletePPopup.run()
            elif 100 < x < 200 and 535 < y < 565:
                self.quit()
            elif 500 < x < 600 and 535 < y < 565:
                self.ChangeToPatientMode()
            elif 120 < x < 220 and 25 < y < 75:
                self.switchHelpScreen()
                
        else:
            if 180 < x< 280 and 120 < y < 180 and self.mode == "patientMode":
                self.makePieChart(self.patient.healthy,self.patient.unhealthy,
                    150,150)
            elif 20 < x < 240 and 300 < y < 550 and self.mode == "patientMode":
                self.canvas.create_rectangle(20,300,230,550, fill = "white")
                self.drawAxes(0)
                self.drawBarGraph(0,20, 60, self.patient.firmicuteConcentration,
                 width= 200, height= 250)
            elif 240 < x < 460 and 300 < y < 550 and self.mode == "patientMode":
                self.canvas.create_rectangle(240,300,450,550, fill = "white")
                self.drawAxes(1)
                self.drawBarGraph(1,10,40,
                    self.patient.bacterioditesConcentration,
                    width= 200, height= 250)
            elif 460 < x < 680 and 300 < y < 550 and self.mode == "patientMode":
                self.canvas.create_rectangle(460,300,680,550, fill = "white")
                self.drawAxes(2)
                self.drawBarGraph(2,30,80,
                    self.patient.lactoBascillusConcentration,
                    width= 200, height= 250)               
            elif 100 < x < 200 and 565 < y < 595:
                self.ChangetoDoctorMode()
            elif 500 < x < 600 and 565 < y < 595:
                self.quit()
        self.redrawAll()
 
    def drawGeneralInformation(self):
        #This function takes in values from variabes stored in the Patient 
        #class and loads as well as displays in the UI 
        #This method also draws the piechart
        self.canvas.create_rectangle(0,0,700,600, fill = "lavender blush",
         outline = "white")
        self.canvas.create_text(50,25,text = "%s" % (self.patient), 
            fill = "black",font = "BellMT 25")
        self.canvas.create_rectangle(5,50,300,250, fill = "light pink")
        self.canvas.create_text(10,50,text = "General Information:", 
            anchor= NW, fill = "black", font = "BellMT 20 bold")
        self.canvas.create_text(10,80, text = "Name: %s" % (self.patient),
         anchor = NW, fill = "black", font = "BellMT 14")
        self.canvas.create_text(10,100,text = "Age: %d " % 
            (self.patient.age),
         anchor= NW, fill = "black", font = "BellMT 14")
        self.canvas.create_text(10,120,text = "Height: %d ft" % 
            (self.patient.height), 
            anchor= NW, fill = "black", font = "BellMT 14")
        self.canvas.create_text(10,140,text = "Weight: %d lbs" % 
            (self.patient.weight),
            anchor= NW, fill = "black", font = "BellMT 14")
        self.canvas.create_text(10,160, text = "BodyMassIndex: %d" % 
            (self.patient.BMI),
            anchor= NW, fill = "black", font = "BellMT 14")
        self.canvas.create_text(10,180, text = "FirmicuteConcentration: %d %%" % 
            (self.patient.firmicuteConcentration),
            anchor= NW, fill = "black", font = "BellMT 14")
        self.canvas.create_text(10,200,text = "BacterioditesConcentration:%d %%" 
            % (self.patient.bacterioditesConcentration), 
            anchor= NW, fill = "black", font = "BellMT 14")
        self.canvas.create_text(10,220,text = "LactoBascillusConcentration:%d %%" 
            % (self.patient.lactoBascillusConcentration), 
            anchor= NW, fill = "black", font = "BellMT 14")
        self.canvas.create_rectangle(180, 120, 280, 170, fill = "cornsilk")
        self.canvas.create_text(230,130,text = " %Healthy", 
            font = "BellMT 14",  fill = "blue")
        self.canvas.create_text(230,150,text = " %Unhealthy", 
            font = "BellMT 14", fill = "red")

    def firmicuteText(self):
        return '''
Percent Firmicute Concentration
- ConcentrationWeight : 1/6
On Graph:
 -BlueBar = HealthyMean
 -GreenBar = PatientData
 -RedBar = UnhealthyMean
'''
    def bacterioditesText(self):
        return '''
Percent Bacteriodites Concentration
- ConcentrationWeight : 1/3
On Graph:
 -BlueBar = HealthyMean
 -GreenBar = PatientData
 -RedBar = UnhealthyMean
'''
    def lactoBascillusText(self):
        return '''
Percent LactoBascillus Concentration
- ConcentrationWeight : 1/2
On Graph:
 -BlueBar = HealthyMean
 -GreenBar = PatientData
 -RedBar = UnhealthyMean
'''
    def drawSpecificInformation(self):
        #This method draew the various bargraphs that take variables 
        #for each patient associated with the particular bacterial concentration
        #and graph them against healthy and unhealthy means
        self.canvas.create_rectangle(5,260,695,560, fill = "pale violet red")
        self.canvas.create_text(20,270,
         text = "Condition Specific Infomation", anchor = NW, fill = "black", 
         font = "BellMT 20 bold")
        self.canvas.create_rectangle(20,300,230,550, fill = "misty rose")
        self.canvas.create_text(130,400, text = self.firmicuteText(), 
            font = "BellMT")        
        self.canvas.create_rectangle(240,300,450,550, fill = "misty rose")
        self.canvas.create_text(350, 400, text = self.bacterioditesText(),
            font = "BellMT")
        self.canvas.create_rectangle(460,300,680,550, fill = "misty rose")
        self.canvas.create_text(570,400, text = self.lactoBascillusText(),
            font = "BellMT")

    def drawLogOut(self):
        #draws the logout button on the botto of the Doctor's/ Patient's Screen
        self.canvas.create_rectangle(100,565,200, 595, fill = "lemon chiffon")
        self.canvas.create_text(150,580, text = "Back", font = "BellMT 20" )
        self.canvas.create_rectangle(500,565,600, 595, fill = "lemon chiffon")
        self.canvas.create_text(550,580, text = "LogOut", font = "BellMT 20" )
    
    def convertDegreesToRadians(self,n):
        #converts radians to degrees to make pie chart
        radianvalue= (float(n)*math.pi/180)
        return radianvalue

    def makePieChart(self,healthy, unhealthy, width = 50, height = 50):
        #draws pie chart based off healthy, unhealthy, and patient values
        #The code for drawing piechart was taken from pastHW, however, it was
        #modified to match the infomation passed in as well as be incoporated 
        #into the canvas as oppose to its own screen
        healthyVal = float(healthy)
        unhealthyVal = float(unhealthy)
        cx = float(width)/0.7
        cy = float(height)/1
        r = min(width, height)/2
        extentPoint1 = ((float(healthyVal))/100)*360
        pointOne = extentPoint1 + 90
        angleOne = self.convertDegreesToRadians(90 + (extentPoint1)/2)
        extentPoint2 = (float(unhealthyVal)/100)*360
        pointTwo = pointOne + extentPoint2
        angleTwo = self.convertDegreesToRadians(pointTwo+ (extentPoint2)/2)
        if healthyVal == 100:
            self.canvas.create_rectangle(cx-(r+5), cy-(r+5), cx+(r+5), cy+(r+5), 
                fill = "white")
            self.canvas.create_oval(cx-r,cy-r,cx+r, cy+r, fill = "blue")
            self.canvas.create_text(cx,cy, text = "100%", fill = "white", 
                font = "Arial 12 bold")
        elif unhealthyVal == 100:
            self.canvas.create_rectangle(cx-(r+5), cy-(r+5), cx+(r+5), cy+(r+5), 
                fill = "white")
            self.canvas.create_oval(cx-r,cy-r,cx+r, cy+r, fill = "red")
            self.canvas.create_text(cx,cy, text = "100%", fill = "white", 
                font = "Arial 12 bold")
        else:
            self.canvas.create_rectangle(cx-(r+5), cy-(r+5), cx+(r+5), cy+(r+5), 
                fill = "white")
            self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, fill = "blue", 
                start = 90, extent= extentPoint1)
            self.canvas.create_text(cx + (r/2)* math.cos(angleOne), 
                cy- (r/2)*math.sin(angleOne), text = ("%d%%")%(healthyVal), 
                fill="white", font="Arial 12 bold")
            self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, fill = "red",
             start = pointOne, extent= extentPoint2)
            self.canvas.create_text(cx - (r/2)* math.cos(angleTwo), 
                cy- (r/2)*math.sin(angleTwo), text = ("%d%%")%(unhealthyVal), 
                fill="white", font="Arial 12 bold")
        self.root.mainloop()

    def chooseBarGraphFillColor(self,x):
        #Allows the healthy, unhealthy, and patient data to be differentiated
        #in the bargraphs displayed
        if x ==0:
            return "blue"
        elif x ==1:
            return "green"
        elif x ==2:
            return "red"

    def drawAxes(self,x):
        #draws axes for the bargraphs to allow for a frame of reference 
        if x ==0:
            self.canvas.create_line(30,515,220,515, fill = "black")
            self.canvas.create_line(30,515,30,350, fill = "black")
            self.canvas.create_text(125,530, text = "Percent Firmicutes")
        elif x ==1:
            self.canvas.create_line(250,515,440,515, fill = "black")
            self.canvas.create_line(250,515,250,350, fill = "black")
            self.canvas.create_text(350,530, text = "Percent Bacteriodites")
        elif x==2:
            self.canvas.create_line(470,515,675,515, fill = "black")
            self.canvas.create_line(470,515,470,350, fill = "black")
            self.canvas.create_text(575,530, text = "Percent LactoBascillus")
                
    def drawBarGraph(self, shiftFactor, healthy, unhealthy, patientData, 
        width= 200, height= 250):
        #The function for devloping the bargraph was developed by me,
        #It essentialy takes in healthy, and unhealthy ranges passed in for 
        #each separate bacterial concentration and plots it again patient 
        #data for that particula bacterial concentration
        shiftFactor = shiftFactor
        healthy = float(healthy)
        unhealthy = float(unhealthy)
        patientData = patientData
        data = [healthy, patientData, unhealthy]
        margin = 10 
        barWidth = (3*width/4)/4
        yScreenRatio = 2
        xScreenRatio = 25
        for x,y in enumerate(data):
            barFill = self.chooseBarGraphFillColor(x)
            left = x *(xScreenRatio) + x*(barWidth) + 2*margin 
            top = height - (y* yScreenRatio + margin)
            right = left + barWidth
            bottom = top + (y * yScreenRatio)
            self.canvas.create_rectangle(left+20+(230*shiftFactor), top+275, 
                right+20+(230*shiftFactor), bottom+275, fill = barFill)
            newLeft = left+20+(230*shiftFactor)
            newRight = right+20+(230*shiftFactor)
            self.canvas.create_text((newLeft+newRight)/2,top+260,text = data[x])
        self.root.mainloop()
            
    
    def drawDoctorsNote(self):
        #This function makes the doctors notes visible on the Patient's Screen
        self.canvas.create_rectangle(350,50,680,250, fill = "old lace")
        self.canvas.create_text(350,50, text = "Doctor's Notes", 
            anchor = NW, fill = "black")
    
    def loadNote(self,letter):
        #This function takes in letters to load the patient notes displayed 
        #in the patient notes section of the UI
        self.patient.doctorsNotesString = self.patient.doctorsNotesString+letter     

    def readFile(self,filename, mode="rt"):
        # Taken from notes in lecture
        with open(filename, mode) as fin:
            return fin.read()

    def writeFile(self,filename, contents, mode="wt"):
        # Taken from notes in lecture
        with open(filename, mode) as fout:
            fout.write(contents)

    def onKeyPressed(self, event):
        #This function takes Kepressed values and (1) adds them to the 
        #self.patient.doctorsNotesString if they are writng value
        #It also accounts for backspace to delete letters/ words
        #Further this function prevents words from going passed the 
        #Doctor's Notes text box 
        if event.keysym == "BackSpace":
            self.patient.doctorsNotesString=self.patient.doctorsNotesString[:-1]
        self.keyPressed = event.char
        letter = self.keyPressed
        if letter.isalpha() or letter.isdigit() or letter in ".?<>*&%$@ ":
                if len(self.patient.doctorsNotesString) % 40 != 0:
                    self.loadNote(letter)
                    self.updateNote()
                else:
                    self.loadNote("\n"+letter)
                    self.updateNote()
        
    def drawNote(self):
        #Functi0n takes in the self.patient.doctorsNotesString and draws it
        doctorsNote = self.patient.doctorsNotesString
        self.height = 75
        self.canvas.create_text(515,self.height, text = doctorsNote, 
            fill = "black", anchor = N)
 
    def drawPatientOptionMenu(self):
        #This function draws a scroll bar for all the patients in the data set
        #It allows the user to view all patient no matter how many, as oppose
        #to my previous version which used buttons to access the patient 
        #specific screen (buttons did not allow for viewing large patient #s)
        #I read this source to learn about scroll and select bars
        #http://stackoverflow.com/questions/2541718/why-am-i-getting-
        #a-instance-has-no-attribute-getitem-error
        master = self.root
        variable = StringVar(master)
        OPTIONS = self.patients
        variable.set(OPTIONS[0])
        w = apply(OptionMenu, (master, variable) + tuple(OPTIONS))
        w.pack()
        button = Button(master, text = "GO",
         command = lambda: self.getPatientAndDisplay(variable.get()))
        button.pack()
        self.displayOn = True
        

    def getPatientAndDisplay(self,name):
        patient = None
        patientIndex = -1
        for i in xrange(len(self.patients)):
            if (self.patients[i].getName() == name):
                patientIndex = i
                break
        if (patientIndex == -1):
            print ("ERROR : balh")
        else:
            patient = self.patients[patientIndex]
        self.onButtonPressed(patient)
        return
            
    def loginRedrawAll(self):
        #this function draws the log in screen
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0,0,700,600, fill= "midnight blue")
        self.canvas.create_line(0,400,105,400, fill = "white smoke", width = 10)
        self.canvas.create_line(100,400, 120, 200, 
            fill = "white smoke",width = 10)
        self.canvas.create_line(120, 200, 140, 580, 
            fill= "white smoke", width = 10)
        self.canvas.create_line(140, 580, 160, 450, 
            fill = "white smoke", width = 10)
        self.canvas.create_line(155, 450, 700, 450, 
            fill = "white smoke", width = 10)
        self.canvas.create_text(410,430, text = 'Welcome To EasyMed', 
            font = 'SnellRoundhand 40', fill = "dark turquoise")
        self.canvas.create_rectangle(560,460,650,500, fill = "white smoke")
        self.canvas.create_text(600,480, text = 'LogIn', 
            font = 'SnellRoundhand 20', fill = "navy")
        
    def IBSDefinition(self):
        return '''
Irritable Bowel Syndrome (IBS) is a common disorder that affects the 
large intestine (colon). Irritable bowel syndrome commonly causes 
cramping, abdominal pain, bloating, gas, diarrhea and constipation.
IBS is a chronic condition that needs long-term management. Only a 
small number of people with irritable bowel syndrome have severe signs 
and symptoms, however those that do may experience aggravate hemorrhoids.
Some people can control their symptoms by managing diet, lifestyle
and stress. Others will need medication and counseling.
'''
    def IBSSymptoms(self):
        return '''
-Abdominal pain or cramping 
-A bloated feeling
-Diarrhea and constipation
-Mucus in stool 
-Weight loss
'''
    def IBSAdditionalTests(self):
        return '''
-Colonoscopy  
-X-ray
-Computerized tomography
-Lower GI series
-Stool tests
'''

    def doctorRedrawAll(self):
        #Accounts for diplay of doctors mode 
        self.canvas.delete(ALL)
        self.canvas.create_rectangle(0,0,700,600, fill= "plum")
        self.canvas.create_rectangle(100, 100, 600, 500, fill = "lavender" )
        self.canvas.create_text (175, 120, text = "DiseaseDefinition",
         font = "BellMT 20 bold")
        self.canvas.create_text(350, 200, text = self.IBSDefinition(), 
            font = "BellMT 14", fill = 'black')
        self.canvas.create_text (152, 280, text = "Symptoms", 
            font = "BellMT 20 bold")
        self.canvas.create_text(220, 330, text = self.IBSSymptoms(), 
            font = "BellMT 14", fill = 'black')
        self.canvas.create_text (170, 390, text = "AdditionalTests", 
            font = "BellMT 20 bold")
        self.canvas.create_text(215, 440, text = self.IBSAdditionalTests(), 
            font = "BellMT 14", fill = 'black')
        self.canvas.create_rectangle(300,515,420, 545, fill = "lemon chiffon")
        self.canvas.create_text(360,530,text = "Add Patient",font = "BellMT 20")
        self.canvas.create_rectangle(300,555,420, 585, fill = "lemon chiffon")
        self.canvas.create_text(360,570, text = "Delete", font = "BellMT 20" )
        self.canvas.create_rectangle(100,535,200, 565, fill = "lemon chiffon")
        self.canvas.create_text(150,550, text = "LogOut", font = "BellMT 20" )
        self.canvas.create_rectangle(500,535,600, 565, fill = "lemon chiffon")
        self.canvas.create_text(550,550, text = "Next", font = "BellMT 20" )
        self.canvas.create_rectangle(120,25,230,75,fill = "lemon chiffon")
        self.canvas.create_text(175,50,text = "Instructions",font = "BellMT 20")
        self.drawDate()
        if self.displayOn == False:
            self.drawPatientOptionMenu()
        return
    
    def patientRedrawAll(self):
        #accounts for display of patient mode
        self.canvas.delete(ALL)
        self.drawGeneralInformation()
        self.drawSpecificInformation()
        self.drawDoctorsNote()
        self.drawNote()
        self.drawLogOut()

    def redrawAll(self):
        #Draw either the log in mode, patient mode or the doctor mode based off 
        #the switch, which is propgated by presseing the button for each patient
        if (not self._isRunning):
            if self.destroy == False: 
                self.root.destroy()
                self.destroy = True 
                return
        if self.mode == "loginMode":
            self.loginRedrawAll()
            
        elif self.mode == "doctorMode":
            if self.loginSuccessful == True:
                self.doctorRedrawAll()
        elif self.mode == "helpScreenMode":
            self.drawHelpScreen()
        else:
            self.patientRedrawAll()

    def isQuitting(self):
        #Accounts for leaving a particular screen
        self.hasQuit = True
        
    def initAnimation(self):
        #starts each animation
        self.hasQuit = False
        self.destroy = False  
        self.loginSuccessful = True 
        self.addPPopup = AddPatientPopUp(self)
        self.deletePPopup = DeletePatientPopUp(self)
        self.LoginPopUp = LoginPopUp(self)
        self.frame2 = Frame(self.root)
        self.frame2.pack()
        self.displayOn = False
        self.mode = "loginMode"
        
myAnimation = EMRAnimation()
myAnimation.run()
