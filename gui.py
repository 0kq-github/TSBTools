from PySide2 import QtWidgets


# ウィンドウの見た目と各機能（今はウィンドウだけ）
version = "0.1"
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"TSBTools v{version}")


# アプリの実行と終了
app = QtWidgets.QApplication()
window = MainWindow()
window.show()
app.exec_()