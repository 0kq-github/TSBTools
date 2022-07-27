from PySide6 import QtWidgets,QtGui
from PySide6.QtCore import QThread,Signal,Qt,QByteArray
from PySide6.QtGui import QPalette, QColor
from main_ui import Ui_MainWindow
from server_ui import Ui_Dialog
import qdarktheme
from tsb.client import tsbAPI
from tsb.client import mojangAPI
from tsb import icons
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
import re

tsb = tsbAPI()
version = "0.1.1"
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.md = markdown.Markdown()
        super().__init__()
        self.setupUi(self)
        #self.pushButton_exit.clicked.connect(self.close)
        #self.pushButton_exit.setStyleSheet('QPushButton {color: white; font-size: 18px;}')
        #self.label_icon.setText(f"<img src=\"data:image/png;base64,{icons.tsb}\" width=21 height=21>")
        self.setWindowTitle(f"TSBTools v{version}")
        icon = QtGui.QPixmap()
        icon.loadFromData(QByteArray.fromBase64(bytes(icons.tsb,encoding="utf-8")))
        self.setWindowIcon(QtGui.QIcon(icon))
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
        <img src=\"data:image/png;base64,{icons.twitter}\" alt=\"Twitter\" width=32 height=26>
    </a> 
    <a style=\"text-decoration:none;\" href=\"https://github.com/0kq-github\">
        <img src=\"data:image/png;base64,{icons.github_light}\" alt=\"GitHub\" width=32 height=32>
    </a>
    <br><br>
    <a style=\"text-decoration:none; color:#6bb4f7;\" href=\"https://tsb.scriptarts.jp/\">
        TSB公式サイト
    </a>
</h3>
"""
        self.label_2.setText(self.md.convert(title_md))

        self.pushButton.clicked.connect(self.detect_mc)
        self.pushButton_4.clicked.connect(self.select_mc)
        self.pushButton_1.clicked.connect(self.install_client)
        self.pushButton_3.clicked.connect(self.create_server)

        self.saves_dir = os.environ["appdata"] + "\\.minecraft\\saves"
        self.lineEdit_2.setText(self.saves_dir)
        self.pushButton_11.clicked.connect(self.detect_saves)
        self.pushButton_2.clicked.connect(self.select_saves)
        self.load_levels()
        self.pushButton_12.clicked.connect(self.reload_levels)
        self.treeWidget.currentItemChanged.connect(self.detect_selection)

        self.pushButton_datapack_extract.clicked.connect(self.extract_datapack)
        self.pushButton_datapack_delete.clicked.connect(self.delete_datapack)
        #self.pushButton_level_extractall.clicked.connect()





    
    def show_tsb_releases(self,releases):
        r, tsb_md = releases
        self.textBrowser.setText(self.md.convert(tsb_md.replace("*","#### ・")))
        self.comboBox.addItems(r)
        self.releases = r

    def select_mc(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,"ゲームディレクトリを開く",self.lineEdit.text())
        if path:
            self.lineEdit.setText(path)
    
    def select_saves(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,"savesを開く",self.lineEdit_2.text())
        if path:
            self.lineEdit_2.setText(path)
    
    def detect_mc(self):
        path = os.environ["appdata"] + "\\.minecraft"
        self.lineEdit.setText(path)
    
    def detect_saves(self):
        path = os.environ["appdata"] + "\\.minecraft\\saves"
        self.lineEdit_2.setText(path)

    def install_client(self):
        title = "TSBTools"
        install_path = self.lineEdit.text()+"\\saves"
        if not self.check_input():
            return
        if os.path.exists(install_path+f"\\TheSkyBlessing_{self.comboBox.currentText()}"):
            ret = QtWidgets.QMessageBox.information(self,title,"ワールドが既に存在します。上書きしますか？\n(現在のワールドは削除されます！)",QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
            if not (ret == QtWidgets.QMessageBox.Yes):
                return
            shutil.rmtree(install_path+f"\\TheSkyBlessing_{self.comboBox.currentText()}")
        os.makedirs(install_path,exist_ok=True)
        self.install(install_path,self.comboBox.currentText())
        if self.checkBox.isChecked():
            self.create_profile()
        mcversion, levelname = self.get_world_info(install_path+f"\\TheSkyBlessing_{self.comboBox.currentText()}"+"\\level.dat")
        QtWidgets.QMessageBox.information(self,title,f"インストールが完了しました！\nTSB {self.comboBox.currentText()}\nMinecraft {mcversion}")
        self.reload_levels()

    def install(self,path,ver,parent=None):
        download_url = tsb.releases[ver]["download_url"]
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
        prog.setAutoClose(False)
        prog.show()
        zip_path = os.getcwd()+f"\\TSBTools\\download\\{ver}.zip"
        if (not os.path.exists(zip_path)) or (self.checkBox_2.isChecked()):
            prog.setLabelText("ダウンロード中:\n"+"TheSkyBlessing "+ver)
            file_size = tsb.releases[ver]["size"]
            prog.setMaximum(file_size)
            res = requests.get(download_url,stream=True)
            i = 0
            os.makedirs(os.getcwd()+"\\TSBTools\\download",exist_ok=True)
            with open(zip_path,"wb") as f:
                for chunk in res.iter_content(chunk_size=1024):
                    f.write(chunk)
                    i += len(chunk)
                    prog.setValue(i)
            prog.setValue(0)
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
        if not os.path.exists(path+f"\\TheSkyBlessing_{ver}\\level.dat"):
            file_list = os.listdir(os.listdir(path+f"\\TheSkyBlessing_{ver}\\TheSkyBlessing"))
            for file in file_list:
                shutil.move(file,f"\\TheSkyBlessing_{ver}")
            os.rmdir(f"\\TheSkyBlessing_{ver}\\TheSKyBlessing")
        prog.close()

    def get_world_info(self,nbt_path):
        """ワールドの情報を取得

        Args:
            nbt_path (str): level.dat

        Returns:
            list: [Version, LevelName]
        """
        result = [None,None]
        with open(nbt_path,"rb") as f:
            nbt = nbt2yaml.parse_nbt(f)
            for n in nbt.data[0].data:
                if n.name == "Version":
                    for nm in n.data:
                        if nm.name == "Name":
                            result[0] = (nm.data)
                if n.name == "LevelName":
                    result[1] = (n.data)
        return result

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
        mcversion,levelname = self.get_world_info(self.lineEdit.text()+"\\saves\\"+f"TheSkyBlessing_{self.comboBox.currentText()}"+"\\level.dat")
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
        icon = QtGui.QPixmap()
        icon.loadFromData(QByteArray.fromBase64(bytes(icons.tsb,encoding="utf-8")))
        self.server_ui.setWindowIcon(QtGui.QIcon(icon))
        if self.comboBox.currentText():
            self.server_ui.comboBox.addItems(self.releases)
            self.server_ui.comboBox.setCurrentText(self.comboBox.currentText())
        self.server_ui.toolButton.clicked.connect(self.select_server)
        self.server_ui.pushButton.clicked.connect(self.install_server)
        self.server_ui.exec()

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
        mcversion,levelname = self.get_world_info(install_path+f"\\TheSkyBlessing_{self.server_ui.comboBox.currentText()}\\level.dat")
        mc = mojangAPI()
        mc_releases = mc.fetch_release()
        download_url = mc_releases[mcversion]
        prog = QtWidgets.QProgressDialog(self.server_ui)
        prog.setWindowModality(Qt.ApplicationModal)
        prog.setWindowTitle("TSBTools")
        prog.setLabelText("ダウンロード中:\n"+"server.jar")
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

    def load_levels(self):
        saves_dir = self.saves_dir
        self.treeWidget.clear()
        if not os.path.exists(saves_dir):
            return
        for d in os.listdir(saves_dir):
            if os.path.isdir(saves_dir+"\\"+d):
                if not os.path.exists(saves_dir+"\\"+d+"\\level.dat"):
                    continue
                try:
                    mcversion,levelname = self.get_world_info(saves_dir+"\\"+d+"\\level.dat")
                except:
                    continue
                if levelname:
                    levelname = re.sub("§.","",levelname)
                else:
                    levelname = d
                if not mcversion:
                    mcversion = "バージョン不明"
                dir_tree = QtWidgets.QTreeWidgetItem([d,f"{levelname} ({mcversion})"])
                if os.path.exists(saves_dir+"\\"+d+"\\datapacks"):
                    datapacks = os.listdir(saves_dir+"\\"+d+"\\datapacks")
                    for dp in datapacks:
                        if dp.endswith(".zip"):
                            with zipfile.ZipFile(saves_dir+"\\"+d+"\\datapacks\\"+dp) as zf:
                                try:
                                    zf.extract("pack.mcmeta",os.getcwd()+"\\TSBTools\\temp")
                                except:
                                    continue
                                with open(os.getcwd()+"\\TSBTools\\temp\\pack.mcmeta",mode="r",encoding="utf-8_sig") as f:
                                    mcmeta = json.load(f)
                                    dir_tree.addChild(QtWidgets.QTreeWidgetItem([dp,mcmeta["pack"]["description"]]))
                        if os.path.isdir(saves_dir+"\\"+d+"\\datapacks\\"+dp):
                            try:
                                with open(saves_dir+"\\"+d+"\\datapacks\\"+dp+"\\pack.mcmeta",mode="r",encoding="utf-8_sig") as f:
                                    mcmeta = json.load(f)
                                    dir_tree.addChild(QtWidgets.QTreeWidgetItem([dp,mcmeta["pack"]["description"]]))
                            except:
                                continue
                self.treeWidget.addTopLevelItem(dir_tree)

    def reload_levels(self):
        self.load_levels()
        self.detect_selection()

    def detect_selection(self):
        current = self.treeWidget.currentItem()
        if current:
            parent = self.treeWidget.currentItem().parent()
            if parent:
                self.selected_level = parent.text(0)
                self.selected_datapack = current.text(0)
                self.set_level_buttons(True)
                self.set_datapack_buttons(True)
            else:
                self.selected_level = current.text(0)
                self.selected_datapack = None
                self.set_level_buttons(True)
                self.set_datapack_buttons(False)
        else:
            self.selected_level = None
            self.selected_datapack = None
            self.set_level_buttons(False)
            self.set_datapack_buttons(False)

    def set_level_buttons(self,enable):
        self.pushButton_level_update.setEnabled(enable)
        self.pushButton_level_vscode.setEnabled(enable)
        self.pushButton_level_explorer.setEnabled(enable)
        self.pushButton_level_extractall.setEnabled(enable)
        self.pushButton_datapack_update.setEnabled(enable)
        self.pushButton_datapack_add.setEnabled(enable)

    def set_datapack_buttons(self,enable):
        self.pushButton_datapack_delete.setEnabled(enable)
        self.pushButton_datapack_extract.setEnabled(enable)

    def extract_datapack(self):
        target = self.lineEdit_2.text()+"\\"+self.selected_level+"\\datapacks\\"+self.selected_datapack
        if os.path.isdir(target):
            QtWidgets.QMessageBox.information(self,"TSBTools","選択されているデータパックは圧縮されていません")
            return
        prog = QtWidgets.QProgressDialog(self)
        prog.setWindowTitle("TSBTools")
        prog.setFixedWidth(400)
        prog.setFixedHeight(100)
        prog.setValue(0)
        prog.setCancelButton(None)
        prog.setWindowFlags(Qt.Window)
        prog.setAutoClose(False)
        prog.show()
        i = 0
        with zipfile.ZipFile(target) as zf:
            files = zf.namelist()
            prog.setMaximum(len(files))
            ext_path = target[:-4]
            for p in files:
                zf.extract(p,ext_path)
                i += 1
                prog.setValue(i)
                prog.setLabelText("展開中:\n"+p)
        os.remove(target)
        prog.close()
        QtWidgets.QMessageBox.information(self,"TSBTools","展開が完了しました！\n"+target)
        for item in self.treeWidget.selectedItems():
            if item.text(0) == self.selected_datapack:
                with open(target[:-4]+"\\pack.mcmeta",mode="r",encoding="utf-8_sig") as f:
                    mcmeta = json.load(f)
                    item.parent().addChild(QtWidgets.QTreeWidgetItem([self.selected_datapack[:-4],mcmeta["pack"]["description"]]))
                item.parent().removeChild(item)


    def delete_datapack(self):
        target = self.lineEdit_2.text()+"\\"+self.selected_level+"\\datapacks\\"+self.selected_datapack
        ret = QtWidgets.QMessageBox.information(self,"TSBTools","本当に削除しますか？",QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if not (ret == QtWidgets.QMessageBox.Yes):
            return
        if os.path.isdir(target):
            shutil.rmtree(target)
        else:
            os.remove(target)
        for item in self.treeWidget.selectedItems():
            if item.text(0) == self.selected_datapack:
                item.parent().removeChild(item)


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

class load_levels(QThread):
    signal = Signal(list)
    

class load_mc_versions(QThread):
    signal = Signal(dict)

    def run(self):
        mc = mojangAPI()
        try:
            releases = mc.fetch_release()
            self.signal.emit(releases)
        except:
            pass


if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication()

    #ダークテーマ
    app.setStyleSheet(qdarktheme.load_stylesheet())

    window = MainWindow()
    #window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()
    app.exec()