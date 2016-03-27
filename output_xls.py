## -*- coding:utf-8 -*-
import sys
import xlrd
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy

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

def write_excel(name, week, date,detial,  time, remark):
    f = xlwt.Workbook() #创建工作簿
    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) #创建sheet
    row = [u'星期',u'日期',u'时间段',u'加班时',u'加班费', u'备注']
    for i in range(0,len(row)):
        sheet1.write(0,i,row[i],set_style('Times New Roman',220,True)) 
    for i in range(0,  len(week)):
        sheet1.write(i+1,0,week[i],set_style('Times New Roman',220,True))
        sheet1.write(i+1,1,date[i],set_style('Times New Roman',220,True))
        sheet1.write(i+1, 2, detial[i], set_style('Times New Roman',220,True))
        sheet1.write(i+1,3,time[i],set_style('Times New Roman',220,True))
        sheet1.write(i+1,4,unicode(remark[i], 'utf-8'),set_style('Times New Roman',220,True))
    f.save(name+'.xlsx') #保存文件
    return

   
        
        
