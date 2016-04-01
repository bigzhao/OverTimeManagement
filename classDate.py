## -*- coding:utf-8 -*-
import sys
import time
import re
import codecs
import output_xls
import os

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
        self.month=03
        self.day=1
        self.wday=0
        self.startTime=''
        self.startSecond=0
        self.endTime=''
        self.endSecond=0
        self.sumTime=0
#        self.getTime()
        self.weekendTime=0
        self.workdayTime=0
    def getTime(self, year, month, day, wday):
       # localtime=time.localtime(time.time())
        self.year=year
        self.month=month
        self.day=day
        self.wday=wday
#        if  self.day==1:
#            timeOfMonth=0
        return
    def setStartTime(self, startHour, startMin,starttime):
        self.startTime=starttime
#        start=time.asctime( time.localtime(starttime) ).split()#提取开始标准时间
        s_hour=int(startHour)
        s_min=int(startMin)
    #    self.startTime=str(s_hour)+':'+str(s_min)
        self.startSecond=3600*s_hour+60*s_min
        print self.startTime

        return
    def setEndTime(self,  endHour, endMin, endtime):
        self.endTime=endtime
        e_hour=int(endHour)
        e_min=int(endMin)
#        if e_min<30:min=30
#        elif e_min>30:
#            e_min=0
#            e_hour+=1
#        self.endTime=str(e_hour)+':'+str(e_min)
        self.endSecond=3600*e_hour+60*e_min
        return
    def getWeekendTime(self):
        weekendtime=0
        record=open(str(self.year)+'_'+str(self.month)+'.txt','r')
        text=str(record.read())
        pattern=re.compile('<wday:6|7.*?time:(.*?)money:.*?>')
        time=re.findall(pattern,text )
        for i in time:
            weekendtime+=float(i)
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
            pattern=re.compile('<wday:.*?time:(.*?)money:.*?>', re.S)
            items=re.findall(pattern,text)
            sumTime=0
            for i in items:
               sumTime+=float(i)
            self.sumTime=sumTime
            record.close
            return
    def readHistory(self, detial):
        
      #     print items
        record=open(str(self.year)+'_'+str(self.month)+'.txt','r')
        text=record.read()
        if text:
            pattern=re.compile('<wday.*?date:'+str(self.year)+'-'+str(self.month)+'-'+str(self.day)+'.*?time:(.*?)money.*?fighter:(.*?)remark:.*?>', re.S) 
            time=re.findall(pattern, text)#找出当   天加班时间 返回l一个列表   todayTime, sumTime,fighter 还找寻奋斗者时间
            #求出今天加班时，求出奋斗者加班时
            todayTime, fighterTime=0, 0
            for i in time:
                 todayTime+=float(i[0])
                 fighterTime+=float(i[1])
            
            
            self.getWeekendTime()
            self.getWorkdayTime()
            record.close()
            self.getSumTime()
            if detial:
                a=str(self.month)+u'月加班:'+str(self.sumTime)+u'小时\n'+u'今天加班：'+str(todayTime)+u'小时\n'+u'至今为止，奋斗者加班时为'+str(fighterTime)+u'小时'+u'周末加班时：'+str(self.weekendTime)+u'小时'+u'工作日加班时：'+str(self.workdayTime)+u'小时'
            else :
                a=str(self.month)+u'月加班:'+str(self.sumTime)+u'小时'+u'今天加班：'+str(todayTime)+u'小时\n'+u'至今为止，奋斗者加班时为'+str(fighterTime)+u'小时'
#           self.output.setText(a)
           
        else:
           a='no data'
        return     a    
    def countTime(self, remark, rest, money, fighter, wuxiu):
        #判断是否包含午休时间
        if wuxiu:
            overTime=(self.endSecond-self.startSecond)/3600.0 - 1
        else:
            overTime=(self.endSecond-self.startSecond)/3600.0
#        regularTime=sec2time(overTime)
        record=codecs.open(str(self.year)+'_'+str(self.month)+'.txt','a+', 'utf-8')
#        start=time.asctime( time.localtime(self.startTime) ).split()#提取开始标准时间
#        end=time.asctime( time.localtime(self.endTime) ).split()#提取结束标准时间
#
#        e_hour=int(end[3][0:2])
#        e.min=int(end[3][3:5])
#        if e_min<30:min=30
#        elif e_min>30:
#            e_min=0
#            e_hour+=1
       # record.write('<wday:'+str(self.wday)+'date:'+str(self.year)+'-'+str(self.month)+'-'+str(self.day)+'detial:'+start[3]+'--'+end[3]+'time:'+str(overTime)+'remark:'+remark+'>')    #以@开头 &中断 ￥结尾之后用正则来匹配 
       #判断是否双休加班，和是否。。。。。
        if self.wday<=4 and overTime>=3.0:food=20
        else : food=0
        if fighter:
            record.write('<wday:'+str(self.wday)+'date:'+str(self.year)+'-'+str(self.month)+'-'+str(self.day)+'start:'+self.startTime+'end:'+self.endTime+'time:'+str(overTime)+'money:0'+'food:'+str(food)+'rest:0'+'fighter:'+str(overTime)+'remark:'+remark+'>')    #以@开头 &中断 ￥结尾之后用正则来匹配 
        elif rest:
            record.write('<wday:'+str(self.wday)+'date:'+str(self.year)+'-'+str(self.month)+'-'+str(self.day)+'start:'+self.startTime+'end:'+self.endTime+'time:'+str(overTime)+'money:0'+'food:'+str(food)+'rest:'+str(overTime)+'fighter:0'+'remark:'+remark+'>')    #以@开头 &中断 ￥结尾之后用正则来匹配 
        elif money:
            record.write('<wday:'+str(self.wday)+'date:'+str(self.year)+'-'+str(self.month)+'-'+str(self.day)+'start:'+self.startTime+'end:'+self.endTime+'time:'+str(overTime)+'money:'+str(overTime)+'food:'+str(food)+'rest:0'+'fighter:0'+'remark:'+remark+'>')    #以@开头 &中断 ￥结尾之后用正则来匹配 

        print 'succeed'
        record.close()
        return str(overTime)
    def makeExcel(self, fileName, openfilName):
        #初始化数组 week是星期几 date是日期 startend是开始结束时间 time是加班时间 money是选择周末拿钱 rest是周末调休 fighter是奋斗者 remark是加班事宜
        week=[]
        date=[]
        start=[]
        end=[]
        time=[]
        food=[]
        money=[]
        rest=[]
        fighter=[]
        remark=[]
        if os.path.isfile(openfilName):  #在目录下find记录文件
            record=open(openfilName,'r')
            text=record.read() 
            pattern=re.compile(r'<wday:(\d)date:(.*?)start:(.*?)end:(.*?)time:(.*?)money:(.*?)food:(.*?)rest:(.*?)fighter:(.*?)remark:(.*?)>',re.S)
            items=re.findall(pattern, text)
            l=len(items)  #有多少条记录
        #接下来存week\date\time\remark
            for i in range(0, l):
                week.append(items[i][0])
                date.append(items[i][1])
                start.append(items[i][2])
                end.append(items[i][3])
                time.append(items[i][4])
                money.append(items[i][5])
                food.append(items[i][6])
                rest.append(items[i][7])
                fighter.append(items[i][8])
                remark.append(items[i][9])
        #写文件名
#        name=str(self.year)+'_'+str(self.month)
            name=fileName
            output_xls.write_excel(name, week, date,start, end,  time, money, food, rest, fighter, remark)
            return
        else: 
            return 1    #找不到文件
        
