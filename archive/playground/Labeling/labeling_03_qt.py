import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QPushButton, QVBoxLayout, QWidget

class LabelingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 主窗口设置
        self.setWindowTitle("Labeling Application")
        self.setGeometry(100, 100, 800, 600)

        # 创建中心窗口小部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 布局和部件
        layout = QVBoxLayout(central_widget)

        # 添加部件（例如标签、按钮、文本框等）
        self.question_label = QLabel("Question:", self)
        layout.addWidget(self.question_label)

        self.question_text = QTextEdit(self)
        layout.addWidget(self.question_text)

        self.next_button = QPushButton("下一题", self)
        self.next_button.clicked.connect(self.next_question)
        layout.addWidget(self.next_button)

        # 设置布局
        central_widget.setLayout(layout)

    def next_question(self):
        # 按钮点击事件处理函数
        pass

def main():
    app = QApplication(sys.argv)
    ex = LabelingApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
