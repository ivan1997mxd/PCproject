#coding=utf8
import sys

from blizzardui.pyqt.QtGui import (
    QApplication, QPixmap)

from blizzardui.widgets import Chatroom

# 常规的启动动作就不多加说明
app = QApplication(sys.argv)
# 两个 NickName 定义了来往的用户昵称
# headImage 应当为一个 46*46 的 QPixmap ，当然如果过大也会被自动截取
mainWindow = Chatroom(toNickName=u'好友 A', fromNickName='LittleCoder',
    headImage=QPixmap('src/chatroom/images/header/default_image.png'))
mainWindow.show()

# 当你输入一些内容并使用 Enter 时，将会调用该方法
def fn(msg):
    mainWindow.add_msg(msg)
    print(unicode(msg))
mainWindow.messageReceived.connect(fn)

# 通过 add_msg ，可以向历史记录中加入消息
# 如果 isSend 设为 False ，将会判定为是收到的消息
mainWindow.add_msg('yo' * 50)
mainWindow.add_msg('yo', isSend=False)
mainWindow.add_msg('yo')
# 通过 set_footer ，可以设置页尾的内容
mainWindow.set_footer(u'最后登录')

sys.exit(app.exec_())