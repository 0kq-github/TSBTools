from PySide2 import QtWidgets,QtGui
from PySide2.QtCore import QThread,Signal,Qt
from main_gui import Ui_MainWindow
from tsb.client import tsbAPI
from tsb.client import mojangAPI
import markdown
import os
import shutil
import requests


tsb = tsbAPI()
version = "0.1"
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.md = markdown.Markdown()
        os.makedirs(os.getcwd()+"\\download",exist_ok=True)
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"TSBTools v{version}")
        self.textBrowser.setText(self.md.convert("###リリース一覧を読み込み中..."))

        self.thread = load_tsb_releases(self)
        self.thread.signal.connect(self.show_tsb_releases)
        self.thread.start()

        #self.progressBar.setValue(0)
        title_md = f"""
<h1 style=\"text-align: center;\">
    TSBTools v{version}
</h1>
<h3 style=\"text-align: center;\">
    Tool created by 0kq 
    <br><br>
    <a href=\"https://twitter.com/_0kq_\">
        <img src=\"./twitter.png\" alt=\"Twitter\" width=32 height=26>
    </a> 
    <a href=\"https://github.com/0kq-github\">
        <img src=\"./github.png\" alt=\"GitHub\" width=32 height=32>
    </a>
    <br><br>
    <a href=\"https://tsb.scriptarts.jp/\">
        TSB公式サイト
    </a>
</h3>
"""
        self.label_2.setText(self.md.convert(title_md))

        self.pushButton.clicked.connect(self.detect_mc)
        self.pushButton_1.clicked.connect(self.install_client)
        self.toolButton.clicked.connect(self.select_mc)
    
    def show_tsb_releases(self,releases):
        r, tsb_md = releases
        self.textBrowser.setText(self.md.convert(tsb_md.replace("*","#### ・")))
        self.comboBox.addItems(r)

    def select_mc(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,".minecraftを開く")
        self.lineEdit.setText(path)
    
    def detect_mc(self):
        path = os.environ["appdata"] + "\\.minecraft"
        self.lineEdit.setText(path)

    def install_client(self):
        if not self.comboBox.currentText():
            QtWidgets.QMessageBox.information(self,"info","バージョンが選択されていません")
            return
        if not self.lineEdit.text():
            QtWidgets.QMessageBox.information(self,"info",".minecraftのパスが入力されていません")
            return
        download_url = tsb.releases[self.comboBox.currentText()]["download_url"]
        prog = QtWidgets.QProgressDialog(self)
        prog.setWindowModality(Qt.ApplicationModal)
        prog.setWindowTitle("ダウンロード中...")
        prog.show()
        file_size = tsb.releases[self.comboBox.currentText()]["size"] // 1024
        res = requests.get(download_url,stream=True)
        i = 0
        with open(os.getcwd()+"\\download\\TheSkyBlessing.zip","wb") as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)
                i += len(chunk)
                print(f"{i} / {file_size}")
                #prog.setValue(len(chunk) / file_size * 100)
        #QtWidgets.QMessageBox.information(self,"debug",download_url["download_url"])

class load_tsb_releases(QThread):
    signal = Signal(tuple)

    def run(self):
        md = markdown.Markdown()
        tsb_md = ""
        try:
            tsb.fetch_release()
            for v in tsb.releases.values():
                tsb_md += f"#{v['name']}\n{v['body']}\n"
        except Exception as e:
            tsb_md = "###リリース一覧の読み込みに失敗しました"
            print(e)
        self.signal.emit(([v for v in tsb.releases.keys()],md.convert(tsb_md.replace("*","#### ・")),))
        

class load_mc_versions(QThread):
    signal = Signal(dict)

    def run(self):
        mc = mojangAPI()
        try:
            releases = mc.fetch_release()
            self.signal.emit(releases)
        except:
            pass

# アプリの実行と終了
app = QtWidgets.QApplication()
window = MainWindow()
window.show()
app.exec_()