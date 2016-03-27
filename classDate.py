## -*- coding:utf-8 -*-
import sys
import time
import re
import codecs
import output_xls

def sec2time(iItv):                     #转换将秒变成时分秒
    if type(iItv)==type(1):
        h=(iItv/3600)
        sUp_h=iItv-3600*h
        m=sUp_h/60
        sUp_m=sUp_h-60*m
        s=sUp_m
        return ":".join(map(str,(h,m,s)))
    else:
        return "[InModuleError]:itv2time(iItv) invalid argument type"

class date:
    def __init__(self):
        self.year=2016
        self.month=1
        self.day=1
        self.wday=0
        self.startTime=0
        self.endTime=0
        self.sumTime=0
        self.getTime()
        self.weekendTime=0
        self.workdayTime=0
    def getTime(self):
        localtime=time.localtime(time.time())
        self.year=localtime[0]
        self.month=localtime[1]
        self.day=localtime[2]
        self.wday=localtime[6]+1
        if  self.day==1:
            timeOfMonth=0
        return
    def setStartTime(self, starttime):
        self.startTime=starttime
        return
    def setEndTime(self, endtime):
        self.endTime=endtime
        return
    def getWeekendTime(self):
        weekendtime=0
        record=open(str(self.year)+'_'+str(self.month)+'.txt','r')
        text=str(record.read())
        pattern=re.compile('<wday:6|7.*?time:(.*?)remark:.*?>')
        time=re.findall(pattern,text )
        for i in time:
            weekendtime+=int(i)
        self.weekendTime=weekendtime
        return
    def getWorkdayTime(self):
        workdaytime=0
        self.getWeekendTime()
        self.getSumTime()
        self.workdayTime=self.sumTime-self.weekendTime
        return
    def getSumTime(self):
        record=open(str(self.year)+'_'+str(self.month)+'.txt','r')
        text=str(record.read())
        if text:
            pattern=re.compile('<wday:.*?time:(.*?)remark:.*?>', re.S)
            items=re.findall(pattern,text)
            sumTime=0
            for i in items:
               sumTime+=int(i)
            self.sumTime=sumTime
            record.close
            return
    def readHistory(self, detial):
      #     print items
        record=open(str(self.year)+'_'+str(self.month)+'.txt','r')
        text=record.read()
        if text:
            pattern=re.compile('<wday.*?date:'+str(self.year)+'-'+str(self.month)+'-'+str(self.day)+'.*?time:(.*?)remark.*?>', re.S) 
            time=re.findall(pattern, text)#找出当   天加班时间 返回l一个列表   todayTime, sumTime
            todayTime=0
            for i in time:
                 todayTime+=int(i)
            self.getWeekendTime()
            self.getWorkdayTime()
            record.close()
            self.getSumTime()
            if detial:
                a=str(self.month)+u'月加班时:'+str(self.sumTime)+u'秒'+u'今天加班时：'+str(todayTime)+u'秒\n'+u'周末加班时：'+str(self.weekendTime)+u'秒'+u'工作日加班时：'+str(self.workdayTime)+u'秒'
            else :
                a=str(self.month)+u'月加班时:'+str(self.sumTime)+u'秒'+u'今天加班时：'+str(todayTime)+u'秒\n'
#           self.output.setText(a)
           
        else:
           a='no data'
        return     a    
    def countTime(self, remark):
        overTime=int(self.endTime-self.startTime)+1
        regularTime='Time:'+sec2time(overTime)
#        self.output.setText(regularTime)
#        remark=unicode(self.remarkEdit.toPlainText())
#        print remark
        record=codecs.open(str(self.year)+'_'+str(self.month)+'.txt','a+', 'utf-8')
        start=time.asctime( time.localtime(self.startTime) ).split()#提取开始标准时间
        end=time.asctime( time.localtime(self.endTime) ).split()#提取结束标准时间
        record.write('<wday:'+str(self.wday)+'date:'+str(self.year)+'-'+str(self.month)+'-'+str(self.day)+'detial:'+start[3]+'--'+end[3]+'time:'+str(overTime)+'remark:'+remark+'>')    #以@开头 &中断 ￥结尾之后用正则来匹配 
        print 'succeed'
        record.close()
        return regularTime
    def makeExcel(self):
        #初始化数组
        week=[]
        date=[]
        detial=[]
        time=[]
        remark=[]
        record=open(str(self.year)+'_'+str(self.month)+'.txt','r')
        text=record.read() 
        pattern=re.compile(r'<wday:(\d)date:(.*?)detial:(.*?)time:(.*?)remark:(.*?)>',re.S)
        items=re.findall(pattern, text)
        l=len(items)  #有多少条记录
        #接下来存week\date\time\remark
        for i in range(0, l):
            week.append(items[i][0])
            date.append(items[i][1])
            detial.append(items[i][2])
            time.append(items[i][3])
            remark.append(items[i][4])
        #写文件名
        name=str(self.year)+'_'+str(self.month)
        output_xls.write_excel(name, week, date,detial,  time, remark)
        return
