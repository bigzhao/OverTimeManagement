# # -*- coding: utf-8 -*-
#
# # Form implementation generated from reading ui file 'web.ui'
# #
# # Created: Sat Apr 23 21:34:29 2016
# #      by: PyQt4 UI code generator 4.10.2
# #
# # WARNING! All changes made in this file will be lost!
#                                              --bigZhao


import sys
import time
import re
import codecs
from PyQt4 import QtCore, QtGui
from browser import Ui_HttpWidget
from PyQt4.QtCore import *
from PyQt4.QtGui import *
class httpWidget(QtGui.QWidget):
    '''
	主体功能是实现自动化登陆邮箱功能
	利用js语句实现
	frm=document.forms[0];frm.username.value='"+mess[0]+"';frm.userTypePwd.value='"+mess[1]+"';frm.wmSubBtn.click();
	'''
    def __init__(self, parent=None):
        super(httpWidget, self).__init__(parent)
        self.ui = Ui_HttpWidget()
        self.ui.setupUi(self)
        self.logged = False
        L = self.layout()
        L.setMargin(0)
        self.ui.horizontalLayout.setMargin(5)
        self.page=self.ui.webView.page()
        self.frame = self.page.mainFrame()
        url = 'http://mail.szangell.com/#lang=cn'
        self.ui.url.setText(url)

        self.ui.webView.setUrl(QtCore.QUrl(url))
        self.ui.back.setEnabled(False)
        self.ui.next.setEnabled(False)
        QtCore.QObject.connect(self.ui.back, QtCore.SIGNAL("clicked()"),\
                        self.back)
        QtCore.QObject.connect(self.ui.next, QtCore.SIGNAL("clicked()"),\
                        self.next)
        QtCore.QObject.connect(self.ui.url, QtCore.SIGNAL("returnPressed()"),\
                        self.url_changed)
        QtCore.QObject.connect(self.ui.webView, QtCore.SIGNAL("linkClicked(const QUrl&)"),\
                        self.link_clicked)
        QtCore.QObject.connect(self.ui.webView, QtCore.SIGNAL("urlChanged(const QUrl&)"),\
                        self.link_clicked)
        QtCore.QObject.connect(self.ui.webView, QtCore.SIGNAL("loadProgress(int)"),\
                        self.load_progress)
        QtCore.QObject.connect(self.ui.webView, QtCore.SIGNAL("titleChanged(const QString&)"),\
                        self.title_changed)
        QtCore.QObject.connect(self.ui.reload, QtCore.SIGNAL("clicked()"),\
                        self.reload_page)
        QtCore.QObject.connect(self.ui.stop, QtCore.SIGNAL("clicked()"),\
                        self.stop_page)
        QtCore.QMetaObject.connectSlotsByName(self)
        QtCore.QObject.connect(self.frame, QtCore.SIGNAL('loadFinished(bool)'), self.do_do)


    def do_do(self, bool):
        url = self.frame.url()
        print(url.toString())
        if url.toString() == "http://mail.szangell.com/#lang=cn":
            if self.logged == False:
                self.do_login()
                self.logged = True
    def url_changed(self):
        page = self.ui.webView.page()
        history = page.history()
        if history.canGoBack():
            self.ui.back.setEnabled(True)
        else:
            self.ui.back.setEnabled(False)

        if history.canGoForward():
            self.ui.next.setEnabled(True)
        else:
            self.ui.next.setEnabled(False)

        url = self.ui.url.text()
        self.ui.webView.setUrl(QtCore.QUrl(url))
    def do_login(self):
        try:
            idfile=codecs.open('mess.txt', 'r', 'utf-8')
            text=idfile.read()
            pattern=re.compile(r'<name:(.*?)pass:(.*?)>', re.S)
            mess=re.findall(pattern, text)[0]
        except:
            mess=''
        js="frm=document.forms[0];frm.username.value='"+mess[0]+"';frm.userTypePwd.value='"+mess[1]+"';frm.wmSubBtn.click();"
        self.frame.evaluateJavaScript(js)

    def stop_page(self):
        self.ui.webView.stop()

    def title_changed(self, title):
        self.setWindowTitle(title)

    def reload_page(self):
        self.ui.webView.setUrl(QtCore.QUrl(self.ui.url.text()))

    def link_clicked(self, url):
        page = self.ui.webView.page()
        self.__setHistButtonState(page, self.ui.back, self.ui.next)

        self.ui.url.setText(url.toString())

    def load_progress(self, load):
        if load == 100:
            self.ui.stop.setEnabled(False)
        else:
            self.ui.stop.setEnabled(True)

    def back(self):
        page = self.ui.webView.page()
        self.__setHistButtonState(page, self.ui.back, None)
        history = page.history()
        history.back()

    def next(self):
        page = self.ui.webView.page()
        history = page.history()
        history.forward()

        self.__setHistButtonState(page, None, self.ui.next)

    def __setHistButtonState(self, page, back, next):
        history = page.history()

        if back is not None:
            if history.canGoBack():
                back.setEnabled(True)
            else:
                back.setEnabled(False)

        if next is not None:
            if history.canGoForward():
                next.setEnabled(True)
            else:
                next.setEnabled(False)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = httpWidget()
    myapp.show()
    sys.exit(app.exec_())

