import matplotlib,os,cv2,sys
matplotlib.use("Qt5Agg")
import imageai
import PyQt5

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from imageai.Detection import VideoObjectDetection
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal

class detectedObject():
    def __init__(self, pid, name, cx, cy):
        self.pid = pid
        self.name = name
        self.cx = cx
        self.cy = cy
        self.track = [[self.cx, self.cy], ]
        return

    def getX(self):
        return self.cx

    def getY(self):
        return self.cy

    def getName(self):
        return self.name

    def updateCoords(self, n_cx, n_cy):
        self.cx = n_cx
        self.cy = n_cy
        self.track.append([n_cx, n_cy])
        return

    def getTrack(self):
        return self.track

class MyFigure(FigureCanvas):
    def __init__(self, width=10, heigh=10, dpi=100):
        self.figs = Figure(figsize=(width, heigh), dpi=dpi)
        self.figs.set_facecolor('#222222')
        super(MyFigure, self).__init__(self.figs)
        self.axes = self.figs.add_subplot(111)
        self.axes.set_facecolor('#222222')
        self.axes.tick_params(axis = 'x',colors = '#ccc')
        self.axes.tick_params(axis='y', colors='#ccc')
        self.axes.spines['bottom'].set_color('#ccc')
        self.axes.spines['top'].set_color('#ccc')
        self.axes.spines['left'].set_color('#ccc')
        self.axes.spines['right'].set_color('#ccc')
class Counter(QThread):
    for_frame_signal=pyqtSignal(list)
    def __init__(self, person_checked,car_checked,bike_checked,p1_x,p1_y,p2_x,
                p2_y,probability,detect_speed,frame_per_second,frame_interval,
                detect_mode,input_file,output_dir):
        super().__init__()
        self.person_checked=person_checked
        self.car_checked=car_checked
        self.bike_checked=bike_checked
        self.p1_x=p1_x
        self.p1_y=p1_y
        self.p2_x=p2_x
        self.p2_y=p2_y
        self.probability=probability
        self.detect_speed=detect_speed
        self.frame_per_second=frame_per_second
        self.frame_interval=frame_interval
        self.detect_mode=detect_mode
        self.input_file = input_file
        self.output_dir = output_dir
    def run(self):
        self.video_detect()
    def forFrame(self, frame_number, output_array, output_count, returned_frame):
        self.for_frame_signal.emit([frame_number, output_array, output_count, returned_frame])
    def video_detect(self):
        video_detector = VideoObjectDetection()
        video_detector.setModelTypeAsYOLOv3()
        video_detector.setModelPath(os.path.join(os.getcwd(), "yolov3.pt"))
        #detection speed not support in latest version
        # video_detector.loadModel(detection_speed=self.detect_speed)
        video_detector.loadModel()
        custom_objects = video_detector.CustomObjects(person=self.person_checked, car=self.car_checked,bicycle=self.bike_checked)
        video_detector.detectObjectsFromVideo(custom_objects=custom_objects,
                                                    input_file_path=self.input_file,
                                                    save_detected_video=False, frame_detection_interval=self.frame_interval,
                                                    frames_per_second=self.frame_per_second ,per_frame_function=self.forFrame,
                                                    minimum_percentage_probability=self.probability, return_detected_frame=True,
                                                    log_progress=False)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 586)
        font = QtGui.QFont("Arial",10)
        # font.setPointSize(10)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setFont(font)
        self.groupBox.setGeometry(QtCore.QRect(240, 0, 551, 491))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 0, 221, 541))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 220, 201, 111))
        self.groupBox_4.setObjectName("groupBox_4")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 20, 35, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setGeometry(QtCore.QRect(80, 20, 35, 16))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_4)
        self.radioButton.setFont(font)
        self.radioButton.setGeometry(QtCore.QRect(150, 20, 35, 16))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.label = QtWidgets.QLabel(self.groupBox_4)
        self.label.setFont(font)
        self.label.setGeometry(QtCore.QRect(10, 50, 54, 12))
        self.label.setObjectName("label")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setGeometry(QtCore.QRect(92, 50, 91, 20))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setFont(font)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 71, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setGeometry(QtCore.QRect(90, 80, 91, 20))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 340, 201, 51))
        self.groupBox_5.setObjectName("groupBox_5")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox_5)
        self.radioButton_4.setFont(font)
        self.radioButton_4.setGeometry(QtCore.QRect(10, 20, 71, 16))
        self.radioButton_4.setChecked(True)
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_5 = QtWidgets.QRadioButton(self.groupBox_5)
        self.radioButton_5.setFont(font)
        self.radioButton_5.setGeometry(QtCore.QRect(110, 20, 83, 16))
        self.radioButton_5.setObjectName("radioButton_5")
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setGeometry(QtCore.QRect(10, 160, 201, 51))
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox_6)
        self.horizontalSlider.setFont(font)
        self.horizontalSlider.setGeometry(QtCore.QRect(30, 20, 131, 22))
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setProperty("value", 30)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_6 = QtWidgets.QLabel(self.groupBox_6)
        self.label_6.setFont(font)
        self.label_6.setGeometry(QtCore.QRect(10, 20, 16, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_6)
        self.label_7.setFont(font)
        self.label_7.setGeometry(QtCore.QRect(165, 20, 31, 21))
        self.label_7.setObjectName("label_7")
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_7.setFont(font)
        self.groupBox_7.setGeometry(QtCore.QRect(10, 400, 201, 131))
        self.groupBox_7.setObjectName("groupBox_7")
        self.label_9 = QtWidgets.QLabel(self.groupBox_7)
        self.label_9.setFont(font)
        self.label_9.setGeometry(QtCore.QRect(10, 20, 96, 16))
        self.label_9.setObjectName("label_9")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setGeometry(QtCore.QRect(10, 40, 131, 20))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton.setFont(font)
        self.pushButton.setGeometry(QtCore.QRect(150, 40, 41, 23))
        self.pushButton.setObjectName("pushButton")
        self.label_10 = QtWidgets.QLabel(self.groupBox_7)
        self.label_10.setFont(font)
        self.label_10.setGeometry(QtCore.QRect(10, 70, 96, 16))
        self.label_10.setObjectName("label_10")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setGeometry(QtCore.QRect(10, 90, 131, 20))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 90, 41, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_8.setFont(font)
        self.groupBox_8.setGeometry(QtCore.QRect(10, 70, 201, 81))
        self.groupBox_8.setObjectName("groupBox_8")
        self.label_3 = QtWidgets.QLabel(self.groupBox_8)
        self.label_3.setFont(font)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 36, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_8)
        self.lineEdit.setFont(font)
        self.lineEdit.setGeometry(QtCore.QRect(50, 20, 61, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_8)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setGeometry(QtCore.QRect(120, 20, 71, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_8)
        self.label_4.setFont(font)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 36, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_8)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setGeometry(QtCore.QRect(50, 50, 61, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_8)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setGeometry(QtCore.QRect(120, 50, 71, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_9.setFont(font)
        self.groupBox_9.setGeometry(QtCore.QRect(10, 20, 201, 41))
        self.groupBox_9.setObjectName("groupBox_9")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_9)
        self.checkBox.setFont(font)
        self.checkBox.setGeometry(QtCore.QRect(10, 20, 35, 16))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_9)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setGeometry(QtCore.QRect(70, 20, 35, 16))
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_9)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setGeometry(QtCore.QRect(130, 20, 59, 16))
        self.checkBox_3.setChecked(False)
        self.checkBox_3.setObjectName("checkBox_3")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(240, 500, 551, 41))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setGeometry(QtCore.QRect(460, 10, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setGeometry(QtCore.QRect(350, 10, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setFont(font)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setStyleSheet("QStackedWidget, QLabel, QPushButton, QRadioButton, QCheckBox,\n"
                             "QGroupBox, QStatusBar, QToolButton, QComboBox, QDialog {\n"
                             "    background-color: #222222;\n"
                             "    color: #BBBBBB;\n"
                             "    font-family: \"Arial\";\n"
                             "}\n"
                             "/* === QWidget === */\n"
                             "QWidget:window {\n"
                             "    background: #222222;\n"
                             "    color: #BBBBBB;\n"
                             "    font-family: \"Arial\";\n"
                             "}\n"
                             "/* === QPushButton === */\n"
                             "QPushButton {\n"
                             "    border: 1px solid #333333;\n"
                             "    padding: 4px;\n"
                             "    min-width: 65px;\n"
                             "    min-height: 12px;\n"
                             "}\n"
                             "QPushButton:hover {\n"
                             "    background-color: #333333;\n"
                             "    border-color: #444444;\n"
                             "}\n"
                             "QPushButton:pressed {\n"
                             "    background-color: #111111;\n"
                             "    border-color: #333333;\n"
                             "    color: yellow;\n"
                             "}\n"
                             "\n"
                             "QPushButton:disabled {\n"
                             "    color: #333333;\n"
                             "}\n"
                             "/* === Checkable items === */\n"
                             "QCheckBox::indicator, QRadioButton::indicator, QTreeView::indicator {\n"
                             "    width: 16px;\n"
                             "    height: 16px;\n"
                             "    background-color: #111111;\n"
                             "    border: 1px solid #333333;\n"
                             "}\n"
                             "QRadioButton::indicator {\n"
                             "    border-radius: 8px;\n"
                             "}\n"
                             "QCheckBox::indicator::checked, QRadioButton::indicator::checked, QTreeView::indicator::checked {\n"
                             "    background-color: qradialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #BBBBBB, stop:1 #111111);\n"
                             "}\n"
                             "QCheckBox::indicator:disabled, QRadioButton::indicator:disabled, QTreeView::indicator:disabled {\n"
                             "    background-color: #444444;\n"
                             "}\n"
                             "QCheckBox::indicator::checked:disabled, QRadioButton::indicator::checked:disabled, QTreeView::indicator::checked:disabled {\n"
                             "    background-color: qradialgradient(cx:0.5, cy:0.5, fx:0.25, fy:0.15, radius:0.3, stop:0 #BBBBBB, stop:1 #444444);\n"
                             "}\n"
                             "/* === QGroupBox === */\n"
                             "QGroupBox {\n"
                             "    border: 2px solid #333333;\n"
                             "    margin-top: 2ex;\n"
                             "}\n"
                             "QGroupBox::title {\n"
                             "    color: #ccc;\n"
                             "    subcontrol-origin: margin;\n"
                             "    subcontrol-position: top left;\n"
                             "    margin-left: 5px;\n"
                             "}\n"
                             "QLineEdit, QListView, QTreeView, QTableView, QAbstractSpinBox {\n"
                             "    background-color: black;\n"
                             "    color: #BBBBBB;\n"
                             "    border: 1px solid #333333;\n"
                             "}\n"
                             "}")
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Detection Window"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Settings"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Detection Speed"))
        self.radioButton_2.setText(_translate("MainWindow", "S"))
        self.radioButton_3.setText(_translate("MainWindow", "M"))
        self.radioButton.setText(_translate("MainWindow", "F"))
        self.label.setText(_translate("MainWindow", "Frames/s:"))
        self.lineEdit_7.setText(_translate("MainWindow", "25"))
        self.label_2.setText(_translate("MainWindow", "Frame_interval:"))
        self.lineEdit_8.setText(_translate("MainWindow", "2"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Directions:"))
        self.radioButton_4.setText(_translate("MainWindow", "Distinguish"))
        self.radioButton_5.setText(_translate("MainWindow", "No_distinguish"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Minimum_percentage_probability"))
        self.label_6.setText(_translate("MainWindow", "0%"))
        self.label_7.setText(_translate("MainWindow", "100%"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Input&Output"))
        self.label_9.setText(_translate("MainWindow", "Input_vedio_path:"))
        self.lineEdit_5.setText(_translate("MainWindow", "input/test.mp4"))
        self.pushButton.setText(_translate("MainWindow", "Open_file"))
        self.label_10.setText(_translate("MainWindow", "Output_dir_path:"))
        self.lineEdit_6.setText(_translate("MainWindow", "output/"))
        self.pushButton_2.setText(_translate("MainWindow", "Open_dir"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Detection_line"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Run"))
        self.label_3.setText(_translate("MainWindow", "Start:"))
        self.lineEdit.setText(_translate("MainWindow", "0"))
        self.lineEdit_2.setText(_translate("MainWindow", "150"))
        self.label_4.setText(_translate("MainWindow", "End:"))
        self.lineEdit_3.setText(_translate("MainWindow", "800"))
        self.lineEdit_4.setText(_translate("MainWindow", "250"))
        self.groupBox_9.setTitle(_translate("MainWindow", "Dection_object"))
        self.checkBox.setText(_translate("MainWindow", "person"))
        self.checkBox_2.setText(_translate("MainWindow", "car"))
        self.checkBox_3.setText(_translate("MainWindow", "bike"))
        self.pushButton_4.setText(_translate("MainWindow", "Stop"))
        self.pushButton_3.setText(_translate("MainWindow", "Compute"))
class MainDialogImgBW(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("VidioCounter v1.0")
        self.setMinimumSize(0,0)
        self.canvas = MyFigure()
        self.figure=self.canvas.figs
        self.axes=self.canvas.axes
        self.gridlayout_ = QGridLayout(self.groupBox)
        self.gridlayout_.addWidget(self.canvas,0,1)
        self.pushButton_3.clicked.connect(self.count_begin)
        self.pushButton_4.clicked.connect(self.count_stop)
        self.pushButton.clicked.connect(self.choose_file)
        self.pushButton_2.clicked.connect(self.choose_dir)
    def init_settings(self):
        self.person_checked = False
        self.car_checked = False
        self.bike_checked = False
        self.probability=self.horizontalSlider.value()
        self.detect_speed='fast'
        if self.checkBox.checkState()==QtCore.Qt.Checked:
            self.person_checked=True
        if self.checkBox_2.checkState()==QtCore.Qt.Checked:
            self.car_checked=True
        if self.checkBox_3.checkState()==QtCore.Qt.Checked:
            self.bike_checked=True
        try:
            self.p1_x = int(self.lineEdit.text())
            self.p1_y = int(self.lineEdit_2.text())
            self.p2_x = int(self.lineEdit_3.text())
            self.p2_y = int(self.lineEdit_4.text())
            self.frame_per_second = int(self.lineEdit_7.text())
            self.frame_interval = int(self.lineEdit_8.text())
            self.input_file = self.lineEdit_5.text()
            self.output_dir = self.lineEdit_6.text()
        except Exception as e:
            QMessageBox.information(QWidget(), "Warning", "Error:%s" % e)
        if self.radioButton.isChecked():
            self.detect_speed = 'faster'
        if self.radioButton_2.isChecked():
            self.detect_speed='normal'
        if self.radioButton_3.isChecked():
            self.detect_speed = 'fast'
        if self.radioButton_4.isChecked():
            self.detect_mod=1
        if self.radioButton_5.isChecked():
            self.detect_mod=2
        print(self.person_checked,self.car_checked,self.bike_checked,self.p1_x,self.p1_y,self.p2_x,
              self.p2_y,self.probability,self.detect_speed,self.frame_per_second,self.frame_interval,
              self.detect_mod,
              self.input_file,
              self.output_dir)
    def count_begin(self):
        self.init_settings()
        self.count = []
        self.objects_2 = []
        self.objects = []
        obj = detectedObject(0, '', 0, 0)
        self.objects.append(obj)
        self.count_car_up, self.count_car_down = [], []
        self.count_person_up, self.count_person_down = [], []
        self.count_bike_up, self.count_bike_down = [], []
        self.execution_path = os.getcwd()
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.videowriter = cv2.VideoWriter(os.path.join(self.output_dir,os.path.split(self.input_file)[-1][:-4]+'_count.avi'), self.fourcc, 25, (640, 480))
        self.count_thread=Counter(person_checked=self.person_checked,car_checked=self.car_checked,bike_checked=self.bike_checked,
                                p1_x=self.p1_x,p1_y=self.p1_y,p2_x=self.p2_x,
                                p2_y=self.p2_y,probability=self.probability,detect_speed=self.detect_speed,
                                frame_per_second=self.frame_per_second,frame_interval=self.frame_interval,
                                detect_mode=self.detect_mod,input_file=self.input_file,output_dir=self.output_dir)
        self.count_thread.for_frame_signal.connect(self.for_frame)
        with open(os.path.join(self.output_dir, os.path.split(self.input_file)[-1][:-4] + '.csv'), 'w') as f:
            f.write('time(min),person_up,person_down,car_up,car_down' + '\n')
        self.count_thread.start()
    def count_stop(self):
        self.count_thread.terminate()
    def choose_dir(self):
        dir=QFileDialog.getExistingDirectory(self,"Select_folder",os.getcwd())
        if dir=="":
            dir="output/"
        self.lineEdit_6.setText(dir)
    def choose_file(self):
        filename,filetype = QFileDialog.getOpenFileName(self,"Select_file",os.getcwd(),"All Files (*);;Vedio Files (*.mp4)")
        if filename=="":
            filename="input/test.mp4"
        self.lineEdit_5.setText(filename)
    def for_frame(self,value):
        frame_number, output_array, output_count, returned_frame=value
        height = returned_frame.shape[0]
        width = returned_frame.shape[1]
        y1_ = self.p2_y
        y2_ = self.p1_y
        k = (y2_ - y1_) / width
        self.figure.clf()
        self.axes = self.figure.add_subplot(111)
        self.axes.set_facecolor('#222222')
        self.axes.tick_params(axis='x', colors='#ccc')
        self.axes.tick_params(axis='y', colors='#ccc')
        self.axes.spines['bottom'].set_color('#ccc')
        self.axes.spines['top'].set_color('#ccc')
        self.axes.spines['left'].set_color('#ccc')
        self.axes.spines['right'].set_color('#ccc')
        if frame_number % 100 == 0:
            self.objects.clear()
            obj = detectedObject(0, '', 0, 0)
            self.objects.append(obj)
        if frame_number % self.frame_interval == 0:
            for i in output_array:
                c_list = []
                d_list = []
                new = ''
                self.count.append(1)
                x1, y1, x2, y2 = i['box_points']
                cx_ = (x1 + x2) / 2
                cy_ = (y1 + y2) / 2
                name = i['name']
                pid = len(self.count)
                self.axes.plot(cx_, cy_, color='red')
                for j in self.objects[-50:]:
                    if abs(cx_ - j.getX()) <= abs(x2 - x1) and abs(cy_ - j.getY()) <= abs(
                            y2 - y1) and name == j.getName():
                        new = False
                        distance = (j.getX() - cx_) ** 2 + (j.getY() - cy_) ** 2
                        if distance != 0:
                            c_list.append(j)
                            d_list.append(distance)
                    else:
                        new = True
                if c_list != []:
                    o = c_list[d_list.index(min(d_list))]
                    o.updateCoords(cx_, cy_)
                    track = o.getTrack()
                    x = []
                    y = []
                    for t in range(len(track)):
                        x.append(track[t][0])
                        y.append(track[t][1])
                    self.axes.plot(x, y, color='red')
                    self.axes.plot(track[-1][0], track[-1][1], 'o', color='red')
                    self.axes.plot(track[-1][0], y2_ - k * track[-1][0], 'o', color='green')
                    if (track[-1][1] - y2_ + k * track[-1][0]) > 0 and (track[0][1] - y2_ + k * track[0][0]) < 0:
                        if self.car_checked and o.getName() == 'car':
                            self.count_car_down.append(o)
                        if self.person_checked and o.getName() == 'person':
                            self.count_person_down.append(o)
                        if self.bike_checked and o.getName()=='bicycle':
                            self.count_bike_down.append(o)
                        self.objects.remove(o)
                    if (track[-1][1] - y2_ + k * track[-1][0]) < 0 and (track[0][1] - y2_ + k * track[0][0]) > 0:
                        if self.car_checked  and o.getName() == 'car':
                            self.count_car_up.append(o)
                        if self.person_checked and o.getName() == 'person':
                            self.count_person_up.append(o)
                        if self.bike_checked and o.getName() == 'bicycle':
                            self.count_bike_down.append(o)
                        self.objects.remove(o)
                if new == True:
                    obj = detectedObject(pid, name, cx_, cy_)
                    self.objects.append(obj)
            self.axes.plot([self.p1_x, width], [y2_, y1_], color='red')
            if self.detect_mod==1:
                text_1=""
                if self.person_checked:
                    text_1=text_1+'person:%s'%str(len(self.count_person_up))
                if self.car_checked:
                    text_1=text_1+'car:%s'%str(len(self.count_car_up))
                if self.bike_checked:
                    text_1=text_1+'bike:%s'%str(len(self.count_bike_up))
                self.axes.text(0, (y2_ - 20),text_1, fontsize=8, color='white',
                             bbox=dict(facecolor='red', alpha=0.5),
                             horizontalalignment='center', verticalalignment='center')
                text_2=""
                if self.person_checked:
                    text_1=text_1+'person:%s'%str(len(self.count_person_down))
                if self.car_checked:
                    text_1=text_1+'car:%s'%str(len(self.count_car_down))
                if self.bike_checked:
                    text_1=text_1+'bike:%s'%str(len(self.count_bike_down))
                self.axes.text(0, (y1_ + 20),text_2, fontsize=8, color='white',
                             bbox=dict(facecolor='green', alpha=0.5),
                             horizontalalignment='center', verticalalignment='center')
            else:
                text=""
                if self.person_checked:
                    text=text+'person:%s'%str(len(self.count_person_up)+len(self.count_person_down))
                if self.car_checked:
                    text_1=text+'car:%s'%str(len(self.count_car_up)+len(self.count_car_down))
                if self.bike_checked:
                    text_1=text+'bike:%s'%str(len(self.count_bike_up)+len(self.count_bike_down))
                self.axes.text(0, (y2_ - 20),text, fontsize=8, color='white',
                             bbox=dict(facecolor='red', alpha=0.5),
                             horizontalalignment='center', verticalalignment='center')
            self.axes.imshow(returned_frame, interpolation="none")
            self.figure.canvas.draw()
            self.figure.canvas.flush_events()
            self.figure.savefig(os.path.join(self.output_dir,'temp.jpg'))
            img = cv2.imread(os.path.join(self.output_dir,'temp.jpg'))
            self.videowriter.write(img)
        if frame_number % (self.frame_per_second*60) == 0:
            with open(os.path.join(self.output_dir, os.path.split(self.input_file)[-1][:-4] + '.csv'), 'a+') as f:
                f.write('%s,%s,%s,%s,%s' % ((frame_number // (self.frame_per_second*60)),len(self.count_person_up),
                                            len(self.count_person_down),len(self.count_car_up),len(self.count_car_down))+'\n')
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        main = MainDialogImgBW()
        main.show()
        sys.exit(app.exec_())
    except Exception as e:
        QMessageBox.information(QWidget(), "Warning", "Error:%s" % e)