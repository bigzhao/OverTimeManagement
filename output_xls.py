## -*- coding:utf-8 -*-
import os
import sys
import xlrd
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy
import shutil
def set_style(name,height,bold=False):
  style = xlwt.XFStyle() # 初始化样式

  font = xlwt.Font() # 为样式创建字体
  font.name = name # 'Times New Roman'
  font.bold = bold
  font.color_index = 4
  font.height = height

  # borders= xlwt.Borders()
  # borders.left= 6
  # borders.right= 6
  # borders.top= 6
  # borders.bottom= 6

  style.font = font
  # style.borders = borders

  return style

def write_excel(destPath, week, date, start, end, time, money, food, rest, fighter, remark, id, name, depart):
    '''
	写入生成excel函数，传入变量如下：
	{
	destPath : 文件保存目的地址
	week；星期几
	data: 日期
	start: 开始时间
	end: 结束时间
	time：加班时间
	money: 加班换钱
	food： 餐补
	rest：周末调休
	fighter: 奋斗者加班时间
	remark: 备注
	id: 工号
	name: 姓名
	depart: 部门
	}
	函数中定义变量如下：{
	totalTime, totalFee, totalFood, totalRest, totalFighter：对应传入变量的时间总和
	
	}
	'''
    totalTime, totalFee, totalFood, totalRest, totalFighter=0.0, 0.0, 0.0, 0.0, 0.0
    srcPath=(os.getcwd()+'\sample.xls')
    rb = open_workbook( srcPath, formatting_info=True)
    wb = copy(rb)
    ws = wb.get_sheet(0)    
    for i in range(0,  len(week)):
        ws.write(i+3,1,depart[i],set_style('Times New Roman',240,True))
        ws.write(i+3,2,id[i],set_style('Times New Roman',240,True))
        ws.write(i+3,3,name[i],set_style('Times New Roman',240,True))
        ws.write(i+3,4,date[i],set_style('Times New Roman',240,True))
        ws.write(i+3, 5, start[i], set_style('Times New Roman',240,True))
        ws.write(i+3, 6, end[i], set_style('Times New Roman',240,True))
        ws.write(i+3,7,time[i],set_style('Times New Roman',240,True))
        if int(week[i])>4:wk=u'是'
        else:wk=u'否'
        ws.write(i+3,8, wk,set_style('Times New Roman',240,True))
        ws.write(i+3,9,str(float(money[i])*25),set_style('Times New Roman',240,True))
        ws.write(i+3,10,food[i],set_style('Times New Roman',240,True))
        ws.write(i+3,11,rest[i],set_style('Times New Roman',240,True))
        ws.write(i+3,12,fighter[i],set_style('Times New Roman',240,True))
        ws.write(i+3,13,remark[i],set_style('Times New Roman',240,True))
        totalTime+=float(time[i])
        totalFee+=float(money[i])
        totalFood+=float(food[i])
        totalRest+=float(rest[i])
        totalFighter+=float(fighter[i])
        #写总和在22行

    ws.write(21, 7,totalTime, set_style('Times New Roman',240,True))
    ws.write(21, 9,totalFee*25, set_style('Times New Roman',240,True))
   
    ws.write(21, 10,totalFood, set_style('Times New Roman',240,True))
    ws.write(21, 11,totalRest, set_style('Times New Roman',240,True))
    ws.write(21, 12,totalFighter, set_style('Times New Roman',240,True))
    wb.save(destPath)
    
    return

   
        
        
