from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QAction
from PyQt4.QtCore import SIGNAL
from src.RunTool import RunTool
from src.ToolConfig import ToolConfig
from UI.Main import Ui_MainWindow
from UI.Config import Ui_Form
import sys

class ZBMain(Ui_MainWindow):
	def __init__(self,dialog,parent=None):
		Ui_MainWindow.__init__(self)
		self.setupUi(dialog)
		self.tabWidget.clear()
		self.config=None
		print("[*] Setting up the UI ")
		self.toolkit={
			"zbid":self.zbid,
			"zbwireshark":self.zbwireshark,
			"zbdump":self.zbdump,
			"zbreplay":self.zbreplay,
			"zbstumbler":self.zbstumbler,
			"zbpanidconflictflood":self.zbpanidconflictflood,
			"zborphannotify":self.zborphannotify,
			"zbrealign":self.zbrealign,
			"zbfakebeacon":self.zbfakebeacon,
			"zbopenear":self.zbopenear,
			"zbassocflood":self.zbassocflood,
			"zbconvert":self.zbconvert,
			"zbdsniff":self.zbdsniff,
			"zbgoodfind":self.zbgoodfind,
			"zbwardrive":self.zbwardrive,
			"zbscapy":self.zbscapy
		}
                if(self.CheckTools()==1):
                        self.SetupTools()
                self.actionTools.triggered.connect(self.ConfigureTools)
		self.actionExit.triggered.connect(self.exit)
		self.pushButton_zbidRefresh.clicked.connect(self.zbidRefresh)


	def exit(self):
		self.close()

	def CheckTools(self):
		file=open("cfg/tools.cfg","r")
		out=file.read()
		file.close()
		if("+" in out):
			return 1
		else:
			return 0

	def ConfigureTools(self):
		if self.config is None:
			self.config=ToolConfig()
		self.config.show()
	        QtCore.QObject.connect(self.config,QtCore.SIGNAL("update_tools(int)"), self.SetupTools)


	def SetupTools(self):
		self.tabWidget.clear()
		file=open("cfg/tools.cfg","r")
		while(True):
			tab=file.readline().strip()
			if tab=="":
				break
			if '+' in tab:
				tab=tab.replace('+','')
				self.tabWidget.addTab(self.toolkit[tab],QtCore.QString(tab))
		file.close()

	def zbidRefresh(self):
		self.zbidThread=RunTool("zbid",None)
		self.zbidThread.start()
                QtCore.QObject.connect(self.zbidThread,QtCore.SIGNAL("update_zbid(QString)"), self.zbidOutput)

	def zbidOutput(self,QString):
		item = QtGui.QListWidgetItem(str(QString))
		self.listWidget_zbid.addItem(item)

if __name__=="__main__":
	app=QtGui.QApplication(sys.argv)
	dialog=QtGui.QMainWindow()
        app.setWindowIcon(QtGui.QIcon("UI/icon.png"))
	prog=ZBMain(dialog)
	dialog.show()
	sys.exit(app.exec_())
