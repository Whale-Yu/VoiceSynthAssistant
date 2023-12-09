import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, \
    QSpinBox, QTextEdit, QPushButton, QVBoxLayout, QWidget, QScrollArea, \
    QPlainTextEdit, QHBoxLayout, QLineEdit, QFileDialog, QMessageBox
from qt_material import apply_stylesheet

from tts import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        '''
        设置状态栏
        '''
        # 创建状态栏
        self.statusBar = self.statusBar()
        # 设置版本号和作者信息
        version = "2023.V1.0"  # 替换为实际的版本号
        author = "作者：鲸鱼工作室"  # 替换为实际的作者名字
        self.statusBar.showMessage(f"版本号：{version}")
        # 创建作者信息标签
        author_label = QLabel(author)
        author_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 设置标签靠右对齐
        # 将作者信息标签添加为状态栏的永久部件
        self.statusBar.addPermanentWidget(author_label)

        # 初始值
        self.save_path = ''

        self.setWindowTitle("语音合成助手")
        self.setGeometry(100, 100, 400, 600)  # 调整窗口大小为800x600

        # 创建文本输入框
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(40, 40, 720, 200)  # 调整文本输入框的尺寸和位置
        self.text_edit.setPlaceholderText("请输入或粘贴需要合成的文本")

        # 创建名称下拉框
        self.name_label = QLabel("支持声音列表:", self)
        self.name_label.setGeometry(40, 280, 80, 30)  # 调整名称标签的位置
        self.name_combo = QComboBox(self)
        self.name_combo.setGeometry(140, 280, 600, 30)  # 调整名称下拉框的尺寸和位置
        self.name_combo.addItem("01-女：zh-HK-HiuGaaiNeural")
        self.name_combo.addItem("02-女：zh-HK-HiuMaanNeural")
        self.name_combo.addItem("03-男：zh-HK-WanLungNeural")
        self.name_combo.addItem("04-女：zh-CN-XiaoxiaoNeural")
        self.name_combo.addItem("05-女：zh-CN-XiaoyiNeural")
        self.name_combo.addItem("06-男：zh-CN-YunjianNeural")
        self.name_combo.addItem("07-男：zh-CN-YunxiNeural")
        self.name_combo.addItem("08-男：zh-CN-YunxiaNeural")
        self.name_combo.addItem("09-男：zh-CN-YunyangNeural")
        self.name_combo.addItem("10-女：zh-CN-liaoning-XiaobeiNeural")
        self.name_combo.addItem("11-女：zh-TW-HsiaoChenNeural")
        self.name_combo.addItem("12-男：zh-TW-YunJheNeural")
        self.name_combo.addItem("13-女：zh-TW-HsiaoYuNeural")
        self.name_combo.addItem("14-女：h-CN-shaanxi-XiaoniNeural")
        # 添加更多的名称选项...

        # 创建语速微调器
        self.rate_label = QLabel("速度:", self)
        self.rate_label.setGeometry(40, 340, 80, 30)  # 调整语速标签的位置
        self.rate_spinbox = QSpinBox(self)
        self.rate_spinbox.setGeometry(140, 340, 600, 30)  # 调整语速微调器的尺寸和位置
        self.rate_spinbox.setRange(0, 100)
        self.rate_spinbox.setValue(0)

        # 创建音调微调器
        self.pitch_label = QLabel("语调:", self)
        self.pitch_label.setGeometry(40, 400, 80, 30)  # 调整音调标签的位置
        self.pitch_spinbox = QSpinBox(self)
        self.pitch_spinbox.setGeometry(140, 400, 600, 30)  # 调整音调微调器的尺寸和位置
        self.pitch_spinbox.setRange(0, 100)
        self.pitch_spinbox.setValue(0)

        # 创建选择路径
        path_layout = QHBoxLayout()
        self.save_path_label = QLabel("音频保存路径:", self)
        self.select_path_button = QPushButton("选择路径", self)
        self.select_path_button.clicked.connect(self.select_output_path)
        # 将选择路径按钮和文件名输入框放在同一行
        path_layout.addWidget(self.save_path_label)
        path_layout.addWidget(self.select_path_button)

        # 创建文件名输入框
        self.filename_label = QLabel("音频文件名(无需加后缀名):", self)
        self.filename_edit = QLineEdit(self)
        self.filename_edit.setPlaceholderText("请输入音频文件名，如test")
        # 将选择路径按钮和文件名输入框放在同一行
        filename_layout = QHBoxLayout()
        filename_layout.addWidget(self.filename_label)
        filename_layout.addWidget(self.filename_edit)

        # 创建状态标签
        self.status_label = QLabel("", self)
        self.status_label.setGeometry(40, 520, 700, 20)  # 调整状态标签的尺寸和位置

        # 创建控制台
        self.console = QPlainTextEdit(self)
        self.console.setGeometry(40, 500, 700, 80)  # 调整控制台的尺寸和位置
        self.console.setReadOnly(True)  # 设置控制台为只读模式

        # 创建生成按钮
        self.generate_button = QPushButton("开始生成语音", self)
        self.generate_button.clicked.connect(self.generate_speech)

        # 创建垂直布局
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_combo)
        layout.addWidget(self.rate_label)
        layout.addWidget(self.rate_spinbox)
        layout.addWidget(self.pitch_label)
        layout.addWidget(self.pitch_spinbox)
        layout.addLayout(path_layout)  # 将标签和按钮放在同一行
        layout.addLayout(filename_layout)  # 将选择路径按钮和文件名输入框放在同一行
        layout.addWidget(self.filename_edit)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.console)
        layout.addWidget(self.status_label)

        # 创建主部件和滚动区域
        main_widget = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidget(main_widget)
        scroll_area.setWidgetResizable(True)
        main_widget.setLayout(layout)

        # 设置主窗口的中心部件为滚动区域
        self.setCentralWidget(scroll_area)

    def generate_speech(self):
        text = self.text_edit.toPlainText().strip()
        name = self.name_combo.currentText().split('：')[-1]
        rate = self.rate_spinbox.value()
        pitch = self.pitch_spinbox.value()
        filename = self.filename_edit.text()

        if text == '' or filename == '' or self.save_path == '':
            # 弹出警告
            QMessageBox.warning(self, '警告', '请检查【文本】或【选择路径】或【文件名】是否为空')
        else:
            # 将文件名和输出路径组合以生成完整的文件路径
            # 输出生成语音的相关信息到控制台
            self.console.appendPlainText(f"文本: {text}")
            self.console.appendPlainText(f"声音：'{name}':")
            self.console.appendPlainText(f"速度: {rate}%")
            self.console.appendPlainText(f"语调: {pitch}%")

            # 调用生成语音的代码
            self.console.appendPlainText(f"【{now_time()}】开始生成语音.... 请耐心等待....")
            rate = f'{rate}%'
            pitch = f'{pitch}%'
            SSML_text = get_SSML(name=name, rate=rate, pitch=pitch, text=text)
            output_path = self.save_path + '/' + filename
            asyncio.get_event_loop().run_until_complete(mainSeq(SSML_text, output_path))
            self.console.appendPlainText(f"【{now_time()}】语音生成成功！音频文件保存至：{output_path}.mp3")
            self.console.appendPlainText("\n")

    def select_output_path(self):
        print('选择路径')
        self.save_path = QFileDialog.getExistingDirectory(self, '选择保存路径', '.')
        # 弹窗表示选择路径成功
        QMessageBox.information(self, '提示', '已设置保存路径')
        self.console.appendPlainText('音频保存路径为：{}'.format(self.save_path))


if __name__ == '__main__':
    # 创建应用程序实例
    app = QApplication(sys.argv)

    theme_list = ['dark_amber.xml',
                  'dark_blue.xml',
                  'dark_cyan.xml',
                  'dark_lightgreen.xml',
                  'dark_pink.xml',
                  'dark_purple.xml',
                  'dark_red.xml',
                  'dark_teal.xml',
                  'dark_yellow.xml',
                  'light_amber.xml',
                  'light_blue.xml',
                  'light_cyan.xml',
                  'light_cyan_500.xml',
                  'light_lightgreen.xml',
                  'light_pink.xml',
                  'light_purple.xml',
                  'light_red.xml',
                  'light_teal.xml',
                  'light_yellow.xml']
    apply_stylesheet(app, theme='dark_cyan.xml')

    # 创建主窗口
    window = MainWindow()
    window.show()

    # 创建图标对象
    icon = QIcon("voice.png")  # 将 "path_to_icon_file.ico" 替换为实际的图标文件路径
    # 设置应用程序的图标
    app.setWindowIcon(icon)

    # 运行应用程序
    sys.exit(app.exec())
