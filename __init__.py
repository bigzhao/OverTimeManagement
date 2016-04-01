## -*- coding:utf-8 -*-
import sys
import time
from PyQt4 import QtCore, QtGui, uic
import re
import codecs
import classDate
qtCreatorFile = "overtime.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#def sec2time(iItv):                     #转换将秒变成时分秒
#
#    if type(iItv)==type(1):
#        h=(iItv/3600)
#        sUp_h=iItv-3600*h
#        m=sUp_h/60
#        sUp_m=sUp_h-60*m
#        s=sUp_m
#        return ":".join(map(str,(h,m,s)))
#    else:
#        return "[InModuleError]:itv2time(iItv) invalid argument type"
        
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
#        self.year=2016
#        self.month=1
#        self.day=1
#        self.wday=0
#        self.startTime=0
#        self.endTime=0
#        self.sumTime=0
       #self.todaytime=0
    #    classDate.sec2time(22)
        self.on=0
        self.timeobj=classDate.date()   #时间类的实例化 
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
#        self.getTime()
        self.startButton.clicked.connect(self.startCount)
#        self.stopButton.clicked.connect(self.stopCount)
#        self.endButton.clicked.connect(self.endCount)
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
#        self.on=1
   #     startTime=time.time()
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
        thedatestring=unicode(thedate.toString("yyyy-MM-dd dddd"))
        print thedatestring[0:4], thedatestring[5:7],thedatestring[8:10], week[thedatestring[11:15]]
        self.timeobj.getTime(thedatestring[0:4],thedatestring[5:7],  thedatestring[8:10], week[thedatestring[11:15]])
        startHour=self.s_hourboBox.currentText()
        startMin=self.s_minboBox.currentText()
        endHour=self.e_hourboBox.currentText()
        endMin=self.e_minboBox.currentText()
        #转换成标准时间
        startTime=str(startHour)+':'+str(startMin)
        self.timeobj.setStartTime(startHour, startMin, startTime)
        endTime=str(endHour)+':'+str(endMin)
        self.timeobj.setEndTime(endHour, endMin, endTime)
        #在显示中显示出来
           #     endTime=time.time()
#        endTime=self.endboBox.currentText()
        
     #   self.output.setText('endtime:'+str(time.asctime( time.localtime(self.startTime)) ))
        regularTime=self.timeobj.countTime(unicode(self.remarkEdit.toPlainText()), rest, money, fighter, wuxiu)  #将备注写入 将选项例如是否是奋斗者写进去并得到时间差
#        self.output.setText()
        self.output.setText(u'开始时间:'+startTime+'\n'+u'结束时间:'+endTime+'\n'+u'加班时间：'+regularTime)

#        else:
#            QtGui.QMessageBox.critical(self,"Error",  u'操作错误 请先点击start')  

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
#        regularTime=self.timeobj.countTime(unicode(self.remarkEdit.toPlainText()))  #将备注写入 并得到时间差
#        self.output.setText(regularTime)
#            
#        else:
#           QtGui.QMessageBox.critical(self,"Error",  u'操作错误 请先点击start')  

#        return
    
#    def stopCount(self):               #按下stop时调用的函数
#        self.timeobj.setStartTime(0)
#        self.timeobj.setEndTime(0)
#        self.output.setText(' ')
#        return
#    oo
#    def countTime(self):
#        overTime=int(self.endTime-self.startTime)
#        regularTime='Time:'+sec2time(overTime)
#        self.output.setText(regularTime)
#        remark=unicode(self.remarkEdit.toPlainText())
#        print remark
#        record=codecs.open(str(self.year)+'_'+str(self.month)+'.txt','a+', 'utf-8')
#        record.write('<wday:'+str(self.wday)+'year:'+str(self.year)+'month:'+str(self.month)+'day:'+str(self.day)+'time:'+str(overTime)+'remark:'+remark+'>')    #以@开��jia讲断 ￥结尾之后用正则来匹配 
#        print 'succeed'
#        record.close() 
#        return
#读取数据
    def readCount(self):
        if self.detialBox.isChecked():detial=1;
        else:detial=0  
        print detial
        week={u'星期一':0, u'星期二':1, u'星期三':2,u'星期四':3,u'星期五':4,u'星期六':5,u'星期日':6}
        thedate=self.calendarWidget.selectedDate()
        thedatestring=unicode(thedate.toString("yyyy-MM-dd dddd"))
#        print thedatestring[0:4], thedatestring[5:7],thedatestring[8:10], thedatestring[11:15]]
        self.timeobj.getTime(thedatestring[0:4],thedatestring[5:7],  thedatestring[8:10], week[thedatestring[11:15]])
        a=self.timeobj.readHistory(detial)
        self.output.setText(a)
        return
        #做表格函数
    def makeXls(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,  ("Save File"),"/home/tdz/untitled.xls",("*.xls"));
#        print unicode(fileName)
        xls_year=str(self.yearspinBox.value())
        xls_month=self.monthspinBox.value()
        if xls_month<10:xls_month='0'+str(xls_month)
        else:xls_month=str(xls_month)
        openfilName=xls_year+'_'+xls_month+'.txt'
        print openfilName
        
        if fileName:
            if self.timeobj.makeExcel(fileName, openfilName): QtGui.QMessageBox.critical(self,"Error",  u'数据不存在，无法导出')  
        return
#        
#      #     print items
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
    window = MyApp()
    window.show()
    sys.exit(app.exec_())  
    setupUi(self)
