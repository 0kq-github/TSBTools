from PySide6 import QtWidgets,QtGui
from PySide6.QtCore import QThread,Signal,Qt,QByteArray,QObject,Signal
from PySide6.QtGui import QPalette, QColor
from main_ui import Ui_MainWindow
from server_ui import Ui_Dialog as server_dialog
from tsbupdater_ui import Ui_Dialog as updater_dialog
from datapack_manager import Ui_Dialog as datapack_dialog
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
from threading import Thread
from pypresence import Presence
import time
import sys
import logging
import datetime
import subprocess
from git import Repo

tsb = tsbAPI()
version = "0.1.6"


log = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
log.addHandler(handler)

def show_exception_box(log_msg):
    """Checks if a QApplication instance is available and shows a messagebox with the exception message. 
    If unavailable (non-console application), log an additional notice.
    """
    if QtWidgets.QApplication.instance() is not None:
            errorbox = QtWidgets.QMessageBox()
            errorbox.critical(None,"TSBTools",log_msg)
    else:
        log.debug("No QApplication instance available.")
 
class UncaughtHook(QObject):
    _exception_caught = Signal(object)
 
    def __init__(self, *args, **kwargs):
        super(UncaughtHook, self).__init__(*args, **kwargs)

        # this registers the exception_hook() function as hook with the Python interpreter
        sys.excepthook = self.exception_hook

        # connect signal to execute the message box function always on main thread
        self._exception_caught.connect(show_exception_box)
 
    def exception_hook(self, exc_type, exc_value, exc_traceback):
        """Function handling uncaught exceptions.
        It is triggered each time an uncaught exception occurs. 
        """
        if issubclass(exc_type, KeyboardInterrupt):
            # ignore keyboard interrupt to support console applications
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
        else:
            #exc_info = (exc_type, exc_value, exc_traceback)
            log_msg = f"例外が発生しました: \n{exc_value}"
            #'\n'.join([''.join(traceback.format_tb(exc_traceback)),'{0}: {1}'.format(exc_type.__name__, exc_value)])
            #log.critical("Uncaught exception:\n {0}".format(log_msg), exc_info=exc_info)

            # trigger message box show
            self._exception_caught.emit(log_msg)



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

        self.__thread_0 = load_tsb_releases()
        self.__thread_0.signal.connect(self.show_tsb_releases)
        self.__thread_0.start()

        self.pushButton_level_add.setEnabled(True)

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
        #self.load_levels()
        self.pushButton_12.clicked.connect(self.reload_levels)
        self.treeWidget.currentItemChanged.connect(self.detect_selection)

        self.pushButton_datapack_extract.clicked.connect(self.extract_datapack)
        self.pushButton_datapack_delete.clicked.connect(self.delete_datapack)
        self.pushButton_datapack_add.clicked.connect(self.add_datapack)
        self.pushButton_level_extractall.clicked.connect(self.extract_all_datapacks)
        self.pushButton_datapack_update.clicked.connect(self.update_datapack)
        self.pushButton_datapack_commit.clicked.connect(self.commit_datapack)

        self.pushButton_level_explorer.clicked.connect(self.open_explorer)
        self.pushButton_level_vscode.clicked.connect(self.open_vscode)

        self.pushButton_level_add.clicked.connect(self.add_level)
        self.pushButton_level_delete.clicked.connect(self.delete_level)

        self.tabWidget.currentChanged.connect(self.update_levels)

    def update_levels(self,i):
        if i == 1:
            if self.treeWidget.topLevelItemCount() == 0:
                self.load_levels()


    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.isAutoRepeat():
            return
        key = QtGui.QKeySequence(event.key()).toString(QtGui.QKeySequence.NativeText)
        self.lastPressedKey = key
        #return super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.isAutoRepeat():
            return
        key = QtGui.QKeySequence(event.key()).toString(QtGui.QKeySequence.NativeText)
        self.lastReleasedKey = key

        """
        if (key == "Del") and self.treeWidget.currentItem():
            try:
                path = self.lineEdit_2.text() + "\\datapacks\\" + self.treeWidget.currentItem().text(0)
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
            except:
                shutil.rmtree(self.lineEdit_2.text() + "\\" + self.treeWidget.currentItem().text(0))
            self.reload_levels()
        """
        #return super().keyReleaseEvent(event)





    
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
            self.saves_dir = path
            self.reload_levels()
    
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
        prog.setWindowTitle(self.windowTitle())
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
            #for info in zf.infolist():
            #    if os.sep != "/" and os.sep in info.filename:
            #        info.filename = info.filename.replace(os.sep, "/")
            files = zf.infolist()
            prog.setMaximum(len(files))
            ext_path = f"{path}\\TheSkyBlessing_{ver}"
            for p in files:
                encoding = "utf-8" if p.flag_bits & 0x800 else "cp437"
                try:
                    p.filename = p.orig_filename.encode(encoding).decode('cp932')
                except:
                    p.filename = p.orig_filename
                if os.sep != "/" and os.sep in p.filename:
                    p.filename = p.filename.replace(os.sep, "/")
                zf.extract(p,ext_path)
                i += 1
                prog.setValue(i)
                prog.setLabelText("展開中:\n"+p.filename)
        if not os.path.exists(f"{path}\\TheSkyBlessing_{ver}\\level.dat"):
            shutil.copytree(f"{path}\\TheSkyBlessing_{ver}\\TheSkyBlessing",f"{path}\\TheSkyBlessing_{ver}",dirs_exist_ok=True)
            shutil.rmtree(f"{path}\\TheSkyBlessing_{ver}\\TheSKyBlessing",ignore_errors=True)
            #os.rmdir(f"{path}\\TheSkyBlessing_{ver}\\TheSKyBlessing")
        with open(f"{path}\\TheSkyBlessing_{ver}\\version.txt",mode="w",encoding="utf-8") as f:
            f.write(ver)
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
                            if nm.data[-1] == "X":
                                for v in mojangAPI().fetch_release().keys():
                                    if v.startswith(nm.data[:-2]):
                                        result[0] = v
                                        break
                            else:
                                result[0] = nm.data
                if n.name == "LevelName":
                    result[1] = n.data
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
        prog.setWindowTitle(self.windowTitle())
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

    def _load_levels(self):
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
    
    def load_levels(self):
        self.treeWidget.clear()
        self.__thread_1 = load_levels(self.saves_dir,self.treeWidget,self.get_world_info)
        self.__thread_1.start()


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
        self.pushButton_datapack_commit.setEnabled(enable)
        self.pushButton_level_explorer.setEnabled(enable)
        self.pushButton_level_extractall.setEnabled(enable)
        #self.pushButton_level_add.setEnabled(enable)
        self.pushButton_level_delete.setEnabled(enable)
        self.pushButton_level_vscode.setEnabled(enable)
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
        prog.setWindowModality(Qt.ApplicationModal)
        prog.setWindowTitle(self.windowTitle())
        prog.setFixedWidth(400)
        prog.setFixedHeight(100)
        prog.setValue(0)
        prog.setMinimum(0)
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

    def _add_datapack(self):
        datapacks_path = self.lineEdit_2.text()+"\\"+self.selected_level+"\\datapacks"
        path,filter = QtWidgets.QFileDialog.getOpenFileName(self,"追加するデータパックを選ぶ",filter="圧縮ファイル (*.zip)")
        if not path:
            return
        os.makedirs(datapacks_path,exist_ok=True)
        shutil.copy(path,datapacks_path)
        self.reload_levels()

    def add_datapack(self):
        datapacks_path = self.lineEdit_2.text()+"\\"+self.selected_level+"\\datapacks"
        self.datapack_ui = datapack_ui()
        self.datapack_ui.setWindowIcon(self.windowIcon())
        self.datapack_ui.setWindowTitle(self.windowTitle())
        self.datapack_ui.fetch_repo()
        self.datapack_ui.exec()


    def extract_all_datapacks(self):
        datapacks_path = self.lineEdit_2.text()+"\\"+self.selected_level+"\\datapacks"
        parent = self.treeWidget.selectedItems()[0].parent()
        datapacks = []
        if not parent:
            parent = self.treeWidget.selectedItems()[0]
        for c in range(parent.childCount()):
            datapacks.append(parent.child(c).text(0))
        prog = QtWidgets.QProgressDialog(self)
        prog.setWindowModality(Qt.ApplicationModal)
        prog.setWindowTitle(self.windowTitle())
        prog.setFixedWidth(400)
        prog.setFixedHeight(100)
        prog.setValue(0)
        prog.setMinimum(0)
        prog.setCancelButton(None)
        prog.setWindowFlags(Qt.Window)
        prog.setAutoClose(False)
        prog.show()
        for d in datapacks:
            i = 0
            target = datapacks_path + "\\" + d
            try:
                with zipfile.ZipFile(target) as zf:
                    files = zf.namelist()
                    prog.setMaximum(len(files))
                    ext_path = target[:-4]
                    for p in files:
                        zf.extract(p,ext_path)
                        i += 1
                        prog.setValue(i)
                        prog.setLabelText("展開中:"+ d +"\n"+p)
                os.remove(target)
            except:
                continue
        prog.close()
        QtWidgets.QMessageBox.information(self,"TSBTools","展開が完了しました！\n"+"\n".join(datapacks))
        self.reload_levels()

    def update_datapack(self):
        level_path = self.lineEdit_2.text()+"\\"+self.selected_level
        if os.path.exists(level_path+"\\version.txt"):
            with open(level_path+"\\version.txt",mode="r",encoding="utf-8") as f:
                ver = f.read()
        else:
            ver = "不明"
        datapack_list = []
        for k,v in tsb.releases.items():
            if v["datapack"]:
                datapack_list.append(k)
        self.updater_ui = updater_ui()
        #icon = QtGui.QPixmap()
        #icon.loadFromData(QByteArray.fromBase64(bytes(icons.tsb,encoding="utf-8")))
        #self.updater_ui.setWindowIcon(QtGui.QIcon(icon))
        self.updater_ui.setWindowIcon(self.windowIcon())
        self.updater_ui.setWindowTitle(self.windowTitle())
        mc_version,name = self.get_world_info(level_path+"\\level.dat")
        label_text = f"""<p align=\"center\">インストール済みのTSBのバージョン: {ver}</p>
<p align=\"center\">Minecraftのバージョン: {mc_version}</p>
"""
        self.updater_ui.label.setText(label_text)
        for v in datapack_list:
            if ver == "不明":
                self.updater_ui.listWidget.addItem("❌ "+v)
            elif ver.split(".")[1] == v.split(".")[1] and int(ver.split(".")[-1]) <= int(v.split(".")[-1]):
                self.updater_ui.listWidget.addItem("✅ "+v)
            else:
                self.updater_ui.listWidget.addItem("❌ "+v)
        self.updater_ui.pushButton.clicked.connect(self._update_datapack)
        self.updater_ui.exec()
        
    def _update_datapack(self):
        if self.updater_ui.listWidget.selectedItems()[0].text().startswith("❌"):
            ret = QtWidgets.QMessageBox.information(self.updater_ui,"TSBTools","互換性のないバージョンです。それでもアップデートを行いますか？",QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
            if not (ret == QtWidgets.QMessageBox.Yes):
                return
        level_path = self.lineEdit_2.text()+"\\"+self.selected_level
        if self.updater_ui.checkBox_2.isChecked():
            shutil.copytree(level_path,level_path+"_backup_"+datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        ver = self.updater_ui.listWidget.selectedItems()[0].text().replace("❌ ","").replace("✅ ","")
        download_url = tsb.get_release()[ver]["datapack"]
        prog = QtWidgets.QProgressDialog(self.updater_ui)
        prog.setWindowModality(Qt.ApplicationModal)
        prog.setWindowTitle(self.windowTitle())
        prog.setFixedWidth(400)
        prog.setFixedHeight(100)
        prog.setValue(0)
        prog.setCancelButton(None)
        prog.setWindowFlags(Qt.Window)
        prog.setAutoClose(False)
        prog.show()
        prog.setLabelText("ダウンロード中:\n"+"TheSkyBlessing "+ver)
        file_size = tsb.get_release()[ver]["datapack_size"]
        prog.setMaximum(file_size)
        res = requests.get(download_url,stream=True)
        i = 0
        os.makedirs(os.getcwd()+"\\TSBTools\\download",exist_ok=True)
        zip_path = os.getcwd()+f"\\TSBTools\\download\\datapack_{ver}.zip"
        with open(zip_path,"wb") as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)
                i += len(chunk)
                prog.setValue(i)
        i = 0
        with zipfile.ZipFile(zip_path) as zf: 
            files = zf.infolist()
            prog.setMaximum(len(files))
            shutil.rmtree(level_path+"\\datapacks")
            os.makedirs(level_path+"\\datapacks",exist_ok=True)
            ext_path = level_path + "\\datapacks"
            for p in files:
                encoding = "utf-8" if p.flag_bits & 0x800 else "cp437"
                try:
                    p.filename = p.orig_filename.encode(encoding).decode('cp932')
                except:
                    p.filename = p.orig_filename
                if os.sep != "/" and os.sep in p.filename:
                    p.filename = p.filename.replace(os.sep, "/")
                zf.extract(p,ext_path)
                i += 1
                prog.setValue(i)
                prog.setLabelText("展開中:\n"+p.filename)
        prog.close()
        with open(level_path+"\\version.txt",mode="w") as f:
            f.write(ver)
        QtWidgets.QMessageBox.information(self.updater_ui,"TSBTools","アップデートが完了しました！")
        self.reload_levels()

    def open_explorer(self):
        result = subprocess.call(["explorer",self.lineEdit_2.text()+"\\"+self.selected_level],shell=True)
    
    def open_vscode(self):
        os.makedirs(self.lineEdit_2.text()+"\\"+self.selected_level+"\\datapacks",exist_ok=True)
        result = subprocess.call(["code","-g",self.lineEdit_2.text()+"\\"+self.selected_level+"\\datapacks"],shell=True)
        if result == 1:
            QtWidgets.QMessageBox.critical(self,"TSBTools","VSCodeの起動に失敗しました。\nVSCodeはインストールされていますか？")

    def commit_datapack(self):
        level_path = self.lineEdit_2.text()+"\\"+self.selected_level
        if os.path.exists(level_path+"\\datapacks\\.git"):
            Repo(level_path+"\\datapacks").remote().pull()
            QtWidgets.QMessageBox.information(self,"TSBTools","適用が完了しました。")
            self.reload_levels()
            return
        ret = QtWidgets.QMessageBox.information(self,"TSBTools","datapacksが上書きされます。続行しますか？",QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if not (ret == QtWidgets.QMessageBox.Yes):
            return
        shutil.rmtree(level_path+"\\datapacks",ignore_errors=True)
        #os.makedirs(level_path+"\\datapacks",exist_ok=True)
        Repo().clone_from("https://github.com/ProjectTSB/TheSkyBlessing.git",level_path+"\\datapacks")
        QtWidgets.QMessageBox.information(self,"TSBTools","適用が完了しました。")
        self.reload_levels()

    def add_level(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self,"追加するワールドを選ぶ")
        try:
            level_ver, level_name = self.get_world_info(path+"\\level.dat")
            level_name = re.sub("§.","",level_name)
        except:
            QtWidgets.QMessageBox.warning(self,"TSBTools","level.datの読み込みに失敗しました。")
            return
        ret = QtWidgets.QMessageBox.information(self,"TSBTools","ワールドを追加しますか？\nワールド情報\nワールド名: "+level_name+"\nバージョン: "+level_ver,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if not (ret == QtWidgets.QMessageBox.Yes):
            return
        shutil.copytree(path, self.lineEdit_2.text()+"\\"+path.split("/")[-1])
        QtWidgets.QMessageBox.information(self,"TSBTools","ワールドを追加しました。")
        self.reload_levels()
    
    def delete_level(self):
        ret = QtWidgets.QMessageBox.information(self,"TSBTools","ワールドを削除しますか？\nワールド情報\nワールド名: "+self.selected_level,QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
        if not (ret == QtWidgets.QMessageBox.Yes):
            return
        shutil.rmtree(self.lineEdit_2.text()+"\\"+self.selected_level)
        QtWidgets.QMessageBox.information(self,"TSBTools","ワールドを削除しました。")
        self.reload_levels()


class server_ui(QtWidgets.QDialog,server_dialog):
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
    
    

class updater_ui(QtWidgets.QDialog, updater_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class datapack_ui(QtWidgets.QDialog, datapack_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.treeWidget.currentItemChanged.connect(self.show_info)
    
    def fetch_repo(self):
        repo_url = "https://raw.githubusercontent.com/0kq-github/tsbtools-repo/main/repository.json"
        r = requests.get(repo_url)
        repos = r.json()
        repo_list = []
        info_dict = {}
        for repo in repos:
            try:
                if repo["github_url"]:
                    user_name,repo_name = repo["github_url"].split("/")[-2:]
                    latest = requests.get(f"https://api.github.com/repos/{user_name}/{repo_name}/releases/latest")
                    latest_json = latest.json()
                    for asset in latest_json["assets"]:
                        if asset["name"] == repo["filename"]:
                            download_url = asset["browser_download_url"]
                            version = latest_json["tag_name"]
                            description_url = f"https://raw.githubusercontent.com/{user_name}/{repo_name}/{repo['github_branch']}/README.md"
                    repo_data = {
                            "name": repo_name,
                            "author": user_name,
                            "description_url": description_url,
                            "download_url": download_url,
                            "version": version
                            }
                    repo_list.append(repo_data)
                    info_dict[repo_name] = description_url
                    repo_item =  QtWidgets.QTreeWidgetItem([repo_data["name"],repo_data["author"],repo_data["version"]])
                    self.treeWidget.addTopLevelItem(repo_item)
                else:
                    repo_list.append(repo)
                    info_dict[repo["name"]] = repo["description_url"]
                    repo_item =  QtWidgets.QTreeWidgetItem([repo["name"],repo["author"],repo["version"]])
                    self.treeWidget.addTopLevelItem(repo_item)
            except Exception as e:
                print(e)
                continue
        self.info_dict = info_dict
        self.repo_list = repo_list
    
    def show_info(self):
        current = self.treeWidget.currentItem()
        if current:
            self.selected_repo = current.text(0)
            r = requests.get(self.info_dict[self.selected_repo])
            md = markdown.Markdown()
            description = md.convert(r.text)
            self.textBrowser.setText(description)





class load_tsb_releases(QThread):
    signal = Signal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)

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

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        mc = mojangAPI()
        try:
            releases = mc.fetch_release()
            self.signal.emit(releases)
        except:
            pass

class load_levels(QThread):
    signal = Signal()

    def __init__(self,saves_dir,treeWidget,get_world_info,parent=None):
        super().__init__(parent)
        self.saves_dir = saves_dir
        self.treeWidget = treeWidget
        self.get_world_info = get_world_info


    def run(self):
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

def discordRPC(RPC:Presence):
    start_time = time.time()
    while True:
        elapsed_time = int(time.time() - start_time)
        elapsed_time_text = str((elapsed_time % 3600) // 60).zfill(2) + ":"+str(elapsed_time % 3600 % 60).zfill(2)
        if (elapsed_time // 3600) != 0:
            elapsed_time_text = str(elapsed_time // 3600).zfill(2) + ":" + elapsed_time_text 
        RPC.update(
            state=f"{elapsed_time_text} 経過",
            large_image="tsb_icon",
            large_text="v"+version
            )
        time.sleep(0.1)

if __name__ == "__main__":
    client_id = "1002237997997096960"
    try:
        RPC = Presence(client_id)
        RPC.connect()
        th = Thread(target=discordRPC,args=(RPC,))
        th.setDaemon(True)
        th.start()
    except:
        pass
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication()

    #ダークテーマ
    app.setStyleSheet(qdarktheme.load_stylesheet())

    window = MainWindow()
    qt_exception_hook = UncaughtHook()
    #window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()
    app.exec()