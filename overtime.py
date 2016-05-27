# -*- coding:utf-8 -*-
import sys
import time
from PyQt4 import QtCore, QtGui, uic
import re
import codecs
import classDate
from web_ui import httpWidget
from PyQt4 import QtWebKit
from browser import Ui_HttpWidget
#import Ui_login
qtCreatorFile = "overtime.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#------------------------------------------------------登陆框-----------------------------------------------------------------------
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



class Ui_Dialog(object):
    '''
    登陆验证框，用户需输入工号即可在id.txt文件中找到对应的名字部门
    错误会提示“错误工号”
    '''
    def setupUi(self, Dialog):
        self.id=''
        self.depart=''
        self.name=''
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 120, 41, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.numberEdit = QtGui.QTextEdit(Dialog)
        self.numberEdit.setGeometry(QtCore.QRect(120, 110, 211, 31))
        self.numberEdit.setObjectName(_fromUtf8("numberEdit"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.login)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "工号:", None))
    
    def login(self):
        ids=[]
        names=[]
        departs=[]
        input=self.numberEdit.toPlainText()
        idfile=codecs.open('id.txt', 'r', 'utf-8')
        mess=idfile.read()
        pattern=re.compile(r'<id:(.*?)name:(.*?)depart:(.*?)>', re.S)
        mess=re.findall(pattern, mess)
        for i in mess:
            ids.append(i[0])
            names.append(i[1])
            departs.append(i[2])
        if  input in ids:
            self.id=input
            self.name=names[ids.index(input)]
            self.depart=departs[ids.index(input)]
            Dialog.accept()
        else:
            QtGui.QMessageBox.critical( Dialog, u'错误', u'错误工号')
    def getMess(self):
        return self.id, self.name, self.depart
        
        
#主程序___________________________________________________________________________________________________________
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.on=0
        self.timeobj=classDate.date()   #时间类的实例化 
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.startButton.clicked.connect(self.startCount)
        self.deleteButton.clicked.connect(self.deleteLast)
        self.readButton.clicked.connect(self.readCount)
        self.xlsButton.clicked.connect(self.makeXls)
        self.changeButton.clicked.connect(self.changeFun)

    def startCount(self):     #按下start时调用的函数
        #查看选项,奋斗者，加班，调休，午休时间
        fighter, money, rest, wuxiu=0, 0, 0, 0
        if  self.fighterButton.isChecked():
            fighter=1
        if self.moneyButton.isChecked():
            money=1
        if self.restButton.isChecked():
            rest=1
        if self.wuxiuBox.isChecked():
            wuxiu=1
        week={u'星期一':0, u'星期二':1, u'星期三':2,u'星期四':3,u'星期五':4,u'星期六':5,u'星期日':6}
        thedate=self.calendarWidget.selectedDate()
        thedatestring= (thedate.toString("yyyy-MM-dd dddd"))
        print (thedatestring[0:4], thedatestring[5:7],thedatestring[8:10], week[thedatestring[11:15]])
        self.timeobj.getTime(thedatestring[0:4],thedatestring[5:7],  thedatestring[8:10], week[thedatestring[11:15]])
        startHour=self.s_hourboBox.currentText()
        startMin=self.s_minboBox.currentText()
        endHour=self.e_hourboBox.currentText()
        endMin=self.e_minboBox.currentText()
        #转换成标准时间
        if int(startHour)*60+int(startMin) < int(endHour)*60+int(endMin):
            startTime=str(startHour)+':'+str(startMin)
            self.timeobj.setStartTime(startHour, startMin, startTime)
            endTime=str(endHour)+':'+str(endMin)
            self.timeobj.setEndTime(endHour, endMin, endTime)
            #在显示中显示出来
            #将备注写入 将选项例如是否是奋斗者写进去并得到时间差
            regularTime=self.timeobj.countTime( (self.remarkEdit.toPlainText()), rest, money, fighter, wuxiu) 
            self.output.setText(u'开始时间:'+startTime+'\n'+u'结束时间:'+endTime+'\n'+u'加班时间：'+regularTime)
            self.readFun(0)
        else:
            QtGui.QMessageBox.critical(self,"Error",  u'输入错误，结束时间必须大于开始时间')

        return

    
    def deleteLast(self):
       #按下delete时调用的函数
       #提取日历的时间
        button = QtGui.QMessageBox.question(self, "Question","确认删除上一条?",
                                     QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                                     QtGui.QMessageBox.Ok)
        if button==QtGui.QMessageBox.Ok:
            week = {u'星期一': 0, u'星期二': 1, u'星期三': 2, u'星期四': 3, u'星期五': 4, u'星期六': 5, u'星期日': 6}
            thedate = self.calendarWidget.selectedDate()
            thedatestring = (thedate.toString("yyyy-MM-dd dddd"))
            self.timeobj.getTime(thedatestring[0:4], thedatestring[5:7], thedatestring[8:10], week[thedatestring[11:15]])
        #调用类的删除函数,并得到被删的文字
            deleteText=self.timeobj.deleteLastLine()
        #使用正则来找到时间人物并显示出来
            if deleteText == 'nodate':
                self.output.setText(u'没有数据可删了')
                return
            pattern=re.compile('<.*?date:(.*?)start:(.*?)end:(.*?)time:.*?name:(.*?)depart:.*?>')
            items=re.findall(pattern,deleteText)
            # print(items[0])
            showText=u'删除记录\n<姓名：'+str(items[0][3])+','+u'日期：'+str(items[0][0])+','+u'时间：'+str(items[0][1])+'--'+str(items[0][2])+'>'
            self.output.setText(showText)
            self.readFun(0)
        return

    #读取数据
    def readCount(self):
        if self.detialBox.isChecked():detial=1;
        else:detial = 0
        a=self.readFun(detial)
        self.output.setText(a)
        return
    def readFun(self,detial):
        week = {u'星期一': 0, u'星期二': 1, u'星期三': 2, u'星期四': 3, u'星期五': 4, u'星期六': 5, u'星期日': 6}
        thedate = self.calendarWidget.selectedDate()
        thedatestring = (thedate.toString("yyyy-MM-dd dddd"))
        self.timeobj.getTime(thedatestring[0:4], thedatestring[5:7], thedatestring[8:10],
                                 week[thedatestring[11:15]])
        timeNow = time.localtime(time.time())
        yearNow = timeNow[0]  # 用来判断当前季度
        monthNow = timeNow[1]
        a, tups = self.timeobj.readHistory(detial, yearNow, monthNow)
        row = 0
        if 0 == detial:
            for tup in tups:
                col = 0
                for item in tup:
                    anitem = QtGui.QTableWidgetItem(item)
                    self.table.setItem(row, col, anitem)
                    col += 1
                row += 1
            for i in range(row, 32):
                for col in range(0, 5):
                    anitem = QtGui.QTableWidgetItem(' ')
                    self.table.setItem(row, col, anitem)
            return a
        return ''
        
    def makeXls(self):
        '''
        做表格函数,调用时间类的导出exl方法
        '''
        thedate = self.calendarWidget.selectedDate()
        thedatestring = (thedate.toString("yyyy-MM-dd dddd"))
        openfilName=thedatestring[0:4]+'_'+thedatestring[5:7]+'.txt'
        fileName = QtGui.QFileDialog.getSaveFileName(self,  ("Save File"),thedatestring[0:4]+'_'+thedatestring[5:7]+".xls",("*.xls"));
        if fileName:
            if self.timeobj.makeExcel(fileName, openfilName): QtGui.QMessageBox.critical(self,"Error",  u'数据不存在，无法导出')  
        return
    def writeMess(self, id, name, depart):
        '''
        三个变量分别来自登陆框匹配id.txt,将登陆的id和姓名写进去 ，为后期写入文件做准备
        '''
        self.timeobj.writeId( (id))
        self.timeobj.writeName( (name))
        self.timeobj.writeDepart( (depart))
        return

    def changeFun(self):
        webapp = httpWidget()
        webapp.show()
        webapp.exec_()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    if Dialog.exec_():
        id, name, depart=ui.getMess()
        window = MyApp()
        window.show()
        window.writeMess(id, name, depart)
        sys.exit(app.exec_())  
        setupUi(self)
