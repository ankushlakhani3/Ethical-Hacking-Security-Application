from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QComboBox, QLineEdit,QTextBrowser,QLabel
from PyQt5 import uic
import sys,subprocess,threading,types, time
import portScanner,ARPscan,MITM,Dos,DDos,BackdoorServer,xss,csrf
class Ui(QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("E:\project\guiapp\EHSA.ui", self)
        
        self.ps_comboBox = self.findChild(QComboBox, 'ps_comboBox')
        self.ps_lineEdit_1 = self.findChild(QLineEdit, 'ps_lineEdit_1')
        self.ps_lineEdit_2 = self.findChild(QLineEdit, 'ps_lineEdit_2')
        self.ps_pushButton = self.findChild(QPushButton, 'ps_pushButton') 
        self.ps_textBrowser = self.findChild(QTextBrowser, 'ps_textBrowser') 
        self.ps_pushButton.clicked.connect(self.uiportscan) 

        self.arps_comboBox = self.findChild(QComboBox, 'arps_comboBox')
        self.arps_lineEdit_1 = self.findChild(QLineEdit, 'arps_lineEdit_1')
        self.arps_pushButton = self.findChild(QPushButton, 'arps_pushButton') 
        self.arps_textBrowser = self.findChild(QTextBrowser, 'arps_textBrowser') 
        self.arps_pushButton.clicked.connect(self.uiarpscan) 

        self.mitm_lineEdit_1 = self.findChild(QLineEdit, 'mitm_lineEdit_1')
        self.mitm_lineEdit_2 = self.findChild(QLineEdit, 'mitm_lineEdit_2')
        self.mitm_pushButton = self.findChild(QPushButton, 'mitm_pushButton')
        self.mitm_textBrowser = self.findChild(QTextBrowser, 'mitm_textBrowser')
        self.mitm_pushButton.clicked.connect(self.uimitm) 

        self.dos_comboBox = self.findChild(QComboBox, 'dos_comboBox')
        self.dos_lineEdit = self.findChild(QLineEdit, 'dos_lineEdit')
        self.dos_lineEdit_1 = self.findChild(QLineEdit, 'dos_lineEdit_1')
        self.dos_lineEdit_2= self.findChild(QLineEdit, 'dos_lineEdit_2')
        self.dos_pushButton = self.findChild(QPushButton, 'dos_pushButton')
        self.dos_textBrowser = self.findChild(QTextBrowser, 'dos_textBrowser')
        self.dos_pushButton.clicked.connect(self.uidos)  

        self.ddos_comboBox = self.findChild(QComboBox, 'ddos_comboBox')
        self.ddos_lineEdit = self.findChild(QLineEdit, 'ddos_lineEdit')
        self.ddos_lineEdit_1 = self.findChild(QLineEdit, 'ddos_lineEdit_1')
        self.ddos_pushButton = self.findChild(QPushButton, 'ddos_pushButton')
        self.ddos_textBrowser = self.findChild(QTextBrowser, 'ddos_textBrowser')
        self.ddos_pushButton.clicked.connect(self.uiddos)  
        
        self.backdoor_lineEdit = self.findChild(QLineEdit, 'backdoor_lineEdit')
        self.backdoors_pushButton_1 = self.findChild(QPushButton, 'backdoor_pushButton_1')
        self.backdoor_pushButton_2 = self.findChild(QPushButton, 'backdoor_pushButton_2')
        self.backdoor_textBrowser = self.findChild(QTextBrowser, 'backdoor_textBrowser')
        self.backdoor_pushButton_1.clicked.connect(self.uibackdoor1) 
        self.backdoor_pushButton_2.clicked.connect(self.uibackdoor2) 

        self.xss_comboBox = self.findChild(QComboBox, 'xss_comboBox')
        self.xss_lineEdit_1 = self.findChild(QLineEdit, 'xss_lineEdit_1')
        self.xss_lineEdit_2 = self.findChild(QLineEdit, 'xss_lineEdit_2')
        self.xss_pushButton = self.findChild(QPushButton, 'xss_pushButton') 
        self.xss_textBrowser = self.findChild(QTextBrowser, 'xss_textBrowser') 
        self.xss_pushButton.clicked.connect(self.uixss)

        self.csrf_comboBox = self.findChild(QComboBox, 'csrf_comboBox')
        self.csrf_lineEdit_1 = self.findChild(QLineEdit, 'csrf_lineEdit')
        self.csrf_pushButton = self.findChild(QPushButton, 'csrf_pushButton') 
        self.csrf_textBrowser = self.findChild(QTextBrowser, 'csrf_textBrowser') 
        self.csrf_pushButton.clicked.connect(self.uicsrf)
        self.show()

    def uiportscan(self):
        portScanner.main(self, self.ps_comboBox.currentText() ,self.ps_lineEdit_1.text(),self.ps_lineEdit_2.text())
      
    def uiarpscan(self):
      def output4():
        ARPscan.main(self, self.arps_comboBox.currentText(), self.arps_lineEdit.text())
      t1 = threading.Thread(target=output4)
      t1.start()

    def uimitm(self):
      def output1():
          result = """[+]successfully performed Man in the middle \n now all packets of target are passing through this pc"""
          self.mitm_textBrowser.append(result)
          MITM.main(self, self.mitm_lineEdit_1.text(), self.mitm_lineEdit_2.text())
      t1 = threading.Thread(target=output1)
      t1.start()
             
    def uidos(self):
      def output5(): 
        output="Starting slowloris attack on"
        self.dos_textBrowser.append(output)
        Dos.main(self, self.dos_comboBox.currentText(), self.dos_lineEdit.text(),self.dos_lineEdit_1.text(),self.dos_lineEdit_2.text())
      t1 = threading.Thread(target=output5)
      t1.start()

    def uiddos(self):
      def output6(): 
        DDos.main(self, self.ddos_comboBox.currentText(), self.ddos_lineEdit.text(),self.ddos_lineEdit_1.text())
      t1 = threading.Thread(target=output6)
      t1.start()
      t1.join()
    
    def uibackdoor1(self):
        def output2():
          BackdoorServer.server(self)
        t1 = threading.Thread(target=output2)
        t1.start()
        t1.join()
      
    def uibackdoor2(self):
        def output3():
          BackdoorServer.main(self, self.backdoor_comboBox.currentText(), self.backdoor_lineEdit.text())
        t1 = threading.Thread(target=output3)
        t1.start()
        
    def uixss(self):
      def output6():
        xss.main(self,self.xss_comboBox.currentText() ,self.xss_lineEdit_1.text(),self.xss_lineEdit_2.text())
      t1 = threading.Thread(target=output6)
      t1.start()

    def uicsrf(self):
      def output7():
        csrf.main(self,self.csrf_lineEdit.text())
      t1 = threading.Thread(target=output7)
      t1.start()  
    
#http://testasp.vulnweb.com/
app = QApplication(sys.argv)

window = Ui()

app.exec_()
