## -*- coding:utf-8 -*-
import sys
import time
import re
import codecs
import output_xls
import os
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg
# from tkinter import *

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
#计算本季度奋斗者加班时间
def readSeason(y, m, term):
    fightTime,moneyTime,restTime=0,0,0
    while term:
        if m<10:filename=str(y)+'_'+'0'+str(m)+'.txt'
        else:filename=str(y)+'_'+str(m)+'.txt'
        if os.path.isfile(filename):
            file=open(filename, 'r')
            text=file.read()
            pattern=re.compile('<wday.*?money:(.*?)food:.*?rest:(.*?)fighter:(.*?)remark:.*?>', re.S)
            time=re.findall(pattern, text)#找出当   fighter 还找寻奋斗者时间
            #把这个月的奋斗者时间累计
            for i in time:
                moneyTime+=float(i[0])
                restTime+=float(i[1])
                fightTime+=float(i[2])
            file.close()
        term-=1
        m=1
        
        # print (fightTime)
    return moneyTime,restTime,fightTime
    
class date:
    def __init__(self):
        self.year=2016
        self.month=3
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
        self.id=''
        self.name=''
        self.depart=''
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
        # print (self.startTime)

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
        pattern=re.compile('<wday:[5:6].*?time:(.*?)money:.*?>')
        time=re.findall(pattern,text )
        # print (time)
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
    def getTimeOfMonth(self,y,m):
        if m < 10:
            filename = str(y) + '_' + '0' + str(m) + '.txt'
        else:
            filename = str(y) + '_' + str(m) + '.txt'
        if os.path.isfile(filename):
            file = open(filename, 'r')
            text = file.read()
            pattern = re.compile('<wday.*?date:(.*?)start:.*?time:(.*?)money:.*?>', re.S)#找到本月日期对应的加班时间
            time = re.findall(pattern, text)  # 找出当
            # 显示
            day=[]
            t=[]
            for i in time:
                x=int(i[0][8:10])
                if x in day:
                    j=day.index(x)
                    t[j]+=float(i[1])#i【1】是时间
                else:
                    day.append(int(i[0][8:10]))
                    t.append(float(i[1]))
            nvs = zip(day, t)
            timeDict = dict((name, value) for name, value in nvs)
            # print(timeDict)
            day.sort()
            t1=[]
            # print(day)
            #对其进行排序
            for i in day:
                t1.append(timeDict[i])
            return day,t1
        #显示图表
    def show(self,x,y,seasonTime):
        # print('sss')
        mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
        ax1 = plt.subplot(211)  # 在图表中创建子图1
        ax2 = plt.subplot(212)  # 在图表中创建子图2
        plt.sca(ax1)
        plt.plot(x,y,'r--')
        j=0
        for i in x:
            plt.text(i,y[j],str(y[j]))
            j+=1
        plt.ylabel(u'时间\小时')
        plt.xlabel(u'日期')
        plt.title(u'本月加班时图形化显示',size=14)
        plt.sca(ax2)
        plt.title(u'  季度加班时饼图',size=14,loc='left')
        plt.pie(seasonTime, labels=(u'加班换钱', u'周末调休', u'奋斗者'))
        # plt.savefig('hahah.png')
        plt.show()
        return
    def readHistory(self, detial, yearNow, monthNow):
        a=''
        tup8=()
      #     print items
        record=open(str(self.year)+'_'+str(self.month)+'.txt','r',)
        text=record.read()
        record.close()
        if detial:
            day,t=self.getTimeOfMonth(yearNow,monthNow)
            if monthNow <= 3:
                SeasonTime = readSeason(yearNow, monthNow)
            elif monthNow <= 6:
                SeasonTime = readSeason(yearNow, monthNow, monthNow - 3)
            elif monthNow <= 9:
                SeasonTime = readSeason(yearNow, monthNow, monthNow - 6)
            else:
                SeasonTime = readSeason(yearNow, monthNow, monthNow - 9)
            # print('hhh')
            self.show(day,t,list(SeasonTime))
        else:
            if text:
                pattern=re.compile('<wday.*?date:'+str(self.year)+'-'+str(self.month)+'-'+str(self.day)+'.*?time:(.*?)money.*?fighter:(.*?)remark:.*?>', re.S)
                time=re.findall(pattern, text)#找出当   天加班时间 返回l一个列表   todayTime, sumTime,fighter 还找寻奋斗者时间
                #求出今天加班时，求出奋斗者加班时
                todayTime, fighterTime=0, 0
                for i in time:
                    todayTime+=float(i[0])
                    fighterTime+=float(i[1])
                if monthNow<=3:
                    fighttimeOfSeason=readSeason(yearNow, monthNow)[2]
                elif monthNow<=6:
                    fighttimeOfSeason=readSeason(yearNow, monthNow, monthNow-3)[2]
                elif monthNow<=9:
                    fighttimeOfSeason=readSeason(yearNow, monthNow, monthNow-6)[2]
                else:
                    fighttimeOfSeason=readSeason(yearNow, monthNow, monthNow-9)[2]

                self.getWeekendTime()
                self.getWorkdayTime()
                self.getSumTime()
                a=str(self.month)+u'月加班:'+str(self.sumTime)+u'小时\n'+u'今天加班：'+str(todayTime)+u'小时\n'+u'至今为止，奋斗者加班时为'+str(fighterTime)+u'小时\n'+u'本季度奋斗者加班时为'+str(fighttimeOfSeason)+u'小时\n'+u'周末加班时：'+str(self.weekendTime)+u'小时\n'+u'工作日加班时：'+str(self.workdayTime)+u'小时'
      #          print('ok')
                #   if detial:
            #      a=str(self.month)+u'月加班:'+str(self.sumTime)+u'小时\n'+u'今天加班：'+str(todayTime)+u'小时\n'+u'本月奋斗者加班时为'+str(fighterTime)+u'小时\n'+u'本月奋斗者加班时为'+str(fighttimeOfSeason)+u'小时\n'+u'周末加班时：'+str(self.weekendTime)+u'小时'+u'工作日加班时：'+str(self.workdayTime)+u'小时'
            #   else :
#           self.output.setText(a)
                # 找出姓名、日期、时间、开始、结束
                pattern = re.compile('<wday.*?date:(.*?)start:(.*?)end:(.*?)time:(.*?)money.*?remark:.*?name:(.*?)depart:.*?>', re.S)
                tup=re.findall(pattern,text)
                tup.reverse()
                if len(tup)>=31:tup8=tup[0:32]
                else:tup8=tup
            else:
               a='no data'
               tup8=()
        return a,tup8
    def countTime(self, remark, rest, money, fighter, wuxiu):
        #判断是否包含午休时间
        if wuxiu:
            overTime=(self.endSecond-self.startSecond)/3600.0 - 1
        else:
            overTime=(self.endSecond-self.startSecond)/3600.0
#        regularTime=sec2time(overTime)
        record=open(str(self.year)+'_'+str(self.month)+'.txt','a+')
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
            record.write('<wday:'+str(self.wday)+'date:'+str(self.year)+'-'+str(self.month)+'-'+str(self.day)+'start:'+self.startTime+'end:'+self.endTime+'time:'+str(overTime)+'money:0'+'food:'+str(food)+'rest:0'+'fighter:'+str(overTime)+'remark:'+remark+'id:'+self.id+'name:'+ (self.name)+'depart:'+ (self.depart)+'>')    #以@开头 &中断 ￥结尾之后用正则来匹配 
        elif rest:
            record.write('<wday:'+str(self.wday)+'date:'+str(self.year)+'-'+str(self.month)+'-'+str(self.day)+'start:'+self.startTime+'end:'+self.endTime+'time:'+str(overTime)+'money:0'+'food:'+str(food)+'rest:'+str(overTime)+'fighter:0'+'remark:'+remark+'id:'+self.id+'name:'+ (self.name)+'depart:'+ (self.depart)+'>')    #以@开头 &中断 ￥结尾之后用正则来匹配 
        elif money:
            record.write('<wday:'+str(self.wday)+'date:'+str(self.year)+'-'+str(self.month)+'-'+str(self.day)+'start:'+self.startTime+'end:'+self.endTime+'time:'+str(overTime)+'money:'+str(overTime)+'food:'+str(food)+'rest:0'+'fighter:0'+'remark:'+remark+'id:'+self.id+'name:'+ (self.name)+'depart:'+ (self.depart)+'>')    #以@开头 &中断 ￥结尾之后用正则来匹配 

      #  print 'succeed'
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
        id=[]
        name=[]
        depart=[]
        if os.path.isfile(openfilName):  #在目录下find记录文件
            record=open(openfilName,'r')
            text=record.read() 
            pattern=re.compile(r'<wday:(\d)date:(.*?)start:(.*?)end:(.*?)time:(.*?)money:(.*?)food:(.*?)rest:(.*?)fighter:(.*?)remark:(.*?)id:(.*?)name:(.*?)depart:(.*?)>',re.S)
            items=re.findall(pattern, text)
            # print(items)
            l=len(items)  #有多少条记录
        #接下来存week\date\time\remark,进行排序
            for i in range(0, l):
                date.append(items[i][1])
                # week.append(items[i][0])
                # start.append(items[i][2])
                # end.append(items[i][3])
                # time.append(items[i][4])
                # money.append(items[i][5])
                # food.append(items[i][6])
                # rest.append(items[i][7])
                # fighter.append(items[i][8])
                # remark.append(items[i][9])
                # id.append(items[i][10])
                # name.append(items[i][11])
                # depart.append(items[i][12])
     #       print name
        #写文件名
            nvs = zip(date, items)
            tict = dict((name, value) for name, value in nvs)
            # print(tict)
            date.sort()
            sortItems=[]
            # print(date)
            for i in date:
                sortItems.append(tict[i])
            # print(sortItems)
            for i in range(0, l):
                week.append(items[i][0])
                start.append(items[i][2])
                end.append(items[i][3])
                time.append(items[i][4])
                money.append(items[i][5])
                food.append(items[i][6])
                rest.append(items[i][7])
                fighter.append(items[i][8])
                remark.append(items[i][9])
                id.append(items[i][10])
                name.append(items[i][11])
                depart.append(items[i][12])
#            name=fileName
            output_xls.write_excel(fileName, week, date,start, end,  time, money, food, rest, fighter, remark, id, name, depart)
            return
        else: 
            return 1    #找不到文件
       
    def writeId(self, id):
        self.id=id
      #  print id
        return
    def writeName(self, name):
        self.name=name
       # print name
        return
    def writeDepart(self, depart):
        self.depart=depart
       # print depart
        return
    #删除最后一行的函数
    def deleteLastLine(self):
        #首先打开文件
        record=open(str(self.year)+'_'+str(self.month)+'.txt','r',)
        text=record.read()
        record.close()
        #正则匹配所有《》的文本，选择最后一行
        pattern=re.compile(r'<(.*?)>',re.S)
        content=re.findall(pattern,text)
        #替换
        pattern = re.compile('<'+content[-1]+'>', re.S)
        # print(content[-1])
        text=re.sub(pattern,'',text)
        # print(text)
        #重写入
        record = open(str(self.year) + '_' + str(self.month) + '.txt', 'w+')
        record.write(text)
        record.close()
        return '<'+content[-1]+'>'  #返回被删的文字