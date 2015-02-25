import sys #sys calls like exit
from PyQt4 import QtCore, QtGui #pyQT modules
from FlyRightAirlines import Ui_MainWindow #QT Designer generated code


#### set up compatibility with pyQT designer generated functions ####
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

        
        self.ui = Ui_MainWindow()        # build ui
        self.ui.setupUi(self)

        self.passCount=0        #declare var as this will be needed several places
        

        ###########################
        self.ui.passComboBox.currentIndexChanged.connect(self.currentIndexChanged) #connect pyqt signal to py slot
    def currentIndexChanged(self, index):#create slot
        self.passCount=index+1 #signal sent is index from 0, passCount should start at 1
        self.genStackedWidget() #genStackedWidget based on passCount
        self.ui.gridLayout_36.addWidget(self.ui.stackedWidget, 1, 0, 1, 1) #add it to the parent elt
        ###########################
        
        ###########################
        """Create a Passanger Page to go in StackedWidget.
        passengerGroupBox title = 'Passenger '+str(i)
        all object names their existing value +str(i)
        with expection of back & fwd buttons"""
    def genPassOptions(self, i):
        self.ui.passPage = QtGui.QWidget()
        passPageI="passPage"+str(i)
        passStr="Passenger "+str(i)
        self.ui.passPage.setObjectName(passPageI)
        self.ui.gridLayout_16 = QtGui.QGridLayout(self.ui.passPage)
        self.ui.gridLayout_16.setObjectName("gridLayout_16"+str(i))
        self.ui.fwdBackNavWidget = QtGui.QWidget(self.ui.passPage)
        self.ui.fwdBackNavWidget.setMaximumSize(QtCore.QSize(50, 50))
        self.ui.fwdBackNavWidget.setObjectName("fwdBackNavWidget"+str(i))
        self.ui.horizontalLayout_2 = QtGui.QHBoxLayout(self.ui.fwdBackNavWidget)
        self.ui.horizontalLayout_2.setSpacing(0)
        self.ui.horizontalLayout_2.setMargin(0)
        self.ui.horizontalLayout_2.setObjectName("horizontalLayout_2"+str(i))
        self.ui.backStackNavButton = QtGui.QPushButton(self.ui.fwdBackNavWidget)
        self.ui.backStackNavButton.setObjectName("backStackNavButton")
        self.ui.horizontalLayout_2.addWidget(self.ui.backStackNavButton)
        self.ui.fwdStackNavButton = QtGui.QPushButton(self.ui.fwdBackNavWidget)
        self.ui.fwdStackNavButton.setObjectName("fwdStackNavButton")
        self.ui.horizontalLayout_2.addWidget(self.ui.fwdStackNavButton)
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
        self.ui.NameAddressGroupBox = QtGui.QGroupBox(self.ui.passengerGroupBox)
        self.ui.NameAddressGroupBox.setObjectName(_fromUtf8("NameAddressGroupBox"+str(i)))
        self.ui.gridLayout_19 = QtGui.QGridLayout(self.ui.NameAddressGroupBox)
        self.ui.gridLayout_19.setObjectName(_fromUtf8("gridLayout_19"+str(i)))
        self.ui.passFirstLabel = QtGui.QLabel(self.ui.NameAddressGroupBox)
        self.ui.passFirstLabel.setObjectName(_fromUtf8("passFirstLabel"))
        self.ui.gridLayout_19.addWidget(self.ui.passFirstLabel, 1, 0, 1, 1)
        self.ui.passAddressLineEdit = QtGui.QLineEdit(self.ui.NameAddressGroupBox)
        self.ui.passAddressLineEdit.setObjectName(_fromUtf8("passAddressLineEdit"+str(i)))
        self.ui.gridLayout_19.addWidget(self.ui.passAddressLineEdit, 4, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.passCityLabel = QtGui.QLabel(self.ui.NameAddressGroupBox)
        self.ui.passCityLabel.setObjectName(_fromUtf8("passCityLabel"))
        self.ui.gridLayout_19.addWidget(self.ui.passCityLabel, 5, 0, 1, 1)
        self.ui.passAddressLabel = QtGui.QLabel(self.ui.NameAddressGroupBox)
        self.ui.passAddressLabel.setObjectName(_fromUtf8("passAddressLabel"))
        self.ui.gridLayout_19.addWidget(self.ui.passAddressLabel, 4, 0, 1, 1)
        self.ui.passFirstLineEdit = QtGui.QLineEdit(self.ui.NameAddressGroupBox)
        self.ui.passFirstLineEdit.setObjectName(_fromUtf8("passFirstLineEdit"+str(i)))
        self.ui.gridLayout_19.addWidget(self.ui.passFirstLineEdit, 1, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.passMidLabel = QtGui.QLabel(self.ui.NameAddressGroupBox)
        self.ui.passMidLabel.setObjectName(_fromUtf8("passMidLabel"))
        self.ui.gridLayout_19.addWidget(self.ui.passMidLabel, 2, 0, 1, 1)
        self.ui.passMidLineEdit = QtGui.QLineEdit(self.ui.NameAddressGroupBox)
        self.ui.passMidLineEdit.setObjectName(_fromUtf8("passMidLineEdit"+str(i)))
        self.ui.gridLayout_19.addWidget(self.ui.passMidLineEdit, 2, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.passLastLabel = QtGui.QLabel(self.ui.NameAddressGroupBox)
        self.ui.passLastLabel.setObjectName(_fromUtf8("passLastLabel"))
        self.ui.gridLayout_19.addWidget(self.ui.passLastLabel, 3, 0, 1, 1)
        self.ui.PassLastLineEdit = QtGui.QLineEdit(self.ui.NameAddressGroupBox)
        self.ui.PassLastLineEdit.setObjectName(_fromUtf8("PassLastLineEdit"))
        self.ui.gridLayout_19.addWidget(self.ui.PassLastLineEdit, 3, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.ui.passCityLineEdit = QtGui.QLineEdit(self.ui.NameAddressGroupBox)
        self.ui.passCityLineEdit.setObjectName(_fromUtf8("passCityLineEdit"))
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
        self.ui.gridLayout_12.addWidget(self.ui.NameAddressGroupBox, 0, 0, 6, 1)
        self.ui.gridLayout_16.addWidget(self.ui.passengerGroupBox, 1, 0, 1, 1)
        self.ui.stackedWidget.addWidget(self.ui.passPage)
        self.ui.backStackNavButton.setText(_translate("MainWindow", "<", None))
        self.ui.fwdStackNavButton.setText(_translate("MainWindow", ">", None))
        self.ui.passengerGroupBox.setTitle(_translate("MainWindow", passStr, None))
        self.ui.seatGroupBox.setTitle(_translate("MainWindow", "Seat Selection", None))
        self.ui.windowRadioButton.setText(_translate("MainWindow", "Window", None))
        self.ui.aisleRadioButton.setText(_translate("MainWindow", "Aisle", None))
        self.ui.centerRadioButton.setText(_translate("MainWindow", "Center", None))
        self.ui.bagGroupBox.setTitle(_translate("MainWindow", "Checked Bags", None))
        self.ui.specialGroupBox.setTitle(_translate("MainWindow", "Special Requests", None))
        self.ui.handiCheckBox.setText(_translate("MainWindow", "Handicap", None))
        self.ui.mealCheckBox.setText(_translate("MainWindow", "Meal Service", None))
        self.ui.commentsLabel.setText(_translate("MainWindow", "Comments:", None))
        self.ui.NameAddressGroupBox.setTitle(_translate("MainWindow", "Name/Address", None))
        self.ui.passFirstLabel.setText(_translate("MainWindow", "First:", None))
        self.ui.passCityLabel.setText(_translate("MainWindow", "City:", None))
        self.ui.passAddressLabel.setText(_translate("MainWindow", "Address:", None))
        self.ui.passMidLabel.setText(_translate("MainWindow", "Middle:", None))
        self.ui.passLastLabel.setText(_translate("MainWindow", "Last:", None))
        self.ui.passStateLabel.setText(_translate("MainWindow", "State:", None))
        self.ui.passZipLabel.setText(_translate("MainWindow", "Zip:", None))
        self.ui.mrsRadioButton.setText(_translate("MainWindow", "Mrs.", None))
        self.ui.mrRadioButton.setText(_translate("MainWindow", "Mr.", None))
        self.ui.msRadioButton.setText(_translate("MainWindow", "Ms.", None))
        self.ui.fwdStackNavButton.clicked.connect(self.clicked)#connect signal from fwdStackNavButton.clicked
        ###########################
    
        ###########################
    def clicked(self): #slot for fwdStackNavButton.clicked
        #set stackedWidget.currentIndex 1 higher
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex()+1)
        #TODO: make it record data, prepopulate fields like address from first entry, make required fields...
        ###########################

    ##TODO: make a back button!

        ###########################
    def genStackedWidget(self):
        #generate a new passOptions page for each passenger in passCount
        for i in range(self.passCount):
            self.genPassOptions(i+1)
        ###########################

########################  END Main class  #####################################

########################  call QtGui and Main  ################################
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
