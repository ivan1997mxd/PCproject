from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
import sys

from PyQt5.QtWidgets import QApplication
from numpy import unicode


class Browser(QWebEngineView):
    def __init__(self):
        super(Browser, self).__init__()
        self.loadFinished.connect(self.print_load_finished)
        self.loadProgress.connect(self.print_percent)

    def print_percent(self, percent):
        print(percent)

    def print_load_finished(self):
        print('Load Finished')
        self.print_html()

    def print_html(self):
        frame = self.page()
        print(unicode(frame.toHtml(self.print_percent)).encode('utf-8'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    br = Browser()
    url = QUrl('http://python.org')
    br.load(url)
    br.show()
    app.exec_()
