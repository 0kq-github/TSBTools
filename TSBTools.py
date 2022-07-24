from PySide2 import QtWidgets,QtGui
from PySide2.QtCore import QThread,Signal,Qt
from PySide2.QtGui import QPalette, QColor
from main_gui import Ui_MainWindow
from tsb.client import tsbAPI
from tsb.client import mojangAPI
import markdown
import os
import requests
import zipfile
import nbt2yaml
import json
import uuid
import datetime
import base64

tsb = tsbAPI()
version = "0.1"
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.md = markdown.Markdown()
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"TSBTools v{version}")
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(os.getcwd()+"\\assets\\tsb_icon.png")))
        self.textBrowser.setText(self.md.convert("###リリース一覧を読み込み中..."))

        self.thread = load_tsb_releases(self)
        self.thread.signal.connect(self.show_tsb_releases)
        self.thread.start()

        title_md = f"""
<h1 style=\"text-align: center;\">
    TSBTools v{version}
</h1>
<h3 style=\"text-align: center;\">
    Tool created by 0kq 
    <br><br>
    <a style=\"text-decoration:none;\" href=\"https://twitter.com/_0kq_\">
        <img src=\"{os.getcwd()}\\assets\\twitter.png\" alt=\"Twitter\" width=32 height=26>
    </a> 
    <a style=\"text-decoration:none;\" href=\"https://github.com/0kq-github\">
        <img src=\"{os.getcwd()}\\assets\\github.png\" alt=\"GitHub\" width=32 height=32>
    </a>
    <br><br>
    <a href=\"https://tsb.scriptarts.jp/\">
        TSB公式サイト
    </a>
</h3>
"""
        self.label_2.setText(self.md.convert(title_md))

        self.pushButton.clicked.connect(self.detect_mc)
        self.toolButton.clicked.connect(self.select_mc)
        self.pushButton_1.clicked.connect(self.install_client)
        
    
    def show_tsb_releases(self,releases):
        r, tsb_md = releases
        self.textBrowser.setText(self.md.convert(tsb_md.replace("*","#### ・")))
        self.comboBox.addItems(r)

    def select_mc(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,"ゲームディレクトリを開く")
        if path:
            self.lineEdit.setText(path)
    
    def detect_mc(self):
        path = os.environ["appdata"] + "\\.minecraft"
        self.lineEdit.setText(path)

    def install_client(self):
        if not self.check_input():
            return
        ret = QtWidgets.QMessageBox.information(self,"TSBTools","起動構成を作成しますか？",QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        self.install()
        if ret == QtWidgets.QMessageBox.Yes:
            self.create_profile()
        mcversion = self.check_world_version(self.lineEdit.text()+"\\saves\\"+f"TheSkyBlessing_{self.comboBox.currentText()}"+"\\level.dat")
        QtWidgets.QMessageBox.information(self,"TSBTools",f"のインストールが完了しました！\nTSB {self.comboBox.currentText()}\nMinecraft {mcversion}")

    def install(self):
        download_url = tsb.releases[self.comboBox.currentText()]["download_url"]
        prog = QtWidgets.QProgressDialog(self)
        prog.setWindowModality(Qt.ApplicationModal)
        prog.setWindowTitle("ダウンロード中...")
        prog.setFixedWidth(400)
        prog.setFixedHeight(100)
        prog.setValue(0)
        prog.show()
        file_size = tsb.releases[self.comboBox.currentText()]["size"]
        res = requests.get(download_url,stream=True)
        i = 0
        os.makedirs(os.getcwd()+"\\download",exist_ok=True)
        zip_path = os.getcwd()+f"\\download\\{self.comboBox.currentText()}.zip"
        with open(zip_path,"wb") as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)
                i += len(chunk)*(100 / file_size)
                prog.setValue(int(i))
        prog.close()
        prog = QtWidgets.QProgressDialog(self)
        prog.setWindowModality(Qt.ApplicationModal)
        prog.setWindowTitle("展開中...")
        prog.setFixedWidth(400)
        prog.setFixedHeight(100)
        prog.setValue(0)
        prog.show()
        i = 0
        with zipfile.ZipFile(zip_path) as zf:
            files = zf.namelist()
            prog.setMaximum(len(files))
            ext_path = self.lineEdit.text()+"\\saves\\"+f"TheSkyBlessing_{self.comboBox.currentText()}"
            for p in files:
                zf.extract(p,ext_path)
                i += 1
                prog.setValue(i)
                prog.setLabelText(p)
        prog.close()

    def check_world_version(self,nbt_path):
        with open(nbt_path,"rb") as f:
            nbt= nbt2yaml.parse_nbt(f)
            for n in nbt.data[0].data:
                if n.name == "Version":
                    for nm in n.data:
                        if nm.name == "Name":
                            return nm.data

    def check_input(self):
        if not self.comboBox.currentText():
            QtWidgets.QMessageBox.information(self,"TSBTools","バージョンが選択されていません")
            return False
        if not self.lineEdit.text():
            QtWidgets.QMessageBox.information(self,"TSBTools","ゲームディレクトリが指定されていません")
            return False
        return True

    def create_profile(self):
        if not self.check_input():
            return
        launcher_profiles = os.environ["appdata"]+"\\.minecraft\\launcher_profiles.json"
        profile_uuid = uuid.uuid4().hex
        mcversion = self.check_world_version(self.lineEdit.text()+"\\saves\\"+f"TheSkyBlessing_{self.comboBox.currentText()}"+"\\level.dat")
        with open(launcher_profiles,mode="r") as f:
            profiles = json.load(f)
            profiles["profiles"][profile_uuid] = {
                "created": datetime.datetime.utcnow().isoformat()+"Z",
                "gameDir": self.lineEdit.text(),
                "icon":"data:image/png;base64,"+base64.b64encode(open(os.getcwd()+"\\assets\\tsb_icon.png","rb").read()).decode("utf-8"),
                "javaArgs" : "-Xmx4G -Xms4G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M",
                "lastVersionId": mcversion,
                "name":"TheSkyBlessing "+self.comboBox.currentText(),
                "type":"custom"
            }
        with open(launcher_profiles,mode="w") as f:
            json.dump(profiles,f,indent=2)



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


app = QtWidgets.QApplication()

#ダークテーマ
"""
app.setStyle("Windows")
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.black)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)
"""

window = MainWindow()
window.show()
app.exec_()