"""
Do Not Believe His Lies
A PyQt Implementation, by Meorge
"""

import sys
import time
import mplayer
import parseXML as dnbhl
import subprocess, threading
import urllib.request as pagegrab
from PyQt5 import QtWidgets, QtGui, QtCore,QtMultimediaWidgets, QtMultimedia, QtPrintSupport
Qt = QtCore.Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setStyleSheet("""
        QMainWindow {
        background-color: black;
        }
        """)
        self.makeUI()
        
    def makeUI(self):

        self.answerArea = QtWidgets.QLineEdit()
        self.answerArea.setPlaceholderText('Enter Code')
        self.answerArea.setAlignment(Qt.AlignHCenter)
        self.answerArea.setStyleSheet("""
        QLineEdit {
        background-color: black;
        color: white;
        border: 3px solid white;
        border-radius: 5px;
        font-family: 'Brandon Grotesque';
        height: 50px;
        font-size: 30px;
        }""")
        
        self.answerArea.returnPressed.connect(self.checkForPuzzle)
        
        self.puzzlenamelabel = QtWidgets.QLabel()
        self.puzzlenamelabel.setStyleSheet("""
            QLabel {
            color: white;
            font-family: 'Brandon Grotesque';
            font-size: 15px;
            }""")
        
        self.timerWidget = QtWidgets.QLabel('T: 0 : 0 : 0')
        self.timerWidget.setStyleSheet("""
                QLabel {
                color: white;
                font-family: 'Brandon Grotesque';
                font-size: 15px;
                }""")
        
        self.hintButton = QtWidgets.QPushButton('Hint')
        self.hintButton.clicked.connect(self.getAHint)
        self.hintButton.setStyleSheet("""
        QPushButton {
        background-color: black;
        color: white;
        font-family: 'Brandon Grotesque';
        border: 3px solid white;
        border-radius: 5px;
        width: 70px;
        height: 50px;
        font-size: 30px;
        }""")

        self.label = QtWidgets.QLabel('Do Not Believe His Lies')
        #self.label.mousePressEvent.connect(self.rightClickMenu)
        self.label.setStyleSheet("""
        QLabel {
        color: white;
        font-size: 30px;
        font-family: 'Brandon Grotesque';
        }
        """)
        
        self.loadingBar = QtWidgets.QProgressBar()
        self.loadingBar.setValue(24)
        self.loadingBar.setTextVisible(False)
        self.loadingBar.setStyleSheet("""
        QProgressBar {
        background-color: black;
        border: 3px solid white;
        border-radius: 5px;
        height: 50px;
        }
        QProgressBar::chunk {
        background-color: white;
        height: 50px;
        }""")
        
        
        self.headerStuff = QtWidgets.QWidget()
        self.hsl = QtWidgets.QHBoxLayout()
        #self.spacer = QtWidgets.QSpacerItem(QtWidgets.QSizePolicy.Expanding)
        
        
        self.timerWidget.setAlignment(Qt.AlignLeft)
        self.puzzlenamelabel.setAlignment(Qt.AlignRight)
        self.hsl.addWidget(self.timerWidget)
        #self.hsl.addWidget(self.spacer)
        self.hsl.addWidget(self.puzzlenamelabel)
        self.headerStuff.setLayout(self.hsl)
        
        
        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.answerArea, 3,0)
        self.layout.addWidget(self.loadingBar, 3,0)
        self.loadingBar.hide()
        self.layout.addWidget(self.hintButton, 3,1)
        
        self.messageStuff = QtWidgets.QWidget()
        self.messageStuffLayout = QtWidgets.QVBoxLayout()
        self.messageStuffLayout.addWidget(self.label, 1)
        #self.messageStuffLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.messageStuff.setLayout(self.messageStuffLayout)
        
        
        self.menubar = QtWidgets.QMenuBar()
        self.fileMenu = self.menubar.addMenu('&Tools')
        
        self.exportAction = QtWidgets.QAction('&Export Resource', self)
        self.exportAction.setShortcut(QtGui.QKeySequence.SaveAs)
        self.exportAction.setStatusTip('Save the current resource')
        self.exportAction.triggered.connect(self.exportResource)
        
        self.printAction = QtWidgets.QAction('&Print', self)
        self.printAction.setShortcut(QtGui.QKeySequence.Print)
        self.printAction.setStatusTip('Print the current image')
        self.printAction.triggered.connect(self.printPicture)
        
        self.fileMenu.addAction(self.exportAction)
        self.fileMenu.addAction(self.printAction)
        self.setMenuBar(self.menubar)
        
        self.layout.addWidget(self.messageStuff, 0,0)

        self.buttons = QtWidgets.QWidget()
        self.buttons.setLayout(self.layout)
        
        self.overallLayout = QtWidgets.QVBoxLayout()
        self.overallLayout.addWidget(self.headerStuff, 0)
        #self.overallLayout.addWidget(self.puzzlenamelabel, 0, Qt.AlignRight)
        self.overallLayout.addWidget(self.messageStuff, 1, Qt.AlignVCenter)
        #self.overallLayout.addWidget(self.videoPlayerWidget, 1, Qt.AlignVCenter)
        self.overallLayout.addWidget(self.buttons, 2, Qt.AlignBottom)
        self.messageStuffLayout.setAlignment(Qt.AlignHCenter)
        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setLayout(self.overallLayout)

        self.setCentralWidget(self.mainWidget)

        self.timerception = QtCore.QTimer()
        self.timerception.setSingleShot(False)
        self.timerception.timeout.connect(self.updateTimer)
        self.timerception.start(1000)
        
        self.setToPuzzle1()
    
    def checkForPuzzle(self):
        text = self.answerArea.text()
        textEdited = self.answerArea.text().replace(' ', '').upper()
        isvalid = dnbhl.getPuzzleInformation(textEdited)
        if isvalid == 'NotFoundError':
            self.answerArea.setText('')
        
            '''self.shakeAnim = QtCore.QPropertyAnimation(self, 'geometry')
            self.shakeAnim.setDuration(1000)
            print(self.answerArea.geometry())
            self.shakeAnim.setStartValue(self.geometry())
            self.shakeAnim.setEndValue(QtCore.QRect(250, 250, 100, 30))
            self.shakeAnim.start()'''
            
        else:
            self.setToPuzzle()

    def setToPuzzle1(self):
        self.label.setPixmap(QtGui.QPixmap('firstpuzzle.png'))
        self.hintButton.hide()
        

    def setToPuzzle(self):
        self.hintButton.show()
        self.answerArea.hide()
        self.loadingBar.show()
        '''for i in range(0,30): 
            self.loadingBar.setValue(i)
            time.sleep(0.01)'''
        self.loadingBar.setRange(0,0)
        self.printAction.setEnabled(False)
        textForXML = self.answerArea.text().upper().replace(' ', '')
        textCopy2 = '"' + self.answerArea.text().upper() + '"'
        self.puzzlenamelabel.setText(textCopy2)
        puzzleinfo = dnbhl.getPuzzleInformation(textForXML)
        if puzzleinfo['type'] == 'text':
            self.label.setText(puzzleinfo['resource'])
        
        elif puzzleinfo['type'] == 'img':
            self.printAction.setEnabled(True)
            if puzzleinfo['resource'][-4:] == '.gif':
                self.movie = QtGui.QMovie(puzzleinfo['resource'], QtCore.QByteArray(), self)
                self.label.setMovie(self.movie)
                self.movie.start()
            else:
                self.label.setPixmap(QtGui.QPixmap('temp'))

        elif puzzleinfo['type'] == 'vid':
            self.movie = QtGui.QMovie('temp', QtCore.QByteArray(), self)
            self.label.setMovie(self.movie)
            self.movie.start()
        
        elif puzzleinfo['type'] == 'sound':
            self.label.setText(puzzleinfo['resource'][1])
            if puzzleinfo['resource'][0][-4:] == '.wav':
                QtMultimedia.QSound.play('temp')
            else:
                pipes = dict(stdin=PIPE, stdout=PIPE, stderr=PIPE)
                subprocess.Popen(["mplayer", "sound.m4a"], **pipes)
                mplayer.communicate(input=b">")

        self.loadingBar.hide()
        self.answerArea.show()
        self.answerArea.setText('')
        

        self.hint = puzzleinfo['hint']

    def getAHint(self):
        self.hintDialog = QtWidgets.QDialog()
        self.hintDialog.setStyleSheet("""
        QDialog {
        background-color: black;
        }
        QLabel {
        color: white;
        font-family: 'Brandon Grotesque';
        }
        QPushButton {
        background-color: black;
        color: white;
        font-family: 'Brandon Grotesque';
        border: 3px solid white;
        border-radius: 5px;
        }""")
        
        
        self.hintLabel = QtWidgets.QLabel(self.hint)
        self.OK = QtWidgets.QPushButton('OK')
        self.layoutthing = QtWidgets.QVBoxLayout()
        self.hintLabel.setWordWrap(True)
        self.layoutthing.addWidget(self.hintLabel, 0)
        self.layoutthing.addWidget(self.OK, 1)
        
        self.OK.clicked.connect(self.closeHint)
        self.hintDialog.setLayout(self.layoutthing)
        self.hintDialog.show()

    def closeHint(self):
        self.hintDialog.close()
    
    def exportResource(self):
        textForXML = self.puzzlenamelabel.text().replace('"', '').replace(' ', '')
        resourceData = dnbhl.getPuzzleInformation(textForXML)
        print(textForXML)
        with open('temp', 'rb') as file:
            data = file.read()

        
        fileToOpen = QtWidgets.QFileDialog.getSaveFileName(self, "Save Resource", '')[0]

        with open(fileToOpen, 'wb') as file:
            file.write(data)
                
    def printPicture(self):
        self.printer = QtPrintSupport.QPrinter()
        self.printDialog = QtPrintSupport.QPrintDialog(self.printer, self)
        self.printDialog.show()
        print(self.label.pixmap())
        if self.printDialog.exec_() == QtWidgets.QDialog.Accepted:
            self.printPainter = QtGui.QPainter(self.printer)
            rect = self.printPainter.viewport()
            size = self.label.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            self.printPainter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            self.printPainter.setWindow(self.label.pixmap().rect())
            self.printPainter.drawPixmap(0, 0, self.label.pixmap())


    def updateTimer(self):
        global minutes, hours, seconds
        seconds += 1
        if seconds == 60:
            seconds = 0
            minutes =+ 1
        try:
            if minutes == 60:
                minutes = 0
                hours =+ 1
        except:
            minutes = 0

        try:
            timerText = 'T: ' + str(hours) + ' : ' + str(minutes) + ' : ' + str(seconds)
        except:
            timerText = 'T: ' + str(0) + ' : ' + str(minutes) + ' : ' + str(seconds)
        self.timerWidget.setText(timerText)

if __name__ == '__main__':
    global app, window
    global minutes, hours, seconds
    minutes, hours, seconds = 0,0,0
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())