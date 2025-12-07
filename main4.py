from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import pygame

class Window(QMainWindow):
    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.bg_label.resize(self.size())
        self.resizeMainScreen()
        self.resizeCows()
        self.resizeBoards()
        

    def resizeMainScreen(self):
        base = min(self.width(), self.height())
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: black;
            }}
            #yourNameLabel {{
                font-size: {int(base * (1/45))}px;
                color: white;
                font-weight: bold;
                background-color: #c97d3f;
                border-radius: 5px;
                padding: {int(base * (1/90))}px;
                border-bottom: 2px solid #8C501F;
                border-right: 2px solid #8C501F;
            }}
            #navIcon {{
                background-color: #c97d3f;
                padding: {int(base * (1/90))}px;
                border-radius: 5px;
                border-bottom: 2px solid #8C501F;
                border-right: 2px solid #8C501F;
            }}
            #restartbutton {{
                background-color: #c97d3f;
                padding: {int(base * (1/90))}px {int(base * (1/45))}px;
                color: white;
                font-size: {int(base * (2/75))}px;
                font-family: "{self.font_family}";
                border-radius: 5px;
                border-bottom: 2px solid #8C501F;
                border-right: 2px solid #8C501F;
            }}
        """)

        self.soundIcon.setIconSize(QSize(int(base * (1/30)), int(base * (1/30))))
        self.pauseIcon.setIconSize(QSize(int(base * (1/30)), int(base * (1/30))))

    def resizeCows(self):
        base = min(self.width(), self.height())
        for cow in self.cows:
            cow.setFixedSize(int(base * (1/3)), int(base * (2/9)))
            cow.setIconSize(QSize(int(base * (1/3)), int(base * (2/9))))
            cow.move(-int(base * (1/3)), int(base * (32/45)))

        if self.cowanim is not None and self.currentCow is not None:
            self.cowanim.setStartValue(QPoint(-int(base * (1/3)), int(base * (32/45))))
            self.cowanim.setEndValue(QPoint(self.width(), int(base * (32/45))))
            self.cowanim.start()
            if not self.isPaused:
                self.cowanim.pause()

        for cowFlip in self.cowsFlipped:
            cowFlip.setFixedSize(int(base * (1/3)), int(base * (2/9)))
            cowFlip.setIconSize(QSize(int(base * (1/3)), int(base * (2/9))))
            cowFlip.move(self.width(), int(base * (32/45)))

        if self.cowanim2 is not None and self.currentCowFlip is not None:
            self.cowanim2.setStartValue(QPoint(self.width(), int(base * (32/45))))
            self.cowanim2.setEndValue(QPoint(-int(base * (1/3)), int(base * (32/45))))
            self.cowanim2.start()
            if not self.isPaused:
                self.cowanim2.pause()

    def resizeBoards(self):
        base = min(self.width(), self.height())
        self.board_label.setFixedSize(int(base * 10/9), int(base * 7/9))

        x = (self.width() - self.board_label.width()) // 2
        y = (self.height() - self.board_label.height()) // 2
        self.board_label.move(x,y)

        self.board_label.setStyleSheet(f"""
                #nameLabel {{
                    font-size: {int(base * 7/180)}px;
                    font-family: "{self.font_family}";
                    margin-top: {int(base * 1/6)}px;
                    color: #ffde59;
                }}
                #nameField {{
                    min-width: {int(base * 1/3)}px;
                    min-height: {int(base * 1/30)}px;
                    margin-top: {int(base * 1/90)}px;
                    padding: {int(base * 1/180)}px {int(base * 1/45)}px;
                    font-size: {int(base * 1/60)}px;
                    border: 1px solid black;
                    border-radius: {int(base * 1/45)}px;
                    background-color: white;
                }}
                #startButton {{
                    min-width: {int(base * 1/6)}px;
                    min-height: {int(base * 1/45)}px;
                    background-color: #ffde59;
                    border: 2px solid #725b00;
                    border-radius: {int(base * 1/45)}px;
                    padding: {int(base * 1/90)}px;
                    margin-top: {int(base * 1/30)}px;
                    font-size: {int(base * 1/36)}px;
                    font-weight: bold;
                    font-family: "{self.font_family}";
                }}
                #startButton:hover {{
                    background-color: #D9B832;
                }}
                #missingNameLabel {{
                    margin-top: {int(base * 1/45)}px;
                    font-size: {int(base * 17/900)}px;
                    font-family: "{self.font_family}";
                }}
            """)
        
        self.restartBoard_label.setFixedSize(int(base * 10/9), int(base * 7/9))
        x = (self.width() - self.restartBoard_label.width() + 20) // 2
        y = (self.height() - self.restartBoard_label.height()) // 2
        self.restartBoard_label.move(x,y)

        self.restartBoard_label.setStyleSheet(f"""
            #restartButton, #restartButtonNo {{
                min-width: {int(base * 1/6)}px;
                min-height: {int(base * 1/45)}px;
                background-color: #ffde59;
                border: 2px solid #725b00;
                border-radius: {int(base * 1/45)}px;
                padding: {int(base * 1/90)}px;
                font-size: {int(base * 1/36)}px;
                font-weight: bold;
                font-family: "{self.font_family}";
            }}
            #restartButton:hover, #restartButtonNo:hover {{
                background-color: #D9B832;
            }}
            #restartButton {{
                margin-top: {int(base * 7/18)}px;
            }}
        """)

        self.scoreBoard_label.setFixedSize(int(base * 10/9), int(base * 7/9))
        x = (self.width() - self.scoreBoard_label.width() + 20) // 2
        y = (self.height() - self.scoreBoard_label.height()) // 2
        self.scoreBoard_label.move(x,y)

        self.scoreBoard_label.setStyleSheet(f"""
            #scoreLabel {{
                font-size: {int(base * 7/90)}px;
                font-family: "{self.font_family}";
                margin-top: {int(base * 1/3)}px;
                color: #ffde59;
            }}
            #playAgainButton {{
                min-width: {int(base * 1/6)}px;
                min-height: {int(base * 1/45)}px;
                background-color: #ffde59;
                border: 2px solid #725b00;
                border-radius: {int(base * 1/45)}px;
                padding: {int(base * 1/90)}px;
                font-size: {int(base * 1/36)}px;
                font-weight: bold;
                font-family: "{self.font_family}";
                margin-top: {int(base * 1/18)}px;
            }}
            #playAgainButton:hover {{
                background-color: #D9B832;
            }}
        """)
        

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hit The Cows")
        self.resize(1500, 900)
        self.setWindowIcon(QIcon("cow.png"))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        font_id = QFontDatabase.addApplicationFont("Chewy-Regular.ttf")
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        self.bg_label = QLabel(self)
        self.bg_label.setPixmap(QPixmap("farm.png"))
        self.bg_label.setScaledContents(True) 

        self.cowanim = None
        self.cowanim2 = None

        self.currentCow = None
        self.currentCowFlip = None

        self.hitCount = 0
        self.missCount = 0
  
        self.gameOver = False
        self.isPaused = True

        self.missed = True
        self.missedFlip = True

        self.hitClick = True

        self.popSound = "popsound.MP3"
        self.bgMusic = "bg_music.mp3"

        self.cowNum = 25

        self.cows = []
        self.cowsFlipped = []
        base = min(self.width(), self.height())
        for i in range(self.cowNum):
            label = QPushButton(self)
            label.setIcon(QIcon("cow.png"))
            label.setFlat(True)
            label.setFixedSize(int(base * (1/3)), int(base * (2/9)))
            label.setIconSize(QSize(int(base * (1/3)), int(base * (2/9))))
            label.move(-int(base * (1/3)), int(base * (32/45)))
            label.hide()
            label.setCursor(QCursor(Qt.PointingHandCursor))

            label.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:pressed {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: transparent;
                    border: none;
                }
            """)

            self.cows.append(label)
            label.clicked.connect(lambda checked, c=label, cowtype="cow": self.hitCow(c, cowtype))

        for i in range(self.cowNum):

            labelflipped = QPushButton(self)
            labelflipped.setIcon(QIcon("cowflipped.png"))
            labelflipped.setFlat(True)
            labelflipped.setFixedSize(int(base * (1/3)), int(base * (2/9)))
            labelflipped.setIconSize(QSize(int(base * (1/3)), int(base * (2/9))))
            labelflipped.move(self.width(), int(base * (32/45)))
            labelflipped.hide()
            labelflipped.setCursor(QCursor(Qt.PointingHandCursor))

            self.resizeCows()

            labelflipped.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:pressed {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: transparent;
                    border: none;
                }
            """)

            self.cowsFlipped.append(labelflipped)
            labelflipped.clicked.connect(lambda checked, c=labelflipped, cowtype="cowFlip": self.hitCow(c, cowtype))
        self.index = 0
        self.indexFlipped = 0

        self.totalCows = len(self.cows) + len(self.cowsFlipped)
        
        labelflipped.setObjectName("cow")

        self.yourNameLabel = QLabel(self)
        self.yourNameLabel.setObjectName("yourNameLabel")
        self.yourNameLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.yourNameLabel.hide()

        self.isSoundOn = True
        self.bgSound = True

        self.soundIcon = QPushButton(self)
        self.soundIcon.setIcon(QIcon("sound.png"))
        self.soundIcon.setObjectName("navIcon")
        self.soundIcon.hide()
        self.soundIcon.setCursor(QCursor(Qt.PointingHandCursor))
        self.soundIcon.clicked.connect(lambda checked, sound=self.soundIcon: self.soundClick(sound))

        self.pauseIcon = QPushButton(self)
        self.pauseIcon.setIcon(QIcon("pause.png"))
        self.pauseIcon.setObjectName("navIcon")
        self.pauseIcon.hide()
        self.pauseIcon.setCursor(QCursor(Qt.PointingHandCursor))
        self.pauseIcon.clicked.connect(self.pauseGame)

        self.restartBtn = QPushButton("Restart", self)
        self.restartBtn.setObjectName("restartbutton")
        self.restartBtn.hide()
        self.restartBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.restartBtn.clicked.connect(self.restartButton)

        hbox = QHBoxLayout()
        hbox.addWidget(self.yourNameLabel, alignment=Qt.AlignLeft)
        hbox.addStretch()
        hbox.addWidget(self.soundIcon)
        hbox.setSpacing(20)
        hbox.addWidget(self.pauseIcon)
        hbox.setSpacing(20)
        hbox.addWidget(self.restartBtn)
        hbox.setContentsMargins(30,20,30,0)

        vbox1 = QVBoxLayout()
        vbox1.addLayout(hbox)
        vbox1.addStretch()
        self.bg_label.setLayout(vbox1)

        self.board_image = QPixmap("board.png")
        self.board_label = QLabel(self)
        self.board_label.setPixmap(self.board_image)
        self.board_label.setScaledContents(True)

        self.restartBoard_image = QPixmap("restartBoard.png")
        self.restartBoard_label = QLabel(self)
        self.restartBoard_label.setPixmap(self.restartBoard_image)
        self.restartBoard_label.setScaledContents(True)
        self.restartBoard_label.hide()

        self.scoreBoard_image = QPixmap("scoreBoard.png")
        self.scoreBoard_label = QLabel(self)
        self.scoreBoard_label.setPixmap(self.scoreBoard_image)
        self.scoreBoard_label.setScaledContents(True)
        self.scoreBoard_label.hide()

        if self.board_label:
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.5)
            self.bg_label.setGraphicsEffect(opacity_effect)

            shadow = QGraphicsDropShadowEffect()
            shadow.setOffset(0, 0)    
            shadow.setBlurRadius(20)        
            shadow.setColor(QColor("#725b00"))

            self.nameLabel = QLabel(self.board_label)
            self.nameField = QLineEdit(self.board_label)
            self.startButton = QPushButton(self.board_label)
            self.missingNameLabel = QLabel(self.board_label)

            self.nameLabel.setGraphicsEffect(shadow)

            self.nameLabel.setObjectName("nameLabel")
            self.nameField.setObjectName("nameField")
            self.startButton.setObjectName("startButton")
            self.missingNameLabel.setObjectName("missingNameLabel")

            self.startButton.setCursor(QCursor(Qt.PointingHandCursor))
            self.startButton.clicked.connect(
                lambda checked, bg=self.bg_label, cowlabel=label, cowlabelflipped = labelflipped, board=self.board_label, namefield=self.nameField, sound=self.soundIcon, pause=self.pauseIcon, restart=self.restartBtn, yourName=self.yourNameLabel, missingName=self.missingNameLabel: self.startClick(bg,cowlabel, cowlabelflipped, board, namefield, sound, pause, restart, yourName, missingName)
            )

            self.startBoard(self.nameLabel, self.startButton, self.missingNameLabel)

            vbox = QVBoxLayout()
            vbox.addWidget(self.nameLabel, alignment=Qt.AlignCenter)
            vbox.addWidget(self.nameField, alignment=Qt.AlignCenter)
            vbox.addWidget(self.startButton, alignment=Qt.AlignCenter)
            vbox.addWidget(self.missingNameLabel, alignment=Qt.AlignCenter)
            vbox.setAlignment(Qt.AlignCenter)
            self.board_label.setLayout(vbox)


    def backgroundMusic(self):
        pygame.mixer.init()
        bg = pygame.mixer.music
        if self.bgSound:
            bg.load(self.bgMusic)
            bg.set_volume(0.5)
            bg.play()
        else:
            bg.stop()

    def startBoard(self, label, startButton, missingName):
        label.setText("Enter your name:")
        startButton.setText("Start")
        missingName.setText("Please enter your name")
        missingName.hide()
        self.backgroundMusic()


    def startClick(self, bg, cowlabel, cowlabelflipped, board, namefield, sound, pause, restart, yourName, missingName):
        if (namefield.text() == ""):
            missingName.show()
        else:
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(1)
            bg.setGraphicsEffect(opacity_effect)
            board.hide()
            yourName.setText(f"{namefield.text()} has hit {self.hitCount} cows, has missed {self.missCount} cows")
            yourName.show()
            sound.show()
            pause.show()
            restart.show()
            self.moveFirstCow()
            self.moveSecondCow()

            self.pauseIcon.setIcon(QIcon("pause.png"))
            self.pauseIcon.setEnabled(True)
            
            self.soundIcon.setEnabled(True)
            self.restartBtn.setEnabled(True)
            self.bgSound = False
            self.backgroundMusic()

    def soundClick(self, sound):
        if self.isSoundOn:
            sound.setIcon(QIcon("soundoff.png"))
            self.isSoundOn = False
        else:
            sound.setIcon(QIcon("sound.png"))
            self.isSoundOn = True

    def endGame(self):
        if self.gameOver:
            return
        self.gameOver = True
        if self.cowanim:
            self.cowanim.stop()
        if self.cowanim2:
            self.cowanim2.stop()

        if 0 <= self.index < len(self.cows):
            self.cows[self.index].hide()

        if 0 <= self.indexFlipped < len(self.cowsFlipped):
            self.cowsFlipped[self.indexFlipped].hide()

        self.bgSound = True
        self.backgroundMusic()
        self.scoreBoard()

    def moveFirstCow(self):
        if self.gameOver:
            return

        if self.index >= len(self.cows):
            self.endGame()
            return

        self.missed = True

        cow = self.cows[self.index]
        cow.show()
        base = min(self.width(), self.height())
        self.cowanim = QPropertyAnimation(cow, b"pos")
        self.cowanim.setDuration(1500)
        self.cowanim.setStartValue(QPoint(0 - cow.width(), int(base * (32/45))))
        self.cowanim.setEndValue(QPoint(self.width(), int(base * (32/45))))

        self.cowanim.finished.connect(lambda: self.nextCow(cow, "cow"))
        self.cowanim.start()

        self.currentCow = cow

        if self.hitCount > 20:
            self.cowanim.setDuration(1400)

        if self.hitCount >= 40:
            self.cowanim.setDuration(1000)


    def moveSecondCow(self):
        if self.gameOver:
            return
        
        if self.indexFlipped >= len(self.cowsFlipped):
            self.endGame()
            return
        
        self.missedFlip = True

        cowFlip = self.cowsFlipped[self.indexFlipped]
        cowFlip.show()
        base = min(self.width(), self.height())
        self.cowanim2 = QPropertyAnimation(cowFlip, b"pos")
        self.cowanim2.setDuration(1400)
        self.cowanim2.setStartValue(QPoint(self.width(), int(base * (32/45))))
        self.cowanim2.setEndValue(QPoint(0 - cowFlip.width(), int(base * (32/45))))

        self.cowanim2.finished.connect(lambda: self.nextCow(cowFlip, "cowFlip"))
        self.cowanim2.start()

        self.currentCowFlip = cowFlip

        if self.hitCount > 20:
            self.cowanim2.setDuration(1300)

        if self.hitCount >= 40:
            self.cowanim2.setDuration(1000)


    def nextCow(self, cow_label, cow_type):
        if cow_type == "cow":
            if self.missed:
                self.missCount += 1
            cow_label.hide()
            self.index += 1
            self.updateLabel()
            if self.index < len(self.cows):
                self.moveFirstCow()
        else:
            if self.missedFlip:
                self.missCount += 1
            cow_label.hide()
            self.indexFlipped += 1
            self.updateLabel()
            if self.indexFlipped < len(self.cowsFlipped):
                self.moveSecondCow()
        if (self.index >= len(self.cows)) and (self.indexFlipped >= len(self.cowsFlipped)):
            self.endGame()

    def hitCow(self, cow_label, cow_type):
        cow_label.setStyleSheet("background-color: transparent")

        if not self.hitClick:
            return

        cow_label.hide()
        self.hitCount += 1
        if self.isSoundOn:
            pygame.mixer.init()
            pygame.mixer.music.load(self.popSound)
            pygame.mixer.music.play()

        if cow_type == "cow":
            self.missed = False
        else:
            self.missedFlip = False

        self.nextCow(cow_label, cow_type)
        self.updateLabel()

    def updateLabel(self):
        if self.gameOver:
            return
        self.yourNameLabel.setText(f"{self.nameField.text()} has hit {self.hitCount} cows, has missed {self.missCount} cows")
        self.yourNameLabel.show()

    def pauseGame(self):
        if self.isPaused:
            self.cowanim.pause()
            self.cowanim2.pause()
            self.isPaused = False
            self.pauseIcon.setIcon(QIcon("play.png"))
            self.hitClick = False
            self.cows[self.index].setCursor(QCursor(Qt.ArrowCursor))
            self.cowsFlipped[self.indexFlipped].setCursor(QCursor(Qt.ArrowCursor))
        else:
            self.cowanim.resume()
            self.cowanim2.resume()
            self.isPaused = True
            self.pauseIcon.setIcon(QIcon("pause.png"))
            self.hitClick = True

    def restartButton(self):
        if self.gameOver:
            return
        self.restartBoard_label.show()
        self.restartBoard_label.raise_()
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)
        self.bg_label.setGraphicsEffect(opacity_effect)
        if 0 <= self.index < len(self.cows):
            opacity_effect1 = QGraphicsOpacityEffect()
            opacity_effect1.setOpacity(0.5)

            cow = self.cows[self.index]
            cow.setGraphicsEffect(opacity_effect1)
        if 0 <= self.indexFlipped < len(self.cowsFlipped):
            opacity_effect1 = QGraphicsOpacityEffect()
            opacity_effect1.setOpacity(0.5)
            cowFlipped = self.cowsFlipped[self.indexFlipped]
            cowFlipped.setGraphicsEffect(opacity_effect1)
        self.cowanim.pause()
        self.cowanim2.pause()
        self.isPaused = True

        restartButton = QPushButton("Yes", self.restartBoard_label)
        restartButton.setObjectName("restartButton")

        restartButtonNo = QPushButton("No", self.restartBoard_label)
        restartButtonNo.setObjectName("restartButtonNo")

        vbox = QVBoxLayout()
        vbox.addWidget(restartButton, alignment=Qt.AlignCenter)
        vbox.addWidget(restartButtonNo, alignment=Qt.AlignCenter)
        vbox.addStretch()
        self.restartBoard_label.setLayout(vbox)
        restartButton.setCursor(QCursor(Qt.PointingHandCursor))
        restartButtonNo.setCursor(QCursor(Qt.PointingHandCursor))

        restartButton.clicked.connect(self.restartGame)
        restartButtonNo.clicked.connect(self.resumeGame)

        self.pauseIcon.setIcon(QIcon("pause.png"))
        self.pauseIcon.setEnabled(False)
        self.soundIcon.setEnabled(False)
        self.restartBtn.setEnabled(False)

    def restartGame(self):
        self.restartBoard_label.hide()

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(1)
        self.bg_label.setGraphicsEffect(opacity_effect)

        if 0 <= self.index < len(self.cows):
            opacity_effect1 = QGraphicsOpacityEffect()
            opacity_effect1.setOpacity(1)
        
            cow = self.cows[self.index]
            cow.setGraphicsEffect(opacity_effect1)
        if 0 <= self.indexFlipped < len(self.cowsFlipped):
            opacity_effect1 = QGraphicsOpacityEffect()
            opacity_effect1.setOpacity(1)
            cowFlipped = self.cowsFlipped[self.indexFlipped]
            cowFlipped.setGraphicsEffect(opacity_effect1)

        for cow in self.cows:
            if hasattr(cow, "anim"):
                cow.anim.stop()
            cow.hide()

        for cow in self.cowsFlipped:
            if hasattr(cow, "anim"):
                cow.anim.stop()
            cow.hide()

        # RESET INDEXES
        self.index = 0
        self.indexFlipped = 0

        self.pauseIcon.setEnabled(True)
        
        self.soundIcon.setEnabled(True)
        self.restartBtn.setEnabled(True)
        self.yourNameLabel.show()

        self.hitCount = 0
        self.missCount = 0
  
        self.gameOver = False
        self.hitClick = True

        self.missed = True
        self.missedFlip = True

        self.totalCows = len(self.cows) + len(self.cowsFlipped)

        self.updateLabel()

        self.moveFirstCow()
        self.moveSecondCow()

    def resumeGame(self):
        self.restartBoard_label.hide()

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(1)
        self.bg_label.setGraphicsEffect(opacity_effect)

        if 0 <= self.index < len(self.cows):
            opacity_effect1 = QGraphicsOpacityEffect()
            opacity_effect1.setOpacity(1)

            cow = self.cows[self.index]
            cow.setGraphicsEffect(opacity_effect1)
        if 0 <= self.indexFlipped < len(self.cowsFlipped):
            opacity_effect1 = QGraphicsOpacityEffect()
            opacity_effect1.setOpacity(1)
            cowFlipped = self.cowsFlipped[self.indexFlipped]
            cowFlipped.setGraphicsEffect(opacity_effect1)

        self.pauseIcon.setEnabled(True)
        
        self.restartBtn.setEnabled(True)
        self.soundIcon.setEnabled(True)
        self.yourNameLabel.show()

        self.cowanim.resume()
        self.cowanim2.resume()

    def playAgain(self):
        self.scoreBoard_label.hide()
        self.board_label.show()
        self.hitCount = 0
        self.missCount = 0
  
        self.gameOver = False

        self.missed = True
        self.missedFlip = True

        self.missingNameLabel.hide()

        self.cowNum = 25

        self.cows = []
        self.cowsFlipped = []
        base = min(self.width(), self.height())
        for i in range(self.cowNum):
            label = QPushButton(self)
            label.setIcon(QIcon("cow.png"))
            label.setFlat(True)
            label.setFixedSize(int(base * (1/3)), int(base * (2/9)))
            label.setIconSize(QSize(int(base * (1/3)), int(base * (2/9))))
            label.move(-int(base * (1/3)), int(base * (32/45)))
            label.hide()
            label.setCursor(QCursor(Qt.PointingHandCursor))

            label.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:pressed {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: transparent;
                    border: none;
                }
            """)

            self.cows.append(label)
            label.clicked.connect(lambda checked, c=label, cowtype="cow": self.hitCow(c, cowtype))

        for i in range(self.cowNum):

            labelflipped = QPushButton(self)
            labelflipped.setIcon(QIcon("cowflipped.png"))
            labelflipped.setFlat(True)
            labelflipped.setFixedSize(int(base * (1/3)), int(base * (2/9)))
            labelflipped.setIconSize(QSize(int(base * (1/3)), int(base * (2/9))))
            labelflipped.move(self.width(), int(base * (32/45)))
            labelflipped.hide()
            labelflipped.setCursor(QCursor(Qt.PointingHandCursor))

            labelflipped.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:pressed {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: transparent;
                    border: none;
                }
            """)

            self.cowsFlipped.append(labelflipped)
            labelflipped.clicked.connect(lambda checked, c=labelflipped, cowtype="cowFlip": self.hitCow(c, cowtype))
        self.index = 0
        self.indexFlipped = 0

        self.totalCows = len(self.cows) + len(self.cowsFlipped)

        self.pauseIcon.hide()
        self.soundIcon.hide()
        self.restartBtn.hide()
        self.yourNameLabel.hide()
        self.bgSound = True
        self.backgroundMusic()

    def scoreBoard(self):
        self.scoreBoard_label.show()
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)
        self.bg_label.setGraphicsEffect(opacity_effect)

        if self.scoreBoard_label.layout() is None:

            self.scoreLabel = QLabel(self.scoreBoard_label)
            self.scoreField = QLineEdit(self.scoreBoard_label)
            playAgainButton = QPushButton("Play Again", self.scoreBoard_label)

            self.scoreLabel.setObjectName("scoreLabel")
            playAgainButton.setObjectName("playAgainButton")

            vbox = QVBoxLayout()
            vbox.addWidget(self.scoreLabel, alignment=Qt.AlignCenter)
            vbox.addWidget(playAgainButton, alignment=Qt.AlignCenter)
            vbox.addStretch()
            self.scoreBoard_label.setLayout(vbox)
            playAgainButton.setCursor(QCursor(Qt.PointingHandCursor))

            shadow = QGraphicsDropShadowEffect()
            shadow.setOffset(0, 0)    
            shadow.setBlurRadius(20)        
            shadow.setColor(QColor("#725b00"))

            self.scoreLabel.setGraphicsEffect(shadow)

            playAgainButton.clicked.connect(self.playAgain)

        self.scoreLabel.setText(f"{self.hitCount} / {self.totalCows}")

        self.pauseIcon.setIcon(QIcon("pause.png"))
        self.pauseIcon.setEnabled(False)
        self.soundIcon.setEnabled(False)
        self.restartBtn.setEnabled(False)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())