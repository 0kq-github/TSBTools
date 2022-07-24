from PySide2 import QtWidgets,QtGui
from PySide2.QtCore import QThread,Signal,Qt
from PySide2.QtGui import QPalette, QColor
from main_ui import Ui_MainWindow
from server_ui import Ui_Dialog
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
import shutil

tsb = tsbAPI()
version = "0.1.1"
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.md = markdown.Markdown()
        super().__init__()
        self.setupUi(self)
        self
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
        self.pushButton_3.clicked.connect(self.create_server)
        
    
    def show_tsb_releases(self,releases):
        r, tsb_md = releases
        self.textBrowser.setText(self.md.convert(tsb_md.replace("*","#### ・")))
        self.comboBox.addItems(r)
        self.releases = r

    def select_mc(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,"ゲームディレクトリを開く",self.lineEdit.text())
        if path:
            self.lineEdit.setText(path)
    
    def detect_mc(self):
        path = os.environ["appdata"] + "\\.minecraft"
        self.lineEdit.setText(path)

    def install_client(self):
        title = "TSBTools"
        install_path = self.lineEdit.text()+"\\saves"
        if not self.check_input():
            return
        if os.path.exists(install_path+f"\\TheSkyBlessing_{self.comboBox.currentText()}"):
            ret = QtWidgets.QMessageBox.information(self,title,"ワールドが既に存在します。上書きしますか？",QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
            if not (ret == QtWidgets.QMessageBox.Yes):
                return
        ret = QtWidgets.QMessageBox.information(self,title,"起動構成を作成しますか？",QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        os.makedirs(install_path,exist_ok=True)
        self.install(install_path,self.comboBox.currentText())
        if not os.path.exists(install_path+f"\\TheSkyBlessing_{self.comboBox.currentText()}\\level.dat"):
            file_list = os.listdir(os.listdir(install_path+f"\\TheSkyBlessing_{self.comboBox.currentText()}\\TheSkyBlessing"))
            for file in file_list:
                shutil.move(file,f"\\TheSkyBlessing_{self.comboBox.currentText()}")
            os.rmdir(f"\\TheSkyBlessing_{self.comboBox.currentText()}\\TheSKyBlessing")
        if ret == QtWidgets.QMessageBox.Yes:
            self.create_profile()
        mcversion = self.check_world_version(install_path+f"\\TheSkyBlessing_{self.comboBox.currentText()}"+"\\level.dat")
        QtWidgets.QMessageBox.information(self,title,f"インストールが完了しました！\nTSB {self.comboBox.currentText()}\nMinecraft {mcversion}")

    def install(self,path,ver,parent=None):
        download_url = tsb.releases[ver]["download_url"]
        if parent:
            prog = QtWidgets.QProgressDialog(parent)
        else:
            prog = QtWidgets.QProgressDialog(self)
        prog.setWindowModality(Qt.ApplicationModal)
        prog.setWindowTitle("TSBTools")
        prog.setLabelText("TheSkyBlessing "+ver+"をダウンロード中...")
        prog.setFixedWidth(400)
        prog.setFixedHeight(100)
        prog.setValue(0)
        prog.setCancelButton(None)
        prog.setWindowFlags(Qt.Window)
        file_size = tsb.releases[ver]["size"]
        prog.setMaximum(file_size)
        prog.show()
        res = requests.get(download_url,stream=True)
        i = 0
        os.makedirs(os.getcwd()+"\\download",exist_ok=True)
        zip_path = os.getcwd()+f"\\download\\{ver}.zip"
        with open(zip_path,"wb") as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)
                i += len(chunk)
                prog.setValue(i)
        prog.close()
        if parent:
            prog = QtWidgets.QProgressDialog(parent)
        else:
            prog = QtWidgets.QProgressDialog(self)
        prog.setWindowModality(Qt.ApplicationModal)
        prog.setWindowTitle("TSBTools")
        prog.setFixedWidth(400)
        prog.setFixedHeight(100)
        prog.setValue(0)
        prog.setCancelButton(None)
        prog.setWindowFlags(Qt.Window)
        prog.show()
        i = 0
        with zipfile.ZipFile(zip_path) as zf:
            files = zf.namelist()
            prog.setMaximum(len(files))
            ext_path = f"{path}\\TheSkyBlessing_{ver}"
            for p in files:
                zf.extract(p,ext_path)
                i += 1
                prog.setValue(i)
                prog.setLabelText("展開中:\n"+p)
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

    def create_server(self):
        self.server_ui = server_ui()
        self.server_ui.setWindowTitle("サーバーを作成")
        self.server_ui.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(os.getcwd()+"\\assets\\tsb_icon.png")))
        if self.comboBox.currentText():
            self.server_ui.comboBox.addItems(self.releases)
            self.server_ui.comboBox.setCurrentText(self.comboBox.currentText())
        self.server_ui.toolButton.clicked.connect(self.select_server)
        self.server_ui.pushButton.clicked.connect(self.install_server)
        self.server_ui.exec_()

    def select_server(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self.server_ui,"サーバーの作成先を開く",self.server_ui.lineEdit.text())
        if path:
            self.server_ui.lineEdit.setText(path)

    def install_server(self):
        title = "サーバーを作成"
        if not self.server_ui.lineEdit.text():
            QtWidgets.QMessageBox.information(self.server_ui,title,"インストール先が指定されていません")
            return
        if not self.server_ui.checkBox.isChecked():
            QtWidgets.QMessageBox.information(self.server_ui,title,"EULAに同意してください")
            return
        if not self.server_ui.comboBox.currentText():
            QtWidgets.QMessageBox.information(self.server_ui,title,"バージョンが選択されていません")
            return
        install_path = self.server_ui.lineEdit.text()+f"\\TheSkyBlessingServer_{self.server_ui.comboBox.currentText()}"
        if os.path.exists(install_path):
            ret = QtWidgets.QMessageBox.information(self,title,"サーバーが既に存在します。上書きしますか？",QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
            if not (ret == QtWidgets.QMessageBox.Yes):
                return
        os.makedirs(install_path,exist_ok=True)
        self.install(install_path,self.server_ui.comboBox.currentText(),parent=self.server_ui)
        mcversion = self.check_world_version(install_path+f"\\TheSkyBlessing_{self.server_ui.comboBox.currentText()}\\level.dat")
        mc = mojangAPI()
        mc_releases = mc.fetch_release()
        download_url = mc_releases[mcversion]
        prog = QtWidgets.QProgressDialog(self.server_ui)
        prog.setWindowModality(Qt.ApplicationModal)
        prog.setWindowTitle("TSBTools")
        prog.setLabelText("server.jarをダウンロード中...")
        prog.setCancelButton(None)
        prog.setFixedWidth(400)
        prog.setFixedHeight(100)
        prog.setValue(0)
        file_size = int(requests.head(download_url).headers["Content-Length"])
        prog.setMaximum(file_size)
        prog.show()
        jar_path = install_path+"\\server.jar"
        res = requests.get(download_url,stream=True)
        i = 0

        with open(jar_path,"wb") as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)
                i += len(chunk)
                prog.setValue(i)
        prog.close()

        with open(install_path+"\\server.properties",mode="w") as f:
            server_properties = f"""resource-pack=https://github.com/ProjectTSB/TSB-ResourcePack/releases/download/{self.server_ui.comboBox.currentText()}/resources.zip
gamemode=adventure
difficulty=normal
server-port={self.server_ui.spinBox.value()}
max-players={self.server_ui.spinBox_3.value()}
motd={self.server_ui.textEdit.toPlainText() % (self.server_ui.comboBox.currentText(),mcversion)}
level-name=TheSkyBlessing_{self.server_ui.comboBox.currentText()}"""
            f.write(server_properties)

        with open(install_path+"\\eula.txt",mode="w") as f:
            f.write("eula=true")

        with open(install_path+"\\start.bat",mode="w",encoding="shift-jis") as f:
            start_bat = f"""@echo off
title TheSkyBlessing {self.server_ui.comboBox.currentText()} - {mcversion}
java -Xmx{self.server_ui.spinBox_2.value()}G -Xms{self.server_ui.spinBox_2.value()}G -jar server.jar nogui
pause"""
            f.write(start_bat)
        QtWidgets.QMessageBox.information(self.server_ui,"TSBTools",f"サーバーの作成が完了しました！\nサーバー起動ファイル:\n{install_path}\\start.bat")


class server_ui(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.horizontalSlider.valueChanged.connect(self.sync_mem_to_box)
        self.spinBox_2.valueChanged.connect(self.sync_box_to_mem)
        self.horizontalSlider_2.valueChanged.connect(self.sync_player_to_box)
        self.spinBox_3.valueChanged.connect(self.sync_box_to_player)
    
    def sync_mem_to_box(self):
        value = self.horizontalSlider.value()
        self.spinBox_2.setValue(value)
    
    def sync_box_to_mem(self):
        value = self.spinBox_2.value()
        self.horizontalSlider.setValue(value)
    
    def sync_player_to_box(self):
        value = self.horizontalSlider_2.value()
        self.spinBox_3.setValue(value)
    
    def sync_box_to_player(self):
        value = self.spinBox_3.value()
        self.horizontalSlider_2.setValue(value)
    
    


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

QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
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