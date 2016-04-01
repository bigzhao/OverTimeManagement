## -*- coding:utf-8 -*-
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

def write_excel(destPath, week, date,start,end,   time, money, food, rest, fighter, remark):
#    f = xlwt.Workbook() #创建工作簿
#    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
#    row = [u'星期',u'日期',u'时间段',u'开始',u'结束', u'备注']
#    for i in range(0,len(row)):
#        sheet1.write(0,i,row[i],set_style('Times New Roman',220,True)) 
#    for i in range(0,  len(week)):
#        sheet1.write(i+1,0,week[i],set_style('Times New Roman',220,True))
#        sheet1.write(i+1,1,date[i],set_style('Times New Roman',220,True))
#        sheet1.write(i+1, 2, start[i], set_style('Times New Roman',220,True))
#        sheet1.write(i+1, 2, end[i], set_style('Times New Roman',220,True))
#        sheet1.write(i+1,3,time[i],set_style('Times New Roman',220,True))
#        sheet1.write(i+1,4,unicode(remark[i], 'utf-8'),set_style('Times New Roman',220,True))
#    f.save(name) #保存文件
    srcPath='/home/tdz/workspace/sample.xls'
#    shutil.copy(srcPath, destPath)
    rb = open_workbook(unicode( srcPath, 'utf-8'), formatting_info=True)
#    print week, date,start,end,   time, money, food, rest, fighter, remark
    #通过sheet_by_index()获取的sheet没有write()方法
#    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    #通过get_sheet()获取的sheet有write()方法
    ws = wb.get_sheet(0)    
    for i in range(0,  len(week)):
        ws.write(i+3,4,date[i],set_style('Times New Roman',240,True))
        ws.write(i+3, 5, start[i], set_style('Times New Roman',240,True))
        ws.write(i+3, 6, end[i], set_style('Times New Roman',240,True))
        ws.write(i+3,7,time[i],set_style('Times New Roman',240,True))
        if int(week[i])>4:wk=u'是'
        else:wk=u'否'
        ws.write(i+3,8, wk,set_style('Times New Roman',240,True))
        ws.write(i+3,9,str(float(money[i])*25),set_style('Times New Roman',240,True))
        ws.write(i+3,10,food[i],set_style('Times New Roman',240,True))
        ws.write(i+3,11, rest[i],set_style('Times New Roman',240,True))
        ws.write(i+3,12,fighter[i],set_style('Times New Roman',240,True))
        ws.write(i+3,13,unicode(remark[i], 'utf-8'),set_style('Times New Roman',240,True))
    wb.save(destPath)
    return

   
        
        
