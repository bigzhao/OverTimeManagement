## -*- coding:utf-8 -*-
import sys
import time
from PyQt4 import QtCore, QtGui, uic
import re
import codecs
import classDate
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
#        self.getTime()
        self.startButton.clicked.connect(self.startCount)
#        self.stopButton.clicked.connect(self.stopCount)
        self.deleteButton.clicked.connect(self.deleteLast)
        self.readButton.clicked.connect(self.readCount)
        self.xlsButton.clicked.connect(self.makeXls)
       
#    def getTime(self):
#        localtime=time.localtime(time.time())
#        self.year=localtime[0]
#        self.month=localtime[1]
#        self.day=localtime[2]
#        self.wday=localtime[6]+1
#        if  self.day==1:
#            timeOfMonth=0
#        return
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
       # print thedatestring[0:4], thedatestring[5:7],thedatestring[8:10], week[thedatestring[11:15]]
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
            regularTime=self.timeobj.countTime( (self.remarkEdit.toPlainText()), rest, money, fighter, wuxiu)  #将备注写入 将选项例如是否是奋斗者写进去并得到时间差
            self.output.setText(u'开始时间:'+startTime+'\n'+u'结束时间:'+endTime+'\n'+u'加班时间：'+regularTime)

        else:
            QtGui.QMessageBox.critical(self,"Error",  u'输入错误，结束时间必须大于开始时间')

        return

#    def getWeekendTime(self):
#        weekendtime=0
#        record=open(str(self.year)+'_'+str(self.month)+'.txt','r')
#        text=str(record.read())
#        pattern=re.compile('<wday:6|7.*?time:(.*?)remark:.*?>')
#        time=re.findall(pattern,text )
#        for i in time:
#            weekendtime+=int(i)
#        self.weedendTime=weekendtime
#        return
#    def getWorkdayTime(self):
#        workdaytime=0
#        self.getWeekendTIme()
#        self.getSumTime()
#        self.workTime=self.sumTime-self.weekendTime
#    def endCount(self):              #按下end时调用的函数
##        if self.on:
#        self.on=0         #判断用户是否按下start再按end
#   #     endTime=time.time()
#        endTime=self.endboBox.currentText()
#        self.timeobj.setEndTime(endTime)
#     #   self.output.setText('endtime:'+str(time.asctime( time.localtime(self.startTime)) ))
#     
#        regularTime=self.timeobj.countTime( (self.remarkEdit.toPlainText()))  #将备注写入 并得到时间差
#        self.output.setText(regularTime)
#            
#        else:
#           QtGui.QMessageBox.critical(self,"Error",  u'操作错误 请先点击start')  

#        return
    
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
            pattern=re.compile('<.*?date:(.*?)start:(.*?)end:(.*?)time:.*?name:(.*?)depart:.*?>')
            items=re.findall(pattern,deleteText)
            # print(items[0])
            showText=u'删除记录\n<姓名：'+str(items[0][3])+','+u'日期：'+str(items[0][0])+','+u'时间：'+str(items[0][1])+'--'+str(items[0][2])+'>'
            self.output.setText(showText)
        return
#    oo
#    def countTime(self):
#        overTime=int(self.endTime-self.startTime)
#        regularTime='Time:'+sec2time(overTime)
#        self.output.setText(regularTime)
#        remark= (self.remarkEdit.toPlainText())
#        print remark
#        record=codecs.open(str(self.year)+'_'+str(self.month)+'.txt','a+', 'utf-8')
#        record.write('<wday:'+str(self.wday)+'year:'+str(self.year)+'month:'+str(self.month)+'day:'+str(self.day)+'time:'+str(overTime)+'remark:'+remark+'>')    #以@开��jia讲断 ￥结尾之后用正则来匹配 
#        print 'succeed'
#        record.close() 
#       return
#读取数据
    def readCount(self):
        if self.detialBox.isChecked():detial=1;
        else:detial = 0
     #   print detial
        week ={u'星期一':0, u'星期二':1, u'星期三':2,u'星期四':3,u'星期五':4,u'星期六':5,u'星期日':6}
        thedate = self.calendarWidget.selectedDate()
        thedatestring = (thedate.toString("yyyy-MM-dd dddd"))
        self.timeobj.getTime(thedatestring[0:4],thedatestring[5:7],  thedatestring[8:10], week[thedatestring[11:15]])
        timeNow = time.localtime(time.time())
        yearNow = timeNow[0]     #用来判断当前季度
        monthNow = timeNow[1]
        # newItem = QtGui.QTableWidgetItem("松鼠")
        # self.table.setItem(0, 0, newItem)
        a,tups=self.timeobj.readHistory(detial,yearNow, monthNow )
        # print('ok')
        row = 0
        if 0 == detial:
            for tup in tups:
                col = 0
                for item in tup:
                    anitem = QtGui.QTableWidgetItem(item)
                    self.table.setItem(row, col, anitem)
                    col += 1
                row += 1
            for i in range(row,32):
                for col in range(0,5):
                    anitem = QtGui.QTableWidgetItem(' ')
                    self.table.setItem(row, col, anitem)

            self.output.setText(a)
        return
        #做表格函数
    def makeXls(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,  ("Save File"),"/home/tdz/untitled.xls",("*.xls"));
        xls_year=str(self.yearspinBox.value())
        xls_month=self.monthspinBox.value()
        if xls_month<10:xls_month='0'+str(xls_month)
        else:xls_month=str(xls_month)
        openfilName=xls_year+'_'+xls_month+'.txt'
   #     print openfilName
        
        if fileName:
            if self.timeobj.makeExcel(fileName, openfilName): QtGui.QMessageBox.critical(self,"Error",  u'数据不存在，无法导出')  
        return
        #将登陆的id和姓名写进去 ，为后期写入文件做准备  
    def writeMess(self, id, name, depart):
        self.timeobj.writeId( (id))
        self.timeobj.writeName( (name))
        self.timeobj.writeDepart( (depart))
        return
#        
#           pattern=re.compile('<wday.*?day:'+str(self.day)+'.*?time:(.*?)remark.*?>', re.S) 
#           time=re.findall(pattern, text)#找出当   天加班时间 返回l一个列表   todayTime, sumTime
#           todayTime=0
#           for i in time:
#                 todayTime+=int(i)
#           a=str(self.month)+u'月加班时:'+str(self.sumTime)+u'秒'+u'今天加班时：'+str(todayTime)+u'秒'
#           self.output.setText(a)
#           record.close()
#        else:
#           self.output.setText('no data')
#        return




if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
 #   Dialog.show()
    if Dialog.exec_():
    #    print ui.getMess()
        id, name, depart=ui.getMess()
        window = MyApp()
        window.show()
        window.writeMess(id, name, depart)
        sys.exit(app.exec_())  
        setupUi(self)
