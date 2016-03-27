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
        self.timeobj=classDate.date()   #时间类的实例化 
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
#        self.getTime()
        self.startButton.clicked.connect(self.startCount)
        self.stopButton.clicked.connect(self.stopCount)
        self.endButton.clicked.connect(self.endCount)
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
        startTime=time.time()
        self.timeobj.setStartTime(startTime)
        self.output.setText('starttime:'+str(time.asctime( time.localtime(startTime))+'\n' ))
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
    def endCount(self):              #按下end时调用的函数
        endTime=time.time()
        self.timeobj.setEndTime(endTime)
     #   self.output.setText('endtime:'+str(time.asctime( time.localtime(self.startTime)) ))
     
        regularTime=self.timeobj.countTime(unicode(self.remarkEdit.toPlainText()))  #将备注写入 并得到时间差
        self.output.setText(regularTime)
        return
    
    def stopCount(self):               #按下stop时调用的函数
        self.timeobj.setStartTime(0)
        self.timeobj.setEndTime(0)
        self.output.setText(' ')
        return
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
    def readCount(self):
        if self.detialBox.isChecked():detial=1;
        else:detial=0  
        print detial
        a=self.timeobj.readHistory(detial)
        self.output.setText(a)
        return
    def makeXls(self):
        self.timeobj.makeExcel()
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
