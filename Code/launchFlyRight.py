####################################################################
"""
Assignment 3 - Object Oriented Programming
Version 2.5
Kaia Chapman & Karna Johnson

This file:
- Creates the GUI application by first launching the QT Designer generated
static GUI code.
- Binds event listeners on tabs and button nav elements to navigate between pages.
- Creates a StackedWidget in the Passenger Info tab that creates a new page to be filled
out for each of a Number of Passangers that the user entered earler.
- Sets next tabs to inanctive and doesn't allow forwardg navigation until a current tab
or page is completed.
- Populates data in tables on tabs 1 and 3 dynamicaly based on numbers of data
fields; currently populated with test data in nested lists.
- Creates data structures to hold all inputs a user entered throughout GUI. Currently prints
them on click of process payment buttn on last tab.


"""
####################################################################

import sys                                      #sys calls like exit
from PyQt4 import QtCore, QtGui                 #pyQT modules
from FlyRightAirlines2pt7 import Ui_MainWindow  #QT Designer generated code for main gui
from dialog import Ui_Dialog                    #QT Designer generated code for dialog box
import connectDB as cnx                         #connectDB class for to allow querying database
import db_flyright_create as newDB              #creates database if it doesn't exist
#import resource


#### set up compatibility with pyQT designer generated functions ####
"""The following definitions are used in the pyQT generated code. They are included
in this file so code is easier to customize when removing a statically generated
component used in the pyQT generated file and adding them as dynamically generated
objects in this file."""
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
#####################################################################

    
######################## begin Main class ###########################
class Main(QtGui.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        
        self.ui = Ui_MainWindow()   # self.ui = the main ui window object
        self.ui.setupUi(self)       #build it


        #lists will hold data inputed in each tab.
        self.passInfoInput=[]
        self.flightSelectionInput=[]
        self.flightCost=[]
        self.flightInfoInput=[]
        self.paymentInput=[]

        self.ui.tabWidget.setCurrentIndex(0)#start on first tab

        #bind currentChanged event that affects all tabs
        self.ui.tabWidget.currentChanged.connect(self.tabChanged)
        #if no db_flyright is yet installed, it will be created and populated
        try:
            db=cnx.connectDB()
        except:
            db=newDB.db_flyright_create()


        ########################## Tab 1 ###########################
        """set tab 2 to be not enabled, set the tab state (of being completed) to false,
connent all buttons clicked signals to appropriate slots - see tab 1 function def section"""
        self.ui.tabWidget.setTabEnabled(1, False)
        self.ui.lookupButton_2.clicked.connect(self.lookupID)
        self.ui.lookupButton.clicked.connect(self.lookupName)
        self.ui.nextCommandLink_3.clicked.connect(self.tab1NextClicked)
        self.ui.lookupTab.state=False;

        ########################## Tab 2 ###########################
        """set tab 3 to be not enabled, set tab 2 state (of being completed) to false,
connent all buttons clicked signals to appropriate slots, connect the change signal of each
input object type to slots that will see if tab is complete- see tab 2 function def section"""
        self.passCount=1            # set to 1 passanger unless changed so at least 1 passangeroption page generated
        self.returnTrip=True        #by defaly GUI will show input objects needed for return trip booking 
        self.ui.tabWidget.setTabEnabled(2, False)
        self.ui.flightInfoTab.state=False;
        #bind events that affect tab
        self.ui.nextCommandLink.clicked.connect(self.tab2NextClicked)
        #getChildInputsElts("string tab name") defined below. It returns several lists
        #of different types of elements that I'm iterating through an binding it's version
        #of a change event to the same slot, tabInfoUpdated()
        flightInfoLineEdits, flightInfoDateEdits, flightInfoTimeEdits,flightInfoRadios,flightInfoComboBoxes=self.getChildInputsElts("flightInfoTab")
        for i in flightInfoTimeEdits:
            i.timeChanged.connect(lambda: self.tabInfoUpdated(self.ui.flightInfoTab))#lambdas are required to add arg to function bound to pyQt signal
        for i in flightInfoDateEdits:
            i.dateChanged.connect(lambda: self.tabInfoUpdated(self.ui.flightInfoTab))
        for i in flightInfoComboBoxes:
            boxName=i.objectName()
            if boxName=="fromComboBox":
                i.activated.connect(self.fromComboBoxChanged)
            if boxName == "toComboBox":
                i.activated.connect(self.toComboBoxChanged)
            else:
                i.currentIndexChanged.connect(self.numPassChanged)
        self.ui.oneWayRadioButton.toggled.connect(self.oneWayToggled)

        ########################## Tab 3 ###########################
        """set tab 3 to be not enabled, set tab 3 state (of being completed) to false,
connent all buttons clicked signals to appropriate slots - see tab 3 function def section"""
        self.ui.flightSelectTab.state=False
        self.ui.tabWidget.setTabEnabled(3, False)
        self.ui.nextCommandLink_2.clicked.connect(self.tab3NextClicked)
        self.flightSelection=[]     #stores the full array of displayable flight info with id at end for depart flight
        self.flightSelection2=[]     #stores the full array of displayable flight info with id at end for return flight
        self.flightCost=[]
        self.flightSelectionInput=[]#stores the id(s) of selected flight(s)
        self.flightSelectionInput2=[]#stores the id(s) of selected flight(s)
        self.flightCost2=[]
        ########################## Tab 4 ###########################
        """set tab 5 to be not enabled, do not set state - states tracked in pages
in the stackedWidget in this tab - see tab 4 function def section"""
        self.ui.tabWidget.setTabEnabled(4, False)

        ########################## Tab 5 ###########################
        """set tab 5 state (of being completed) to false,
connent all buttons clicked signals to appropriate slots, connect the change signal of each
input object type to slots that will see if tab is complete- see tab 5 function def section"""
        self.ui.paymentTab.state=False
        paymentLineEdits, paymentDateEdits, paymentTimeEdits,paymentRadios,paymentComboBoxes=self.getChildInputsElts("paymentTab")
        for i in paymentDateEdits:
            i.dateChanged.connect(lambda: self.tabInfoUpdated(self.ui.paymentTab))
        for i in paymentLineEdits:
            i.textChanged.connect(lambda: self.tabInfoUpdated(self.ui.paymentTab))
        self.ui.purchaseButton.clicked.connect(self.processPurchase)
        self.ui.cancelButton.clicked.connect(self.cancelPurchase)

        
    ################################## END INIT ################################################
                
    ######################### START GENERAL EVENT SUPPORT FUNCTIONS ############################

    ################################
    def getChildInputsElts(self, tab):
        """Arg: a string of var name for tab in tabWidget,
OR the string "page" if called on a page in stackedWidget
Returns:
[0] dateEdits=list of all QDateEdit objects in tab given,
[1] timeEdits=list of all QDateEdit objects in tab given,
[2] radios=list of all QRadioButton objects in tab given,
[3] comboBoxes=list of all QComboBox objects in tab given
Each return list will be empty for possitions where the given tab has no children of a type
TODO: FIX to get checkboxes"""
        if tab == "page":
            obj=self.ui.stackedWidget.currentWidget()
        else:
            #get tab object
            obj = self.ui.tabWidget.findChild(QtGui.QWidget, tab)
        if obj!=0:#if success on finding tab object
            lineEdits = obj.findChildren(QtGui.QLineEdit)
            dateEdits = obj.findChildren(QtGui.QDateEdit)
            timeEdits = obj.findChildren(QtGui.QTimeEdit)
            comboBoxes= obj.findChildren(QtGui.QComboBox)
            radios    = obj.findChildren(QtGui.QRadioButton)
        #print("on tab ",tab,"in getChildInputElts lineEdits==", [i.text() for i in lineEdits])
        return lineEdits, dateEdits, timeEdits, radios, comboBoxes
    ################################END getChildInputsElts(tab)


    ################################
    def setInputs(self, tabStr, data=[]):
        """Arg: str of tab name to setInputs on,
optional arg: list of data to set inputs to
if no list is provided all fileds will be set to default/blank.
TODO: Complete setInputs to data"""
        lineEdits, dateEdits, timeEdits, radios, comboBoxes =self.getChildInputsElts(tabStr)
        #print("on tab ",tabStr,"in function start lineedits=", [i.text() for i in lineEdits])
        if data==[]:
            #print("on tab ",tabStr,"if date = [] comboboxes=", [i.currentText() for i in comboBoxes])
            #print("on tab ",tabStr,"after clear lineedits=", [i.text() for i in lineEdits])
            [i.setDate(QtCore.QDate.currentDate()) for i in dateEdits]
            [i.setTime(QtCore.QTime.currentTime()) for i in timeEdits]
            if tabStr=="flightInfoTab":
                blank=""
                self.ui.fromComboBox.insertItem(0,blank)
                self.ui.toComboBox.insertItem(0,blank)
            if tabStr=="passInfoTab":
                passGroupBoxes=self.ui.stackedWidget.currentWidget().findChildren(QtGui.QGroupBox)
                for box in passGroupBoxes:
                    print("box=",box.objectName())
                    checkBoxes =box.findChildren(QtGui.QCheckBox)
                    lineEdits +=box.findChildren(QtGui.QTextEdit)
                    comboBoxes+=box.findChildren(QtGui.QComboBox)
                    radios    +=box.findChildren(QtGui.QRadioButton)
                    [i.setChecked(False) for i in checkBoxes]
            [i.setCurrentIndex(0) for i in comboBoxes]
            [i.clear() for i in lineEdits]
            #print("on tab ",tabStr,"after setcurrent index comboboxes=",[i.currentText() for i in comboBoxes])
            [i.setChecked(False) for i in radios]
        else:#data passed in to populate #TODO - THIS SECTION WOULD RESET DATA TO PARAMETERS TO MODIFY A RESERVATION
            pass              
    ################################                  
            
        

    ################################           
    def getInputs(self, tab):
        """Arg: a string of var name for tab in tabWidget
OR the string "page" if called on a page in stackedWidget
Return:  ONSUCESS- a dictionary of all objects selected/checked/otherwise inputed like
{object1:object1Text, object2:object2Text,...} |ONFAIL- (int)0"""
        lineEdits, dateEdits, timeEdits, radios, comboBoxes=self.getChildInputsElts(tab)
        #merge date and time edit dicts to handle the same
        edits=dateEdits + timeEdits + lineEdits
        #create dict inputs containing {input object:string of user input}
        inputs={i:i.text() for i in edits}
        inputs.update({i:i.currentText() for i in comboBoxes})
        inputs.update({i:i.text() for i in radios if i.isChecked()})
        return inputs if len(inputs)>0 else 0
    ################################

    ################################
    def getBlankInputs(self, inputs):
        """Arg: a dictionary inputs (like {object1:object1Text, object2:object2Text,...})
Return: IF BLANK FIELDS-a list of the objects with blank input text |
ELSE NOT BLANK FIELDS- int(0) """
        blanks=[k for (k,v) in inputs.items() if v == ""]
        return blanks if len(blanks)>0 else 0
    ################################


    ################################
    def tabInfoUpdated(self, tabChanged):
        """SLOT called when any item in an info gathering tab changed -
ARG=the QWidgtet object in the tabWidget that was changedg
sets next tab to enabled and changes the state to true"""
        #print("in tabInfoUpdated,")
        inputs=self.getInputs(tabChanged.objectName())
        #print("inputs=",inputs)
        if inputs:
            if not self.getBlankInputs(inputs):
                if self.ui.tabWidget.indexOf(tabChanged)<5:#if not on last tab, allow next tab
                    self.ui.tabWidget.setTabEnabled(self.ui.tabWidget.indexOf(tabChanged)+1, True)
                tabChanged.state=True
                #print("tabChanged.objectName()=",tabChanged.objectName())
                if tabChanged.objectName()=="flightInfoTab" and self.returnTrip: #fix allow nav before dates chosen
                    self.enforceDateTimeDiff("silent")
        else:
            if not self.returnTrip:
                self.ui.flightInfoTab.state=True
                self.ui.tabWidget.setTabEnabled(2,True)
                
    ################################

            
    ################################
    def tabChanged(self):
        """Function calls processes to generate data in wigets and records data based on entries.  """
        #print("tabChanged with passCount = ", self.passCount)
        if self.ui.tabWidget.currentIndex()!= 1:
            self.genStackedWidget()
        if self.ui.tabWidget.currentIndex()==2:
            db=cnx.connectDB()
            #set up parameters: departAirport, departDate(str), departTime(str), arriveAirport, numPass, rate(str='coach'||'firstclass')
            departAirport=self.flightInfoInput['fromComboBox'].split('(')[1][:-1]
            departDate=self.flightInfoInput['departDateEdit']
            departTime=self.flightInfoInput['departTimeEdit']
            arriveAirport=self.flightInfoInput['toComboBox'].split('(')[1][:-1]
            try:
                rate=self.flightInfoInput['firstRadioButton']#if this can be accessed
                rate="firstclass"
            except:
                rate="coach"
            self.flightOptDepartData=db.flightSelectTableData(departAirport,departDate,departTime,arriveAirport,self.passCount,rate)
            self.createFlightOptTable(self.ui.departingTableWidget, self.flightOptDepartData)
            if self.returnTrip:
                departAirport2=self.flightInfoInput['toComboBox'].split('(')[1][:-1]
                departDate2=self.flightInfoInput['retDateEdit']
                departTime2=self.flightInfoInput['retTimeEdit']
                arriveAirport2=self.flightInfoInput['fromComboBox'].split('(')[1][:-1]
                self.flightOptReturnData=db.flightSelectTableData(departAirport2,departDate2,departTime2,arriveAirport2,self.passCount,rate)
                self.createFlightOptTable(self.ui.returnTableWidget, self.flightOptReturnData)                
        if self.ui.tabWidget.currentIndex()==3:
            testData=[]
            [testData.append(['Flight: '+i[0]+" to "+i[3],i[6]]) for i in [j for j in [k for k in self.flightSelection]]]
            [testData.append(['Flight: '+i[0]+" to "+i[3],i[6]]) for i in [j for j in [k for k in self.flightSelection2]]]
            self.generateTab5Table(testData)
    ################################
        

    ################################
    def dialogBlankFields(self, blanks):
        """Arg: a list of input objects user left blank while attempting nav to next section
This funtion creates a new dialog box to inform user of blanks that need filled."""
        parentTitles={}
        #use dictionarylike {"titleString":""} so dup title strings not added
        for i in blanks:
            parentTitles[i.parent().title()]=""
            #To do: fix code to set backround of blank input objects to different shade or get rid of.
            #It's not working on QComboBoxes and needs to revert when user types in field if kept.
            #self.ui.errorPalette = QtGui.QPalette()#this isn't working on comboBoxes...TODO
            #self.ui.errorPalette.setColor(i.backgroundRole(), QtGui.QColor('#ff9'))
            #i.setPalette(self.ui.errorPalette)
            #i.setAutoFillBackground( True );
        dialog=Dialog()
        dialog.addText("<div>Please fill in information on:</div>")
        #add the text from each of the unique parent element titles held in parentTitles.keys()
        [(dialog.addText("<p>- "+k+"</p>")) for k in parentTitles.keys()]
        dialog.completeText()
        dialog.exec_()
        
    ################################    

    def recordInputs(self, inputs, tab):
        """Args: a dict of {object:user input in object} from a tab,
a string of name of tab.
Function is starting to record input in appropriate data structures from each tab."""
        if tab == "passInfoTab":
            """passInfoInput will be a list of dictionaries that hold
{object name:input in object} for each passenger"""
            i=self.ui.stackedWidget.currentIndex()
            try:
                self.passInfoInput[i]={k.objectName():v for (k,v) in inputs.items()}
            except:
                self.passInfoInput.append({k.objectName():v for (k,v) in inputs.items()})
            passGroupBoxes=self.ui.stackedWidget.currentWidget().findChildren(QtGui.QGroupBox)
            for box in passGroupBoxes:
                print("box=",box.objectName())
                checkBoxes= box.findChildren(QtGui.QCheckBox)
                comboBoxes= box.findChildren(QtGui.QComboBox)
                radios    = box.findChildren(QtGui.QRadioButton)
                textEdits = box.findChildren(QtGui.QTextEdit)
                extra={j.objectName():j.text() for j in radios if j.isChecked()}
                print("extra=",extra)
                extra.update({j.objectName():j.currentText() for j in comboBoxes})
                print("extra2=",extra)
                extra.update({j.objectName():j.text() for j in checkBoxes if j.isChecked()})
                print("extra3=",extra)
                extra.update({j.objectName():j.toPlainText() for j in textEdits})
                print("extra4=",extra)
                print("self.passInfoInput[i]=",self.passInfoInput[i])
                self.passInfoInput[i].update(extra)
            # fixed - replace " " or "-" with "" in zip code as soon as stored
            self.passInfoInput[i]['passZipLineEdit'+str(i+1)]=self.passInfoInput[i]['passZipLineEdit'+str(i+1)].replace("-","").replace(" ","")
        elif tab == "flightInfoTab":
            """flightInfoInput will be a dict of {object name:input in object}"""
            self.flightInfoInput={k.objectName():v for (k,v) in inputs.items()}
    ########################## END GENERAL EVENT SUPPORT FUNCTIONS #############################     
        
    ############################## START TAB 1 - LOOKUP TAB ####################################
    ################################
    def tab1NextClicked(self):
        """SLOT tab1Next is the new reservation button -
enable next tab and set index to go there"""
        self.ui.tabWidget.setTabEnabled(1, True)
        self.ui.tabWidget.setCurrentIndex(1)
    ################################

    ################################
    def lookupID(self):
        """Calls db module processes to allow search for reservation by id.
Dialogs errors in getting input or not finding a reservation. Feeds data
from matched reservations to funct to generate the tableWidget below"""
        idInput=self.ui.resNumLineEdit.text()
        if idInput=="":
            dialog=Dialog()
            dialog.addText("Please fill in the Reservation ID to Lookup")
            dialog.completeText()
            dialog.exec_()
        else:
            db=cnx.connectDB()
            data=db.lookupId(idInput)
            #print("data=",data)
            try:
                isData=data[0]      #works if we got back data
                self.generateTab1Table(data)
            except:                   #else no customer found
                dialog=Dialog()
                dialog.addText("<div>Customer not found.</div>")
                dialog.completeText()
                dialog.exec_()   
    ################################

    ################################
    def lookupName(self):
        """Calls db module processes to allow search for reservation by id.
Dialogs errors in getting input or not finding a reservation. Feeds data
from matched reservations to funct to generate the tableWidget below"""
        nameInputs={"Last Name":self.ui.lineEdit, "First Name":self.ui.lineEdit_2, "Zip Code":self.ui.lineEdit_3}
        blanks={k:v for (k,v) in nameInputs.items() if v.text()==""}
        if len(blanks)>0:
            dialog=Dialog()
            dialog.addText("<table>\n\t<th><td>To Search by Name, Please Fill Out:</td></th>")
            [dialog.addText("\n\t<tr><td>"+k+"</td></tr>") for k in blanks.keys()]
            dialog.addText("\n</table>")
            dialog.completeText()
            dialog.exec_()
        else:
            db=cnx.connectDB()
            data=db.lookupName(nameInputs["First Name"].text(), nameInputs["Last Name"].text(), nameInputs["Zip Code"].text())
            #print("data=",data)
            try:
                isData=data[0]      #works if we got back data
                self.generateTab1Table(data)
            except:                   #else no customer found
                dialog=Dialog()
                dialog.addText("<div>Customer not found.</div>")
                dialog.completeText()
                dialog.exec_()   
    ################################

    
    ##############################################################
    def generateTab1Table(self, data):
        """Funtion will set rowCount to how many items in possible flight matches and set the
row count of the table to that number. It will call creaeTab1Table once and for as many times
as in rowCount it  will and call populateTab1Table with the iteration and the list of data
field at that index"""
        #rowCount == number of lists nested in testData list
        rowCount=len(data)
        #setting the row count for the tableWidget to the number of rows represented in testData
        self.ui.tableWidget.setRowCount(rowCount)
        #call createTable which creates static table properties once
        self.createTab1Table()
        #for each row in testData call populateTable with params:
        #(iteration number , the list/row at that iteration number in testData) 
        [self.populateTab1Table(i, [data[i][j] for j in range(len(data[i]))] ) for i in range(rowCount)]
    ##############################################################


    ##############################################################
    def createTab1Table(self):
        """Function creates all the elemts in table that need made once no matter
how many rows in table."""
        #setting the column count for the tableWidget
        self.ui.tableWidget.setColumnCount(5)
        #setting the flight number column size
        self.ui.tableWidget.setColumnWidth(0, 65)
        #setting the departing column size
        self.ui.tableWidget.setColumnWidth(1, 237)
        #setting the arriving column size
        self.ui.tableWidget.setColumnWidth(2, 237)
        #set Number Of Passengers column size
        self.ui.tableWidget.setColumnWidth(3,65)
        #setting the GO button column size
        self.ui.tableWidget.setColumnWidth(4, 48)
        #setting the header text for the Reservation #
        header1 = QtGui.QTableWidgetItem('RES #')
        #setting the header text for departing
        header2 = QtGui.QTableWidgetItem('Departing')
        #setting the header text for arriving
        header3 = QtGui.QTableWidgetItem('Arriving')
        #setting the header text for # flyers
        header4=QtGui.QTableWidgetItem('# Flyers')
        #setting the header text for the go button to nothing
        header5 = QtGui.QTableWidgetItem('')
        #setting the header name for the flight # column
        self.ui.tableWidget.setHorizontalHeaderItem(0, header1)
        #setting the header name for the departing flight column
        self.ui.tableWidget.setHorizontalHeaderItem(1, header2)
        #setting the header name for the arriving flight column
        self.ui.tableWidget.setHorizontalHeaderItem(2, header3)
        #set the header name for # Passengers
        self.ui.tableWidget.setHorizontalHeaderItem(3, header4)
        #setting the header name for the Go button column
        self.ui.tableWidget.setHorizontalHeaderItem(4, header5)
    ##############################################################

    ##############################################################
    def populateTab1Table(self, rowNum, rowDataList):
        """ARGS:
rowNum = current iteration of row number
rowDataList = a list of strings representing:
    flightNum, deptDate, deptTime, deptLoc, destDate, destTime, destLoc, passNum
Function creates and populates all objects in table that need creates once for each row"""
        #setting a QTableWidgetItem to a provided flight number
        flightNum = QtGui.QTableWidgetItem(rowDataList[0])
        #setting a QTableWidgetItem to a string of info on flight departing
        departStr = QtGui.QTableWidgetItem(rowDataList[1]+" "+ rowDataList[2] +" "+ rowDataList[3])
        #setting a QTableWidgetItem to a string of info on flight arriving
        arriveStr = QtGui.QTableWidgetItem(rowDataList[4]+" "+ rowDataList[5] +" "+ rowDataList[6])
        #set passenger number
        passNum=QtGui.QTableWidgetItem(rowDataList[7])
        #setting the flight number to first column
        self.ui.tableWidget.setItem(rowNum, 0, flightNum)
        #setting the item for the departing flight
        self.ui.tableWidget.setItem(rowNum, 1, departStr)
        #setting the item for the arriving flight
        self.ui.tableWidget.setItem(rowNum, 2, arriveStr)
        #setting the passenger number to 4th column
        self.ui.tableWidget.setItem(rowNum, 3, passNum)
        #creating a QPushButton within the tableWidget
        goBtn = QtGui.QPushButton(self.ui.tableWidget)
        #setting the button text to GO
        goBtn.setText('GO')
        goBtn.clicked.connect(lambda: self.goToRes(rowDataList[0]))
        #placing the button into the 5th column
        self.ui.tableWidget.setCellWidget(rowNum, 4, goBtn)
    ##############################################################

    ##############################################################
    def goToRes(self, resNum):
        """SLOT to listen for goButton that's populated when a reservation is found is clicked
Creates a dialog to ask user to cancel or confirm reservation. If cancel calls db.cancelRes with
the resNum needing cancelled, and creates new dialog with confirmation information.
If confirm calls db.confirmId with resNum and creates a new dialog with the returned reservation details."""
        dialog=Dialog()
        dialog.addText("Please select an option to cancel or confirm reservation.")
        dialog.completeText()
        dialog.pushButton.setText(_translate("Dialog", "Confirm", None))
        dialog.addCancelOpt()
        db=cnx.connectDB()
        isConfirm=dialog.exec_()
        dialog=Dialog()
        if isConfirm:
            flights, passengers=db.confirmId(resNum)
            rateClass="first class"
            if flights[0][0]=="C" or flights[0][0]==0:
                rateClass="coach"
            numFlyers=len(passengers)
            dialog.addText("<table><thead><th colspan='3' align='center'>Your reservation is for "
                           +str(numFlyers)+" "+rateClass+" seats" if numFlyers>1 else "<table><thead><th colspan='3' align='center'>Your reservation is for "
                           +str(numFlyers)+" "+rateClass+" seat")
            dialog.addText("</th></thead><thead><th colspan='3' align='center'>on flights" if len(flights)>1 else "</th></thead><thead><th colspan='3' align='center'>on flight")
            dialog.addText(":</th></thead><br />")
            for i in flights:
                dialog.addText("<br /><tr><th colspan='3'><u>Departing:</u></th></tr>")
                dialog.addText("<tr><td width='45%'>"+str(i[1])[:-3]+"</td><td colspan=2>"+i[3]+", "+i[4]+" ("+i[2]+")</td></tr>")
                dialog.addText("<tr><th colspan='3'><u>Arriving:</u></th></tr>")
                dialog.addText("<tr><td width='45%'>"+str(i[5])[:-3]+"</td><td colspan=2>"+i[7]+", "+i[8]+" ("+i[6]+")</td></tr>")
            dialog.addText("<br /><tr><th colsapn='3'><u>Passenger Information:</u></th></tr>")
            dialog.addText("<tr><td width='33%'><u>Name</u></td><td width='33%'><u>Meal?</u></td><td width='33%'><u># Bags</u></td></tr>")
            for i in passengers:
                meal="Yes" if i[2]==1 else "No"
                dialog.addText("<tr><td width='46%'>"+i[0]+" "+i[1]+"</td><td width='27%'>"+meal+
                               "</td><td width='27%'>"+str(i[3])+"</td></tr>")
                extra=""
                if i[4]:
                    extra+="<div>*Assist prepared for passenger.</div>"
                if i[5]:
                    extra+="<div>*Special request: "+i[5]+"</div>"
                if extra !="":
                    dialog.addText("<tr><td colspan=3>"+extra+"</td></tr>")
            dialog.addText("</table><br /><center><b>Thanks for flying right!</b></center>")
            dialog.completeText()
            dialog.exec_()
                    
        else:
            result=db.cancelRes(resNum)            
            dialog.addText("<div>Reservation number "+resNum+" has been cancelled.</div>")
            dialog.addText("<div>"+str(float(result[0]*(-1.0)))+" has been refunded to "+result[6]+"'s "+result[2]
                           +" ending in the last 4 digits :"+str(result[3])[-4:]+"</div>")
            dialog.completeText()
            dialog.exec_()
    ##############################################################
        
    ################################# END TAB 1 - LOOKUP TAB ###################################


    ############################# START TAB 2 - FLIGHT INFO TAB ################################
    ################################
    def tab2NextClicked(self):
        """SLOT called when tab2NextClicked...
This function checks that all info has been filled out on Flight Info tab before alloing
user to continue to next tab. It also calls genStackedWidget as the passanger count was chosen
on this tab, so program now knows how many pages on the passanger info tab StackedWidget to build"""
        if self.returnTrip:
            #print("if self.returnTrip:")
            self.enforceDateTimeDiff()
        if self.ui.flightInfoTab.state:
            #print("if self.ui.flightInfoTab.state")
            self.recordInputs(self.getInputs("flightInfoTab"), "flightInfoTab")
            self.ui.tabWidget.setCurrentIndex(2)
            #self.createFlightOptTable(self.ui.departingTableWidget) 
            #self.createFlightOptTable(self.ui.returnTableWidget)
        else:
            #print("else")
            blanks = self.getBlankInputs(self.getInputs("flightInfoTab"))
            if blanks:
                self.dialogBlankFields(blanks)
    ################################

    ################################
    def oneWayToggled(self):
        """SLOT: hides or shows the input elements needed to fill in data on  a return trip
when oneWayRadioButton is toggled"""
        if self.ui.oneWayRadioButton.isChecked():
            self.ui.retDateEdit.hide()
            self.ui.retDateLabel.hide()
            self.ui.retTimeEdit.hide()
            self.ui.returnTimeLabel.hide()
            self.returnTrip=False
            self.tabInfoUpdated(self.ui.passInfoTab)
            #print("Here, self.returnTrip=",self.returnTrip)
        else:
            self.ui.retDateEdit.show()
            self.ui.retDateLabel.show()
            self.ui.retTimeEdit.show()
            self.ui.returnTimeLabel.show()
            self.returnTrip=True
    ################################

    ################################
    def fromComboBoxChanged(self):
        """SLOT: if user selection in fromComboBox (on flightInfo tab) is changed from the default
blank selection, remove the blank from the list. Then call tabInfoUpdated to add permission
to nav to next page if no blank fields left, then call  enforceFromToDiff to revoke nav
permission if destination identical to departure airport."""
        if self.ui.fromComboBox.itemText(0)=="":
            self.ui.fromComboBox.removeItem(0)
        self.tabInfoUpdated(self.ui.flightInfoTab)
        self.enforceFromToDiff()
    ################################


    ################################
    def toComboBoxChanged(self):
        """SLOT: if user selection in toComboBox (on flightInfo tab) is changed from the default
blank selection, remove the blank from the list. Then call tabInfoUpdated to add permission
to nav to next page if no blank fields left, then call  enforceFromToDiff to revoke nav
permission if destination identical to departure airport."""
        if self.ui.toComboBox.itemText(0)=="":
            self.ui.toComboBox.removeItem(0)
        self.tabInfoUpdated(self.ui.flightInfoTab)
        self.enforceFromToDiff()
    ################################

    ################################
    def numPassChanged(self):
        """SLOT: if the number of passengers is changed tabInfoUpdated should be called on the tab
and any tabs previously enabled after one after this tab should be disables as info would need
changed in them"""
        self.tabInfoUpdated(self.ui.flightInfoTab)
        self.ui.flightSelectTab.state=False
        self.ui.tabWidget.setTabEnabled(3, False)
        self.ui.passInfoTab.state=False
        self.ui.tabWidget.setTabEnabled(4, False)
        self.ui.paymentTab.state=False
    ################################
    def enforceFromToDiff(self):
        """Revoke allowing user to navigate to next tab if airports in toComboBox and
fromComboBox are identical"""
        if self.ui.toComboBox.currentText()==self.ui.fromComboBox.currentText():
            self.ui.tabWidget.setTabEnabled(2, False)
            self.ui.flightInfoTab.state=False
            dialog=Dialog()
            dialog.addText("Destination Airport cannot match Departure Airport")
            dialog.completeText()
            dialog.exec_()
    ################################

    ################################
    def enforceDateTimeDiff(self, silent=False):
        """Function will need to make sure return date/time combo after depart date/time.
It currently just makes sure they are not identical and creates a dialog and prevents fw nav
if they are."""
        if self.returnTrip:
            if str(self.ui.departDateEdit.text()) == str(self.ui.retDateEdit.text()):
                if str(self.ui.departTimeEdit.text()) == str(self.ui.retTimeEdit.text()):
                    if not silent:
                        dialog=Dialog()
                        dialog.addText("Return Date and Time must be after Departue Date and Time")
                        dialog.completeText()
                        dialog.exec_()
                    self.ui.tabWidget.setTabEnabled(2, False)
                    self.ui.flightInfoTab.state=False
        #TODO: functions to convert date & time strings to floats that support comparison
    ################################
            
    ############################# END TAB 2 - FLIGHT INFO TAB ################################

            
    ########################## START TAB 3 - FLIGHT SELECTION TAB ############################
    ################################
    def tab3NextClicked(self):
        """SLOT listens for next button click, sends to next tab if state is True, else dialogs error"""
        if self.ui.flightSelectTab.state:
            self.ui.tabWidget.setCurrentIndex(3)
        else:
            dialog=Dialog()
            dialog.addText("<div>Please select a flight.</div>")
            dialog.completeText()
            dialog.exec_()
    ################################


    ################################
    def createFlightOptTable(self, widget, tableData):
        """This function sets up pices of a given table that only need called once.
For each option in provided tableData it calls createDepartOption  with what iteration it's
on and the option at that index."""       
        choices = QtGui.QTableWidgetItem('Flight Choices')
        widget.setHorizontalHeaderItem(0, choices)
        choices.setTextAlignment(0)
        numOptions=len(tableData)
        widget.setRowCount(numOptions)
        widget.setColumnCount(1)
        widget.setColumnWidth(0,800)
        widget.numRowsTotal=0
        for i in range(numOptions):
            #print("goto createDepartOption with i=",i, "tableDate[i]=", tableData[i])
            self.createDepartOption(i, tableData[i], widget)
    ################################
            
    ################################
    def createDepartOption(self, i, currentOptData, widget):
        """Arguments: the current iteration, 2d list with current option data
Creates and populated all items in the table that need generated once per option.
For each row in current option calls populateDepartTableRow with the iteration and
the row at that index"""
        #items created once per option set
        departOption="departOption1"+str(i)
        self.ui.departOption = QtGui.QTableWidget(3,4)
        self.ui.departOption.setObjectName("departOption"+str(i))
        #setting the column count for the tableWidget
        self.ui.departOption.setColumnCount(4)
        #setting the departing column size
        self.ui.departOption.setColumnWidth(0, 250)
        #setting the arriving column size
        self.ui.departOption.setColumnWidth(1, 250)
        #set Number Of Passengers column size
        self.ui.departOption.setColumnWidth(2,65)
        header1 = QtGui.QTableWidgetItem('Depart')
        #setting the header text for arriving
        header2 = QtGui.QTableWidgetItem('Arrive')
        #setting the header text for # flyers
        header3=QtGui.QTableWidgetItem('Price')
        header4=QtGui.QTableWidgetItem('Total')
        #setting the header name for the flight # column
        self.ui.departOption.setHorizontalHeaderItem(0, header1)
        #setting the header name for the departing flight column
        self.ui.departOption.setHorizontalHeaderItem(1, header2)
        #setting the header name for the arriving flight column
        self.ui.departOption.setHorizontalHeaderItem(2, header3)
        self.ui.departOption.setHorizontalHeaderItem(3, header4)
        widget.setCellWidget(i,0,self.ui.departOption)
        self.ui.departOption.setRowCount(len(currentOptData))
        rowsInCurrentOpt=len(currentOptData)
        #for each row in current option, call populateDepartTableRow with the index of
        #the iteration and the row at that index. Track total price and give it as last
        #optional param to populateDepartTableRow on last iteration for each option.
        totalPrice=0
        for j in range(rowsInCurrentOpt):
            totalPrice+=float(currentOptData[j][6])
            print("goto populateDepartTableRow with i=",i,";j=",j, ";currentOptData[j]=", currentOptData[j],";rowsInCurrentOpt",rowsInCurrentOpt)
            print("totalPrice=",totalPrice,";j+1=",str(j+1), ";rowsInCurrentOpt",rowsInCurrentOpt)
            self.populateDepartTableRow(rowsInCurrentOpt, i,j, currentOptData[j], widget, totalPrice)if rowsInCurrentOpt==j+1 else self.populateDepartTableRow(rowsInCurrentOpt, i, j, currentOptData[j], widget)
    ################################
            
    ################################
    def populateDepartTableRow(self, rowsInCurrentOpt, i,j, listData, widget, total=None):
        """Args: the index of a row within an option, the list of data in that row:
[departCity, departTime, departDate, arriveCity, arriveTime, arriveDate,price]
optional arg: a float total price that will be provided on last iteration
Function creates and populates all items in table that need done on each row of each option,
and on the last iteration, the final column that spans all rows in the option"""
        widget.numRowsTotal+=1
        depart1 = QtGui.QTableWidgetItem(listData[0]+" "+listData[1]+" "+listData[2])
        arrive1 = QtGui.QTableWidgetItem(listData[3]+" "+listData[4]+" "+listData[5])
        price1 = QtGui.QTableWidgetItem("$"+listData[6])
        #print("entering populateDepartTableRow, setting departOption to j=", j)
        #setting the item for the departing flight
        self.ui.departOption.setItem(j, 0, depart1)
        #setting the item for the arriving flight
        self.ui.departOption.setItem(j, 1, arrive1)
        self.ui.departOption.setItem(j, 2, price1)
        #on last iteration arg total will be not None, then set last column that spans rows
        #in option to a radio button and a label with info on total price
        if total:
            self.ui.departOption.setSpan(j,3,rowsInCurrentOpt,1)
            #row height for ith row = 24px for header + 30px for each row in current option
            widget.setRowHeight(i,24+(30*rowsInCurrentOpt))
            #print("Total=",total, ";I should make a radio now with set to row=",j)
            holder=QtGui.QWidget()
            self.ui.label = QtGui.QLabel(holder)
            self.ui.label.setObjectName("label"+str(i))
            self.ui.radioButton = QtGui.QRadioButton(holder)
            self.ui.radioButton.setGeometry(QtCore.QRect(30, 12, 16, 16))
            self.ui.radioButton.setText("")
            self.ui.radioButton.setObjectName(_fromUtf8("radioButton"+str(i)))
            #print("connecting flightSelectRadioClicked to i=", i)
            self.ui.radioButton.clicked.connect(lambda: self.flightSelectRadioClicked(i, widget))
            self.ui.label.setText("$"+str(total))
            self.ui.departOption.setCellWidget(j, 3, holder)
    ################################

    ################################
    def flightSelectRadioClicked(self, i, widget):
        print("flightSelectRadioClicked with i=",i)
        """SLOT: for flightSelectRadioClicked
Args: 1=order of radios, widget=the depart/return table widgets
Processes which choice was made and sets corresponding lists to the data
from that radio. Unselects other radios. Sets state Tre and enables nav
to next tab"""
        radios=widget.findChildren(QtGui.QRadioButton)
        for j in range(len(radios)):
            if j!=i:
                print("j!=i with i=",i, ";j=",j)
                radios[j].setChecked(False);
            else:
                print("j==i with i=",i, ";j=",j)
                #db=cnx.connectDB()
                print("widget.objectName()=",widget.objectName())
                if widget.objectName()=="departingTableWidget":
                    self.flightSelection=self.flightOptDepartData[i]
                    self.flightSelectionInput=[j[-1] for j in self.flightSelection] #put last item of each flight, id, in flightSelectionInput
                    self.flightCost=[j[-2] for j in self.flightSelection]           #and the one before, price, in flightCost
                    print("flightSelection=",self.flightSelection)
                else:
                    self.flightSelection2=self.flightOptReturnData[i]
                    self.flightSelectionInput2=[j[-1] for j in self.flightSelection2]#put last item of each flight, id, in flightSelectionInput
                    self.flightCost2=[j[-2] for j in self.flightSelection2]
                    print("flightSelection2=",self.flightSelection2)
                if self.returnTrip:
                    print("There is a return trip.")
                    if len(self.flightCost2)>0:
                        self.ui.flightSelectTab.state=True;
                        self.ui.tabWidget.setTabEnabled(3, True)
                    else:
                        print("Fill out return toenable next tab.")
                else:
                    print("There is NOT a return trip.")
                    self.ui.flightSelectTab.state=True;
                    self.ui.tabWidget.setTabEnabled(3, True)               
    ################################
        
    ########################### END TAB 3 - FLIGHT SELECTION TAB #############################
        
        
    ########################### START TAB 4 - PASSENGER INFO TAB #############################
    ###########################
    def fwdStackNavClicked(self):
        """SLOT for fwdStackNavButton.clicked
fwdStackNavButton is the fwd nav in the StackedWidget in the Passenger Info tab"""
        #set stackedWidget.currentIndex 1 higher
        done=self.tab4CheckComplete()
        if done:
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex()+1)
            if len(self.passInfoInput)>0:
                #if there's already been at least one passenger entered, set the adress fields
                #from the first passenger inputed to the placeholder text on rest of entries
                firstPass=self.passInfoInput[0]
                #[print("HERE="+k,v) for (k,v) in firstPass.items()]
                pass1Address=firstPass["passAddressLineEdit1"]
                pass1City=firstPass["passCityLineEdit1"]
                pass1Zip=firstPass["passZipLineEdit1"]
                pass1State=firstPass["passStateComboBox1"]
                self.ui.passAddressLineEdit.setText(pass1Address)
                self.ui.passCityLineEdit.setText(pass1City)
                self.ui.passZipLineEdit.setText(pass1Zip)    
                self.ui.passStateComboBox.setCurrentIndex(self.ui.passStateComboBox.findText(pass1State))
    ################################

    ################################
    def backStackNavButton(self):
        """SLOT: for backStackNavButton.clicked  -set stackedWidget.currentIndex 1 lower"""
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex()-1)
    ###########################
                                                          
    ################################
    def tab4NextClicked(self):
        """SLOT: cals function to check if tab info complete, if so allows fw nav"""
        done=self.tab4CheckComplete()
        if done:
            self.ui.tabWidget.setTabEnabled(4, True)
            self.ui.tabWidget.setCurrentIndex(4)
    ################################
    
    ################################
    def tab4CheckComplete(self):
        """Function checks if blank inputs. If blanks, calls to dialog them and returns false.
If no blanks, calls to record inputs and returns true."""
        if self.ui.flightSelectTab.state:
            inputs=self.getInputs("page")
            blanks = self.getBlankInputs(inputs)
            if blanks == 0:
                self.recordInputs(inputs, "passInfoTab")
                i=self.ui.stackedWidget.currentIndex()
                #print("self.passInfoInput=",self.passInfoInput)
                if self.passInfoInput[i]['passZipLineEdit'+str(i+1)].isdigit():
                    return True
                else:
                    dialog=Dialog()
                    dialog.addText("<div>Please enter a numeric zip code.</div>")
                    dialog.completeText()
                    dialog.exec_()
                    return False
            else:
                self.dialogBlankFields(blanks)
                return False
        else:
            return False
    ################################


    ################################
        """Funtion generates the stacked widget on the Passanger Info tab the number of times
user entered and sets passCount to that number also"""
    def genStackedWidget(self):
        try:
            self.passCount=int(self.ui.passComboBox.currentText())
        except: #leave set to 1 to generate 1 options page for 1 passanger if not set to an int
            pass
        #generate a new passOptions page for each passenger in passCount
        for i in range(self.passCount):
            self.genPassOptions(i+1)
    ################################


    ################################
        """Argument: i, iterator in range 1=>(number of passanger pages that need built+1).
 This function creates one iteration of the Passanger Info to go in main StackedWidget on
 Passanger Info tab. All object names that later may need accessed are assigned as their
 existing value +str(i) (to make var names like "mealCheckBox1", "mealCheckBox2")"""
    def genPassOptions(self, i):
        #print(self.ui.stackedWidget)
        """This section looks at behavior if a user selects a number of passengers and later
navs back and selects a different number. If they select a higher number, the existing
pages need to be left alone and more pages need added. If they select a lower number,
the pages in excess of a new passanger number need removed while pages still in selected
number should be left alone.

TODO: fix behavior - when changed to a higher number on a second change the fwd button on
the page stays bound to tab4NextClicked still? Leave test prints untill addressed."""
        existingWidget = self.ui.stackedWidget.widget(i-1)
        nextWidget=self.ui.stackedWidget.widget(i)
        if existingWidget != None:#if there is already a widget
            #print("THE EXISTING WIDGET IS: "+str(existingWidget.objectName()))
            if i==self.passCount and nextWidget != None:
                #if on last iteration and there's still more widgets after in stackedWidget
                #print("#if on last iteration and there's still more widgets after in stackedWidget, process")
                ##go through and remove them
                moreWidgets=True
                widgetIndex=i
                while moreWidgets:
                    #print("removing widget at index ", widgetIndex)
                    self.ui.stackedWidget.removeWidget(self.ui.stackedWidget.widget(widgetIndex))
                    widgetIndex+=1
                    widgetAfterNext=self.ui.stackedWidget.widget(widgetIndex)
                    if widgetAfterNext == None:
                        #print("No more widgets at indes ", widgetIndex)
                        moreWidgets=False
                if self.ui.stackedWidget.currentIndex()>self.passCount:
                    self.ui.stackedWidget.setCurrentIndex(self.passCount)
                #print("name of grandparent ", self.ui.fwdStackNavButton.parent().parent().objectName())
                self.page=self.ui.fwdStackNavButton.parent().parent().findChild(QtGui.QWidget,"passPage"+str(self.passCount))
                #print("PAGE=", self.page.objectName())
                self.fwd=self.page.findChild(QtGui.QPushButton, "fwdStackNavButton")
                #print("fwd=", self.fwd.objectName())
                try:
                    self.fwd.clicked.disconnect(self.fwdStackNavClicked)#disconnect old signal from fwdStackNavButton.clicked
                except:
                    pass
                self.fwd.clicked.connect(self.tab4NextClicked)#connect signal from fwdStackNavButton.clicked
                self.fwd.setGeometry(QtCore.QRect(640, 10, 61, 27))
                self.fwd.setText(_translate("MainWindow", "Next ->", None))
                #print(self.fwd.parent().objectName())
                return
            elif i==self.passCount and nextWidget==None: #if both at end and no change happened
                #print("#if both at end and no change happened, return")
                return
            elif i!=self.passCount and nextWidget!=None:
                #print("if there are more widgets in existing stackedWidget and more iterations to go, return")
                #if there are more widgets in existing stackedWidget and more iterations to go
                return #this iteration doesn't need changed
            elif i!=self.passCount and nextWidget==None:
                #if we're on the last widget in existing stackedWidget and more iterations to go
                #print("if we're on the last widget in existing stackedWidget and more iterations to go, process")

                self.ui.fwdStackNavButton.setGeometry(QtCore.QRect(640, 10, 31, 27))
                try:
                    self.ui.fwdStackNavButton.clicked.disconnect(self.tab4NextClicked)#connect signal from fwdStackNavButton.clicked             
                    #print(self.ui.fwdStackNavButton.objectName(), ".tab4NextClicked should be disconnected now")
                except:
                    pass
                self.ui.fwdStackNavButton.clicked.connect(self.fwdStackNavClicked)#connect signal from fwdStackNavButton.clicked
                self.ui.fwdStackNavButton.setText(_translate("MainWindow", ">", None))
                return
            
        self.ui.passPage = QtGui.QWidget()
        passPageI="passPage"+str(i)
        passStr="Passenger "+str(i)
        self.ui.passPage.setObjectName(passPageI)
        self.ui.gridLayout_16 = QtGui.QGridLayout(self.ui.passPage)
        self.ui.gridLayout_16.setObjectName("gridLayout_16"+str(i))
        self.ui.fwdBackNavWidget = QtGui.QWidget(self.ui.passPage)
        self.ui.fwdBackNavWidget.setMaximumSize(QtCore.QSize(50, 50))
        self.ui.fwdBackNavWidget.setObjectName("fwdBackNavWidget"+str(i))
        self.ui.gridLayout_16.addWidget(self.ui.fwdBackNavWidget, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.ui.passengerGroupBox = QtGui.QGroupBox(self.ui.passPage)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ui.passengerGroupBox.setFont(font)
        self.ui.passengerGroupBox.setObjectName("passengerGroupBox"+str(i))
        self.ui.gridLayout_12 = QtGui.QGridLayout(self.ui.passengerGroupBox)
        self.ui.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"+str(i)))
        self.ui.seatGroupBox = QtGui.QGroupBox(self.ui.passengerGroupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ui.NameAddressGroupBox = QtGui.QGroupBox(self.ui.passengerGroupBox)
        self.ui.NameAddressGroupBox.setObjectName(_fromUtf8("NameAddressGroupBox"+str(i)))
        self.ui.gridLayout_19 = QtGui.QGridLayout(self.ui.NameAddressGroupBox)
        self.ui.gridLayout_19.setObjectName(_fromUtf8("gridLayout_19"+str(i)))
        self.ui.mrAlignWidget = QtGui.QWidget(self.ui.NameAddressGroupBox)
        self.ui.mrAlignWidget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.ui.mrAlignWidget.setObjectName(_fromUtf8("mrAlignWidget"+str(i)))
        self.ui.gridLayout_18 = QtGui.QGridLayout(self.ui.mrAlignWidget)
        self.ui.gridLayout_18.setMargin(0)
        self.ui.gridLayout_18.setObjectName(_fromUtf8("gridLayout_18"+str(i)))
        self.ui.mrsRadioButton = QtGui.QRadioButton(self.ui.mrAlignWidget)
        self.ui.mrsRadioButton.setObjectName(_fromUtf8("mrsRadioButton"+str(i)))
        self.ui.gridLayout_18.addWidget(self.ui.mrsRadioButton, 0, 2, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.mrRadioButton = QtGui.QRadioButton(self.ui.mrAlignWidget)
        self.ui.mrRadioButton.setObjectName(_fromUtf8("mrRadioButton"+str(i)))
        self.ui.gridLayout_18.addWidget(self.ui.mrRadioButton, 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.msRadioButton = QtGui.QRadioButton(self.ui.mrAlignWidget)
        self.ui.msRadioButton.setObjectName(_fromUtf8("msRadioButton"+str(i)))
        self.ui.gridLayout_18.addWidget(self.ui.msRadioButton, 0, 3, 1, 1)
        self.ui.gridLayout_19.addWidget(self.ui.mrAlignWidget, 0, 1, 1, 1)
        self.ui.passFirstLabel = QtGui.QLabel(self.ui.NameAddressGroupBox)
        self.ui.passFirstLabel.setObjectName(_fromUtf8("passFirstLabel"))
        self.ui.gridLayout_19.addWidget(self.ui.passFirstLabel, 1, 0, 1, 1)
        self.ui.passCityLabel = QtGui.QLabel(self.ui.NameAddressGroupBox)
        self.ui.passCityLabel.setObjectName(_fromUtf8("passCityLabel"))
        self.ui.gridLayout_19.addWidget(self.ui.passCityLabel, 5, 0, 1, 1)
        self.ui.passAddressLabel = QtGui.QLabel(self.ui.NameAddressGroupBox)
        self.ui.passAddressLabel.setObjectName(_fromUtf8("passAddressLabel"))
        self.ui.gridLayout_19.addWidget(self.ui.passAddressLabel, 4, 0, 1, 1)
        self.ui.passFirstLineEdit = QtGui.QLineEdit(self.ui.NameAddressGroupBox)
        self.ui.passFirstLineEdit.setObjectName(_fromUtf8("passFirstLineEdit"+str(i)))
        self.ui.gridLayout_19.addWidget(self.ui.passFirstLineEdit, 1, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.passLastLabel = QtGui.QLabel(self.ui.NameAddressGroupBox)
        self.ui.passLastLabel.setObjectName(_fromUtf8("passLastLabel"))
        self.ui.gridLayout_19.addWidget(self.ui.passLastLabel, 3, 0, 1, 1)
        self.ui.PassLastLineEdit = QtGui.QLineEdit(self.ui.NameAddressGroupBox)
        self.ui.PassLastLineEdit.setObjectName(_fromUtf8("passLastLineEdit"+str(i)))
        self.ui.gridLayout_19.addWidget(self.ui.PassLastLineEdit, 3, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.passAddressLineEdit = QtGui.QLineEdit(self.ui.NameAddressGroupBox)
        self.ui.passAddressLineEdit.setObjectName(_fromUtf8("passAddressLineEdit"+str(i)))
        self.ui.gridLayout_19.addWidget(self.ui.passAddressLineEdit, 4, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.passCityLineEdit = QtGui.QLineEdit(self.ui.NameAddressGroupBox)
        self.ui.passCityLineEdit.setObjectName(_fromUtf8("passCityLineEdit"+str(i)))
        self.ui.gridLayout_19.addWidget(self.ui.passCityLineEdit, 5, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.passStateLabel = QtGui.QLabel(self.ui.NameAddressGroupBox)
        self.ui.passStateLabel.setObjectName(_fromUtf8("passStateLabel"))
        self.ui.gridLayout_19.addWidget(self.ui.passStateLabel, 6, 0, 1, 1)
        self.ui.passStateComboBox = QtGui.QComboBox(self.ui.NameAddressGroupBox)
        self.ui.passStateComboBox.setObjectName(_fromUtf8("passStateComboBox"+str(i)))
        states=['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
        self.ui.passStateComboBox.insertItems (0, states)
        self.ui.gridLayout_19.addWidget(self.ui.passStateComboBox, 6, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.passZipLabel = QtGui.QLabel(self.ui.NameAddressGroupBox)
        self.ui.passZipLabel.setObjectName(_fromUtf8("passZipLabel"))
        self.ui.gridLayout_19.addWidget(self.ui.passZipLabel, 7, 0, 1, 1)
        self.ui.passZipLineEdit = QtGui.QLineEdit(self.ui.NameAddressGroupBox)
        self.ui.passZipLineEdit.setObjectName(_fromUtf8("passZipLineEdit"+str(i)))
        self.ui.gridLayout_19.addWidget(self.ui.passZipLineEdit, 7, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.gridLayout_12.addWidget(self.ui.NameAddressGroupBox, 0, 0, 6, 1)
        self.ui.gridLayout_16.addWidget(self.ui.passengerGroupBox, 1, 0, 1, 1)
        self.ui.fwdStackNavButton = QtGui.QPushButton(self.ui.passPage)
        self.ui.fwdStackNavButton.setObjectName(_fromUtf8("fwdStackNavButton"))
        if i == self.passCount: #if on last passanger
            self.ui.fwdStackNavButton.setGeometry(QtCore.QRect(640, 10, 61, 27))
            self.ui.fwdStackNavButton.clicked.connect(self.tab4NextClicked)#connect signal from fwdStackNavButton.clicked
            self.ui.fwdStackNavButton.setText(_translate("MainWindow", "Next ->", None))
        else:
            self.ui.fwdStackNavButton.setGeometry(QtCore.QRect(640, 10, 31, 27))
            self.ui.fwdStackNavButton.clicked.connect(self.fwdStackNavClicked)#connect signal from fwdStackNavButton.clicked
            self.ui.fwdStackNavButton.setText(_translate("MainWindow", ">", None))
        if not i==1:
            self.ui.backStackNavButton = QtGui.QPushButton(self.ui.passPage)
            self.ui.backStackNavButton.setObjectName("backStackNavButton")
            self.ui.backStackNavButton.setGeometry(QtCore.QRect(610, 10, 31, 27))
            self.ui.backStackNavButton.clicked.connect(self.backStackNavButton)#connect signal from fwdStackNavButton.clicked
            self.ui.backStackNavButton.setText(_translate("MainWindow", "<", None))
        self.ui.stackedWidget.addWidget(self.ui.passPage)
        self.ui.seatGroupBox.setFont(font)
        self.ui.seatGroupBox.setObjectName(_fromUtf8("seatGroupBox"+str(i)))
        self.ui.gridLayout_21 = QtGui.QGridLayout(self.ui.seatGroupBox)
        self.ui.gridLayout_21.setObjectName(_fromUtf8("gridLayout_21"+str(i)))
        self.ui.windowRadioButton = QtGui.QRadioButton(self.ui.seatGroupBox)
        self.ui.windowRadioButton.setObjectName(_fromUtf8("windowRadioButton"+str(i)))
        self.ui.gridLayout_21.addWidget(self.ui.windowRadioButton, 2, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.aisleRadioButton = QtGui.QRadioButton(self.ui.seatGroupBox)
        self.ui.aisleRadioButton.setObjectName(_fromUtf8("aisleRadioButton"+str(i)))
        self.ui.gridLayout_21.addWidget(self.ui.aisleRadioButton, 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.centerRadioButton = QtGui.QRadioButton(self.ui.seatGroupBox)
        self.ui.centerRadioButton.setObjectName(_fromUtf8("centerRadioButton"+str(i)))
        self.ui.gridLayout_21.addWidget(self.ui.centerRadioButton, 1, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.gridLayout_12.addWidget(self.ui.seatGroupBox, 0, 2, 2, 1)
        self.ui.bagGroupBox = QtGui.QGroupBox(self.ui.passengerGroupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ui.bagGroupBox.setFont(font)
        self.ui.bagGroupBox.setObjectName(_fromUtf8("bagGroupBox"+str(i)))
        self.ui.gridLayout_46 = QtGui.QGridLayout(self.ui.bagGroupBox)
        self.ui.gridLayout_46.setObjectName(_fromUtf8("gridLayout_46"+str(i)))
        self.ui.bagSpinBox = QtGui.QSpinBox(self.ui.bagGroupBox)
        self.ui.bagSpinBox.setObjectName(_fromUtf8("bagSpinBox"+str(i)))
        self.ui.gridLayout_46.addWidget(self.ui.bagSpinBox, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.ui.gridLayout_12.addWidget(self.ui.bagGroupBox, 2, 2, 2, 1)
        self.ui.specialGroupBox = QtGui.QGroupBox(self.ui.passengerGroupBox)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ui.specialGroupBox.setFont(font)
        self.ui.specialGroupBox.setObjectName(_fromUtf8("specialGroupBox"+str(i)))
        self.ui.verticalLayout_2 = QtGui.QVBoxLayout(self.ui.specialGroupBox)
        self.ui.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"+str(i)))
        self.ui.handiCheckBox = QtGui.QCheckBox(self.ui.specialGroupBox)
        self.ui.handiCheckBox.setObjectName(_fromUtf8("handiCheckBox"+str(i)))
        self.ui.verticalLayout_2.addWidget(self.ui.handiCheckBox)
        self.ui.mealCheckBox = QtGui.QCheckBox(self.ui.specialGroupBox)
        self.ui.mealCheckBox.setObjectName(_fromUtf8("mealCheckBox"+str(i)))
        self.ui.verticalLayout_2.addWidget(self.ui.mealCheckBox)
        self.ui.commentsLabel = QtGui.QLabel(self.ui.specialGroupBox)
        self.ui.commentsLabel.setObjectName(_fromUtf8("commentsLabel"))
        self.ui.verticalLayout_2.addWidget(self.ui.commentsLabel)
        self.ui.commentsTextEdit = QtGui.QTextEdit(self.ui.specialGroupBox)
        self.ui.commentsTextEdit.setObjectName(_fromUtf8("commentsTextEdit"+str(i)))
        self.ui.verticalLayout_2.addWidget(self.ui.commentsTextEdit)
        self.ui.gridLayout_12.addWidget(self.ui.specialGroupBox, 4, 2, 2, 1)
        self.ui.passengerGroupBox.setTitle(_translate("MainWindow", passStr, None))
        self.ui.seatGroupBox.setTitle(_translate("MainWindow", "Seat Selection *Optional", None))
        self.ui.windowRadioButton.setText(_translate("MainWindow", "Window", None))
        self.ui.aisleRadioButton.setText(_translate("MainWindow", "Aisle", None))
        self.ui.centerRadioButton.setText(_translate("MainWindow", "Center", None))
        self.ui.bagGroupBox.setTitle(_translate("MainWindow", "Checked Bags", None))
        self.ui.specialGroupBox.setTitle(_translate("MainWindow", "Special Requests *Optional", None))
        self.ui.handiCheckBox.setText(_translate("MainWindow", "Handicap", None))
        self.ui.mealCheckBox.setText(_translate("MainWindow", "Meal Service", None))
        self.ui.commentsLabel.setText(_translate("MainWindow", "Comments:", None))
        self.ui.NameAddressGroupBox.setTitle(_translate("MainWindow", "Name/Address", None))
        self.ui.passFirstLabel.setText(_translate("MainWindow", "First:", None))
        self.ui.passCityLabel.setText(_translate("MainWindow", "City:", None))
        self.ui.passAddressLabel.setText(_translate("MainWindow", "Address:", None))
        self.ui.passLastLabel.setText(_translate("MainWindow", "Last:", None))
        self.ui.passStateLabel.setText(_translate("MainWindow", "State:", None))
        self.ui.passZipLabel.setText(_translate("MainWindow", "Zip:", None))
        self.ui.mrsRadioButton.setText(_translate("MainWindow", "Mrs.", None))
        self.ui.mrRadioButton.setText(_translate("MainWindow", "Mr.", None))
        self.ui.msRadioButton.setText(_translate("MainWindow", "Ms.", None))
        ###########################

    ############################ END TAB 4 - PASSENGER INFO TAB ##############################


    ############################## START TAB 5 - PAYMENT TAB #################################

    ###########################
    def populateCostTable(self, rowNum, rowDataList):
        """Args: current rowNum, a list of data from that row
TODO: cost table was unfortuantly called departingTableWidget_2 much earlier. Fix"""
        flightNum = QtGui.QTableWidgetItem(rowDataList[0])
        costPSNum = QtGui.QTableWidgetItem("$"+rowDataList[1])
        costTotal = QtGui.QTableWidgetItem("$"+str(float(rowDataList[1])* self.passCount))
        #setting the flight number to first column
        self.ui.departingTableWidget_2.setItem(rowNum, 0, flightNum)
        #setting the item for the departing flight
        self.ui.departingTableWidget_2.setItem(rowNum, 1, costPSNum)
        #setting the item for the arriving flight
        self.ui.departingTableWidget_2.setItem(rowNum, 2, costTotal)
        return float(rowDataList[1])
    ###########################

    ###########################
    
    def generateTab5Table(self, data):
        """function will set rowCount to how many items in possible flight matches and set the
row count of the table to that number. It will call createTab1Table once and for as many times
as in rowCount it  will call populateTab1Table with the iteration and the list of data
field at that index"""
        #rowCount == number of lists nested in testData list
        rowCount=len(data)
        #setting the row count for the tableWidget to the number of rows represented in testData
        self.ui.departingTableWidget_2.setRowCount(rowCount+1)
        #setting the column count
        self.ui.departingTableWidget_2.setColumnCount(3)
        #setting the flight column width
        self.ui.departingTableWidget_2.setColumnWidth(0, 490)
        #setting the costPS column width
        self.ui.departingTableWidget_2.setColumnWidth(1, 100)
        #setting the costTotal column width
        self.ui.departingTableWidget_2.setColumnWidth(2, 90)
        #Header items
        flightHeader = QtGui.QTableWidgetItem('Flight')
        costPSHeader = QtGui.QTableWidgetItem('Cost Per Seat')
        costTotalHeader = QtGui.QTableWidgetItem('Total Cost')
        #setting the header items
        self.ui.departingTableWidget_2.setHorizontalHeaderItem(0, flightHeader)
        self.ui.departingTableWidget_2.setHorizontalHeaderItem(1, costPSHeader)
        self.ui.departingTableWidget_2.setHorizontalHeaderItem(2, costTotalHeader)
        #This is where I don't know how to make it one dimensional. I am trying to figure out how
        #to make this one dimensional but I can't. When it gets populated it just say 'L' for the first
        #column 'e' for the second column and 'g' for the third column. I am trying to delete some things
        #but either the syntax is wrong or it still doesn't print right.
        perSeatTotal=0
        for i in range(rowCount):
            perSeatTotal+=self.populateCostTable(i,data[i])
        self.populateCostTable(rowCount,['TRIP TOTAL:', str(perSeatTotal)])
    

    ###########################    
    def checkComplete(self):
        """This function will check if complete - altered for testing currently"""
        blanks= self.getBlankInputs(self.getInputs("paymentTab"))
        if True:#TEMP CODE -blanks should be 0 on completion once fill in cost box
            self.ui.paymentTab.state=True
            return True
        else:
            self.ui.paymentTab.state=False
            self.dialogBlankFields(blanks)
            return False
    ###########################

    ###########################
    def processPurchase(self):
        """Function unpacks and prepares params from stored data from all data entered throughout GUI in db
and calls onnectDB class functions to insert data appropriate numbers of times when either one or many records
need entered in a table for a reservation. It then calls reset GUI on success."""
        if self.checkComplete():
            self.paymentInput={k.objectName():v for (k,v) in self.getInputs("paymentTab").items()}
            db=cnx.connectDB()
            ###test print section - leave for now###
            """
            try:
                {print("flightInfoInput="+k,v) for (k,v) in self.flightInfoInput.items()}
            except:
                pass
            [print("flightSelectionInput="+str(i)) for i in self.flightSelectionInput]
            [print("flightSelection="+str(i)) for i in self.flightSelection]
            [print("flightCost="+str(i)) for i in self.flightCost]
            [print("flightSelectionInput2="+str(i)) for i in self.flightSelectionInput2]
            [print("flightSelection2="+str(i)) for i in self.flightSelection2]
            [print("flightCost2="+str(i)) for i in self.flightCost2]

            try:
                {print("paymentInput="+k,v) for (k,v) in self.paymentInput.items()}

            except:
                pass
            for i in self.passInfoInput:
                {print("passInfoInput="+k,v) for (k,v) in i.items()}
            """
            """
***lauchFlyRightClass ELEMENT PARAMS***
passInfoInput=passStateComboBox1 Alabama
passInfoInput=centerRadioButton1 Center
passInfoInput=passCityLineEdit1 ct1
passInfoInput=mrRadioButton1 Mr.
passInfoInput=passAddressLineEdit1 ad1
passInfoInput=passZipLineEdit1 zp1
passInfoInput=passLastLineEdit1 l1
passInfoInput=passFirstLineEdit1 f1

***db psudocode***
in init:
    self.customerIds=[]
def insertCustomer(fname, lname, address, city, zip, email=None):#in case I have time to add in an email field later to replace salutaion radios
    INSERT INTO customer...;
    self.customerIds.append(SELECT last_inputed id);
***AFFECTED TABLES(S)***
CUSTOMER:    
+---------+--------------+------+-----+---------+----------------+
| Field   | Type         | Null | Key | Default | Extra          |
+---------+--------------+------+-----+---------+----------------+
| id      | mediumint(9) |      | PRI | NULL    | auto_increment |
| fname   | varchar(20)  |      |     |         |                |
| lname   | varchar(30)  |      |     |         |                |
| address | varchar(200) |      |     |         |                |
| city    | varchar(50)  |      |     |         |                |
| zip     | int(11)      |      |     | 0       |                |
| email   | varchar(100) | YES  |     | NULL    |                |
+---------+--------------+------+-----+---------+----------------+"""
        self.resultInsCust=False
        for i in range(self.passCount):
            zipCode=self.passInfoInput[i]["passZipLineEdit"+str(i+1)]
            #print("zipCode=",zipCode)
            self.resultInsCust=db.insertCustomer(self.passInfoInput[i]["passFirstLineEdit"+str(i+1)],self.passInfoInput[i]["passLastLineEdit"+str(i+1)], self.passInfoInput[i]["passAddressLineEdit"+str(i+1)],self.passInfoInput[i]["passCityLineEdit"+str(i+1)],zipCode)

        """
***lauchFlyRightClass ELEMENT PARAMS***
* payment.amount= sum([float(i) for i in self.flightCost2+self.flightCost])
* payment.day=(get in db class)
* payment.card_name=paymentInput=creditNameLineEdit cnam1
* payment.method=paymentInput=visaRadioButton Visa
* payment.number=paymentInput=cardNumberLineEdit cnum1
* payment.ccv=paymentInput=cvvLineEdit ccv1
* payment.card_date=paymentInput=creditDateEdit 3/1/2015
***db psudocode***
def insertPayment(amount, method, number, ccv, cardDate, cardName):
    INSERT INTO PAYMENT... VALUES(datetime.datetime(), method, number, ccv, cardDate, cardName);
    paymentID=SELECT last_inputed_id();#look up method
    self.insertRes(paymentId)
def insertRes(self, paymentId):
    INSERT INTO reservation (payment_id) VALUES ({{paymentId}});
    self.resId=SELECT last_inputed id;
****AFFECTED TABLES(S)***
PAYMENT:
+-----------+--------------+------+-----+---------------------+----------------+
| Field     | Type         | Null | Key | Default             | Extra          |
+-----------+--------------+------+-----+---------------------+----------------+
| id        | mediumint(9) |      | PRI | NULL                | auto_increment |
| amount    | decimal(7,2) |      |     | 0.00                |                |
| day       | datetime     |      |     | 0000-00-00 00:00:00 |                |
| method    | varchar(11)  |      |     |                     |                |
| number    | bigint(20)   |      |     | 0                   |                |
| ccv       | smallint(6)  |      |     | 0                   |                |
| card_date | datetime     |      |     | 0000-00-00 00:00:00 |                |
| card_name | varchar(30)  |      |     |                     |                |
+-----------+--------------+------+-----+---------------------+----------------+
RESERVATION:
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| id         | mediumint(9) |      | PRI | NULL    | auto_increment |
| payment_id | mediumint(9) |      | MUL | 0       |                |
+------------+--------------+------+-----+---------+----------------+
"""
        self.resultInsPay=False
        if self.resultInsCust:
            method="AmEx"
            try:
                method=self.paymentInput['visaRadioButton']
            except:
                try:
                    method=self.paymentInput['mcRadioButton'] 
                except:
                    pass
            amount=sum([float(i) for i in self.flightCost2+self.flightCost])
            self.resultInsPay=db.insertPayment(amount, method, self.paymentInput["cardNumberLineEdit"],self.paymentInput["cvvLineEdit"],self.paymentInput["creditDateEdit"],self.paymentInput["creditNameLineEdit"])
        
        """
***lauchFlyRightClass ELEMENT PARAMS***
self.flightSelectionInput=6
***db psudocode***
def updateSeat(self, flight):
    seatIds=[]=SELECT id FROM seat WHERE flight_id={{flightSelectionInput=6}};
    UPDATE seat SET available=0 WHERE id={{seatId}};
****AFFECTED TABLES(S)***
SEAT:
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| id        | mediumint(9) |      | PRI | NULL    | auto_increment |
| position  | char(1)      |      |     |         |                |
| flight_id | mediumint(9) |      | MUL | 0       |                |
| available | tinyint(1)   |      |     | 1       |                |
+-----------+--------------+------+-----+---------+----------------+"""

        self.resultUpdateSeat=False
        #print("self.resultInsPay=",self.resultInsPay)
        if self.resultInsPay:
            for i in range(self.passCount):
                #print("self.flightSelectionInput=",self.flightSelectionInput)
                for flight in self.flightSelectionInput:
                    print("flight=",flight)
                    self.resultUpdateSeat=db.updateSeat(flight)
                for flight in self.flightSelectionInput2:
                    print("flight2=",flight)
                    self.resultUpdateSeat=db.updateSeat(flight)
        else:
            dialog=Dialog()
            dialog.addText("Payment could not be submitted - Please verify information")
            dialog.completeText()
            dialog.exec_()    
            

        """
***lauchFlyRightClass ELEMENT PARAMS***
commentsTextEdit1: 'comment'
mealCheckBox1: 'Meal Service',
windowRadioButton1: 'Window',
handiCheckBox1: 'Handicap', 
passInfoInput=qt_spinbox_lineedit 0 ####TODO!!! change to append i
passInfoInput=qt_spinbox_lineedit 2
passInfoInput=centerRadioButton1 Center
passInfoInput=windowRadioButton2 Window
passInfoInput=passStateComboBox2 Florida
passInfoInput=qt_spinbox_lineedit 0
* passenger.class=flightInfoInput=firstRadioButton First Class    

***db psudocode***
    def insertPassenger(self,i, hasMeal, numBags, hasAssist, isComment, rateClass):
    INSERT INTO PASSENGER...
****AFFECTED TABLES(S)***
PASSENGER:!*!*!NEED VALUES !*!*!
+----------------+--------------+------+-----+---------+----------------+
| Field          | Type         | Null | Key | Default | Extra          |
+----------------+--------------+------+-----+---------+----------------+
| id             | mediumint(9) |      | PRI | NULL    | auto_increment |
| customer_id    | mediumint(9) |      | MUL | 0       |                |
| reservation_id | mediumint(9) |      | MUL | 0       |                |
| seat_id        | mediumint(9) |      | MUL | 0       |                |
| meal           | tinyint(1)   |      |     | 0       |                |
| bags  !*!*!    | int(2)       |      |     | 0       |                |
| assist         | tinyint(1)   |      |     | 0       |                |
| comment        | varchar(200) | YES  |     | NULL    |                |
| class          | tinyint(1)   |      |     | 0       |                |
+----------------+--------------+------+-----+---------+----------------+

"""
        if self.resultUpdateSeat:
            resId=False
            for i in range(self.passCount):
                try:
                    rateClass=self.flightInfoInput["firstRadioButton"]
                    rateClass=1
                except:
                    rateClass=0
                hasMeal=0
                try:
                    hasMeal=self.passInfoInput[i]['mealCheckBox'+str(i+1)]
                    hasMeal=1
                except:
                    pass
                numBags=self.passInfoInput[i]['qt_spinbox_lineedit']
                hasAssist=0
                try:
                    hasAssist=self.passInfoInput[i]['handiCheckBox'+str(i+1)]
                    hasAssist=1
                except:
                    pass
                comment=None
                try:
                    comment=self.passInfoInput[i]['commentsTextEdit'+str(i+1)]
                except:
                    pass
                resId=db.insertPassenger(i,hasMeal,numBags,hasAssist,comment,rateClass)
            if not resId:
                dialog=Dialog()
                dialog.addText("System error in inputting reservation - please contact tech to manually assign seat.")
                dialog.completeText()
                dialog.exec_()   
            else:
                dialog=Dialog()
                dialog.addText("<div>Thanks for flying right!</div><div>Your Reservation ID is: "+str(resId)+".</div>")
                dialog.completeText()
                dialog.exec_()   
                db.reset()
                self.resetGUI()
        else:
            dialog=Dialog()
            dialog.addText("Unspecified error in inputting reservation - please verify information and retry.")
            dialog.completeText()
            dialog.exec_()            
            
            
    ###########################
            
    ################################
    def resetGUI(self):
        """function will reset GUI display and data back to starting values and reset user on first page """
        self.setInputs("lookupTab")
        self.setInputs("flightInfoTab")
        self.setInputs("flightSelectTab")
        self.setInputs("passInfoTab")
        self.setInputs("paymentTab")
        self.ui.flightInfoTab.state=False;
        self.ui.flightSelectTab.state=False;
        self.ui.passInfoTab.state=False;
        self.ui.paymentTab.state=False;
        self.passInfoInput=[]
        self.flightSelectionInput=[]
        self.flightInfoInput=[]
        self.flightSelectionInput2=[]
        self.flightInfoInput2=[]
        self.paymentInput=[]
        self.ui.tabWidget.setTabEnabled(1, False)
        self.ui.tabWidget.setTabEnabled(2, False)
        self.returnTrip=True
        
    ################################
            
    ################################    
    def cancelPurchase(self):
        """Dialogs a confirmation the user wants to cancel, if so calls resetGUI"""
        dialog = Dialog()
        dialog.addText("Are you sure you want to cancel?")
        dialog.completeText()
        dialog.pushButton.setText(_translate("Dialog", "Confirm", None))
        dialog.addCancelOpt()
        isConfirm=dialog.exec_()
        if isConfirm:
            self.resetGUI()

    ################################
        
    ############################### END TAB 54 - PAYMENT TAB #################################

########################  END Main class  #####################################

#######################  START Dialog class  ##################################
    """This class connects to dialog.ui pyQT generated file. It allows creation of Dialog objects
that can alert users of errors"""
    """TODO OPTIONAL: make prettier. def alert(textStr) so smaller dialog box can be called with
less steps out of class. def addTitle(textStr) so titles bold/centered"""
class Dialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self): #constuctor
        QtGui.QDialog.__init__(self)
        self.setupUi(self)       #build it
        #Set class variables of strings that can be concatinated together in functions (see below)
        #that allow class user to pass params of text strings that will create the html for
        #the textBrowser object's setHtml method.
        self.HTMLstart="<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
        self.HTMLend="</p>\n<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"
        self.textStart="<span style=\" font-size:8pt;\">"
        self.textEnd="</span>"
        self.textStr=""
        #bind OK buttons signal to OKclicked slot
        self.pushButton.clicked.connect(self.OKclicked)
    ###########################

    ###########################
    def addText(self, textToAdd):
        """Arg: text string
Sets textStr to a HTML span with text string.
completeText needs called after all calls to this function."""
        self.textStr+=self.textStart+textToAdd+self.textEnd

    ###########################
    def completeText(self):
        """Completes the HTML for the textBrowser's setHtml method.
Finishes use of class object."""
        self.fullHTML=self.HTMLstart+self.textStr+self.HTMLend
        self.textBrowser.setHtml(_translate("Dialog",self.fullHTML, None))
    ###########################

    ###########################
    def addCancelOpt(self):
        """Adds a 'cancel' button to Dialog object. ('OK' button built in)"""
        self.dialogCancelButton = QtGui.QPushButton(self)
        self.dialogCancelButton.setGeometry(QtCore.QRect(130, 270, 75, 23))
        self.dialogCancelButton.setObjectName(_fromUtf8("dialogCancelButton"))
        self.dialogCancelButton.setText(_translate("Dialog", "Cancel", None))
        self.dialogCancelButton.clicked.connect(self.cancelClicked)
    ###########################

    ###########################
    def OKclicked(self):
        """SLOT: processes accept button clicked and returns True"""
        self.accept()
        return True
    ###########################

    ###########################
    def cancelClicked(self):
        """SLOT: processes reject button clicked and returns False"""
        self.reject()
        return False
    ###########################
        

########################  call QtGui and Main  ################################
if __name__ == '__main__':              #if pyQT generated code feature tests as generated correctly
    app = QtGui.QApplication(sys.argv)  #app = a pyQT application
    main = Main()                       #main = object created by calling Main()
    main.show()                         #display the GUI
    sys.exit(app.exec_())               #exit the app
