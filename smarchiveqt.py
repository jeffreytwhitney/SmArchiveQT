from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
from operator import attrgetter
from pathlib import Path
from datetime import datetime
import sys


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(649, 419)
        MainWindow.setMaximumSize(QtCore.QSize(650, 450))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.txtSourceDirectory = QtWidgets.QLineEdit(self.centralwidget)
        self.txtSourceDirectory.setGeometry(QtCore.QRect(140, 10, 301, 20))
        self.txtSourceDirectory.setObjectName("txtSourceDirectory")
        self.txtSourceDirectory.setEnabled(False)
        self.txtArchiveDirectory = QtWidgets.QLineEdit(self.centralwidget)
        self.txtArchiveDirectory.setGeometry(QtCore.QRect(140, 40, 301, 20))
        self.txtArchiveDirectory.setObjectName("txtArchiveDirectory")
        self.txtArchiveDirectory.setEnabled(False)
        self.btnSourceDirectory = QtWidgets.QPushButton(self.centralwidget)
        self.btnSourceDirectory.setGeometry(QtCore.QRect(450, 10, 21, 23))
        self.btnSourceDirectory.setObjectName("btnSourceDirectory")
        self.btnSourceDirectory.clicked.connect(self.btnSourceDirectory_Clicked)
        self.btnArchiveDirectory = QtWidgets.QPushButton(self.centralwidget)
        self.btnArchiveDirectory.setGeometry(QtCore.QRect(450, 40, 21, 23))
        self.btnArchiveDirectory.setObjectName("btnArchiveDirectory")
        self.btnArchiveDirectory.clicked.connect(self.btnArchiveDirectory_Clicked)
        self.lblSourceDirectory = QtWidgets.QLabel(self.centralwidget)
        self.lblSourceDirectory.setGeometry(QtCore.QRect(6, 10, 121, 20))
        self.lblSourceDirectory.setObjectName("lblSourceDirectory")
        self.lblArchiveDirectory = QtWidgets.QLabel(self.centralwidget)
        self.lblArchiveDirectory.setGeometry(QtCore.QRect(6, 40, 121, 20))
        self.lblArchiveDirectory.setObjectName("lblArchiveDirectory")
        self.sldFileNameSuffixLength = QtWidgets.QSlider(self.centralwidget)
        self.sldFileNameSuffixLength.setGeometry(QtCore.QRect(164, 100, 131, 22))
        self.sldFileNameSuffixLength.setMinimum(1)
        self.sldFileNameSuffixLength.setMaximum(5)
        self.sldFileNameSuffixLength.setPageStep(1)
        self.sldFileNameSuffixLength.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.sldFileNameSuffixLength.setObjectName("sldFileNameSuffixLength")
        self.lblFileNameSuffixLengthValue = QtWidgets.QLabel(self.centralwidget)
        self.lblFileNameSuffixLengthValue.setGeometry(QtCore.QRect(140, 100, 21, 20))
        self.lblFileNameSuffixLengthValue.setObjectName("lblFileNameSuffixLengthValue")
        self.lblFileNameSuffixLength = QtWidgets.QLabel(self.centralwidget)
        self.lblFileNameSuffixLength.setGeometry(QtCore.QRect(6, 100, 121, 20))
        self.lblFileNameSuffixLength.setObjectName("lblFileNameSuffixLength")
        self.chkOverwriteMode = QtWidgets.QCheckBox(self.centralwidget)
        self.chkOverwriteMode.setGeometry(QtCore.QRect(140, 140, 450, 17))
        self.chkOverwriteMode.setObjectName("chkOverwriteMode")
        self.chkOverwriteMode.stateChanged.connect(self.chkOverwriteMode_Checked)
        self.chkTestMode = QtWidgets.QCheckBox(self.centralwidget)
        self.chkTestMode.setGeometry(QtCore.QRect(140, 160, 450, 17))
        self.chkTestMode.setObjectName("chkTestMode")
        self.chkSkipMode = QtWidgets.QCheckBox(self.centralwidget)
        self.chkSkipMode.setGeometry(QtCore.QRect(140, 180, 250, 17))
        self.chkSkipMode.setObjectName("chkSkipMode")
        self.chkSkipMode.stateChanged.connect(self.chkSkipMode_Checked)
        self.lblFileExtension = QtWidgets.QLabel(self.centralwidget)
        self.lblFileExtension.setGeometry(QtCore.QRect(6, 70, 121, 20))
        self.lblFileExtension.setObjectName("lblFileExtension")
        self.txtFileExtension = QtWidgets.QLineEdit(self.centralwidget)
        self.txtFileExtension.setGeometry(QtCore.QRect(140, 70, 61, 20))
        self.txtFileExtension.setObjectName("txtArchiveDirectory_2")
        self.lstOutput = QtWidgets.QListWidget(self.centralwidget)
        self.lstOutput.setGeometry(QtCore.QRect(10, 210, 631, 131))
        self.lstOutput.setObjectName("lstOutput")
        self.lblOutput = QtWidgets.QLabel(self.centralwidget)
        self.lblOutput.setGeometry(QtCore.QRect(10, 190, 47, 13))
        self.lblOutput.setObjectName("lblOutput")
        self.btnExecute = QtWidgets.QPushButton(self.centralwidget)
        # self.btnExecute.setEnabled(False)
        self.btnExecute.setGeometry(QtCore.QRect(560, 350, 75, 23))
        self.btnExecute.setObjectName("btnArchive")
        self.btnExecute.clicked.connect(self.btnExecute_Clicked)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 649, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.sldFileNameSuffixLength.valueChanged[
            'int'].connect(self.lblFileNameSuffixLengthValue.setNum)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SmArchive: Smart Archive Tool"))
        self.btnSourceDirectory.setText(_translate("MainWindow", "..."))
        self.btnArchiveDirectory.setText(_translate("MainWindow", "..."))
        self.lblSourceDirectory.setText(_translate("MainWindow", "Source Directory:"))
        self.lblArchiveDirectory.setText(_translate("MainWindow", "Archive Directory:"))
        self.lblFileNameSuffixLengthValue.setText(_translate("MainWindow", "1"))
        self.lblFileNameSuffixLength.setText(_translate("MainWindow", "FileName Suffix Length:"))
        self.chkOverwriteMode.setText(_translate("MainWindow", "Overwrite Mode (Automatically overwrites duplicate files)"))
        self.chkTestMode.setText(_translate("MainWindow", "Test Mode (Won\'t move files, just tells you what it would have done)"))
        self.chkSkipMode.setText(_translate("MainWindow", "Skip Mode (Skips duplicate files)"))
        self.lblFileExtension.setText(_translate("MainWindow", "File Extension:"))
        self.txtFileExtension.setText(_translate("MainWindow", "*.*"))
        self.lblOutput.setText(_translate("MainWindow", "Output:"))
        self.btnExecute.setText(_translate("MainWindow", "Archive!"))

    def btnArchiveDirectory_Clicked(self):
        self.txtArchiveDirectory.setText(self.GetFilePathViaDialog())

    def btnSourceDirectory_Clicked(self):
        self.txtSourceDirectory.setText(self.GetFilePathViaDialog())

    def chkOverwriteMode_Checked(self, state):
        if QtCore.Qt.CheckState(state) == Qt.CheckState.Checked:
            self.chkSkipMode.setChecked(False)

    def chkSkipMode_Checked(self, state):
        if QtCore.Qt.CheckState(state) == Qt.CheckState.Checked:
            self.chkOverwriteMode.setChecked(False)

    def btnExecute_Clicked(self):
        sourceDirectory = self.txtSourceDirectory.text()
        archiveDirectory = self.txtArchiveDirectory.text()
        self.lstOutput.clear()
        if not Path(sourceDirectory).exists():
            self.showErrorMessage("Source Directory does not exist.", "Error")
            return

        if not Path(archiveDirectory).exists():
            self.showErrorMessage("Archive Directory does not exist.", "Error")
            return

        if str(sourceDirectory).strip().upper() == str(archiveDirectory).strip().upper():
            self.showErrorMessage("Source Directory and Archive Directory cannot be the same directory.", "Error")
            return

        if self.txtFileExtension.text()[0] == "*":
            fileExtension = self.txtFileExtension.text()[1:]
        else:
            fileExtension = self.txtFileExtension.text()
        overwriteMode = self.chkOverwriteMode.isChecked()
        testMode = self.chkTestMode.isChecked()
        skipMode = self.chkSkipMode.isChecked()
        fileSuffixLength = int(self.lblFileNameSuffixLengthValue.text())
        self.ArchiveFiles(sourceDirectory, archiveDirectory, fileSuffixLength, fileExtension, overwriteMode, skipMode, testMode)


    def showErrorMessage(self, message, title):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Critical)
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()

    def showDuplicateFileDialog(self, sourceFilePath, archiveFilePath):
        sourceFile = Path(sourceFilePath)
        archiveFile = Path(archiveFilePath)

        sourceFileSize = "{:,} bytes".format(sourceFile.stat().st_size)
        sourceFileLastModified = datetime.fromtimestamp(sourceFile.stat().st_mtime)

        archiveFileSize = "{:,} bytes".format(archiveFile.stat().st_size)
        archiveFileLastModified = datetime.fromtimestamp(archiveFile.stat().st_mtime)

        detailedText = f"SourceFile {sourceFile.name}: \n\tFileSize: {sourceFileSize}\n\tLast Modified: {sourceFileLastModified}\nArchiveFile {archiveFile.name}: \n\tFileSize: {archiveFileSize}\n\tLast Modified: {archiveFileLastModified}"

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setText(f"File {archiveFile.name} already exists in archive directory. Replace?")
        msgBox.setWindowTitle("Duplicate Archive File")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msgBox.setDetailedText(detailedText)
        msgBox.exec()
        return msgBox.clickedButton().text() == "&Yes"

    def GetFilePathViaDialog(self):
        dialog = QFileDialog()
        returnPath = dialog.getExistingDirectory()
        return str(Path(returnPath).absolute()) + "\\"

    def ArchiveFiles(self, sourceDirectory, archiveDirectory, fileSuffixLength, fileExtension, overwriteMode, skipMode,
                     testMode):
        allSourceFilesList = []
        uniqueSourceFilesList = []
        numberOfArchivedFiles = 0

        sourceFiles = Path(sourceDirectory)
        for x in sourceFiles.iterdir():
            if not x.is_file():
                continue
            if (fileExtension == ".*") or (x.suffix == fileExtension):
                archive_file = ArchiveFileInfo(str(x.absolute()), fileSuffixLength)
                allSourceFilesList.append(archive_file)
                if not uniqueSourceFilesList.__contains__(archive_file):
                    uniqueSourceFilesList.append(archive_file)

        for y in uniqueSourceFilesList:
            filteredFileList = list(filter(lambda l: l.Hash == y.Hash, allSourceFilesList))
            maxFilteredFile = max(filteredFileList, key=attrgetter('ArchiveFileSuffix'))
            for z in filteredFileList:
                if z.ArchiveFileSuffix != maxFilteredFile.ArchiveFileSuffix:
                    newFilePath = archiveDirectory + z.FileName + z.FileExtension
                    if self.ArchiveFile(z.FilePath, newFilePath, overwriteMode, skipMode, testMode):
                        numberOfArchivedFiles += 1

        self.UpdateArchiveOutput(f"Total number of files moved: {numberOfArchivedFiles}")

    def ArchiveFile(self, sourceFilePath, archiveFilePath, overwriteMode, skipMode, testMode):
        if Path(archiveFilePath).exists():
            if skipMode is True:
                return False
            if overwriteMode:
                if not testMode:
                    Path(sourceFilePath).replace(archiveFilePath)
                    self.UpdateArchiveOutput(f"Archived file '{archiveFilePath}'")
                    return True
                else:
                    # TestMode = True
                    self.UpdateArchiveOutput(f"Would have archived file '{archiveFilePath}'")
                    return False
            else:
                # OverwriteMode =  False
                if not testMode:
                    if self.showDuplicateFileDialog(sourceFilePath, archiveFilePath):
                        Path(sourceFilePath).replace(archiveFilePath)
                        self.UpdateArchiveOutput(f"Archived file '{archiveFilePath}'")
                        return True
                    else:
                        # User did not enter 'Y'
                        self.UpdateArchiveOutput(f"Skipped file '{archiveFilePath}'")
                        return False
                else:
                    # TestMode = True
                    if self.showDuplicateFileDialog(sourceFilePath, archiveFilePath):
                        self.UpdateArchiveOutput(f"Would have archived file '{archiveFilePath}'")
                        return False
                    else:
                        # User did not enter 'Y'
                        self.UpdateArchiveOutput(f"Skipped file '{archiveFilePath}'")
                        return False

        else:
            # Archive File does not already exist.
            if not testMode:
                Path(sourceFilePath).replace(archiveFilePath)
                self.UpdateArchiveOutput(f"Archived file '{archiveFilePath}'")
                return True
            else:
                # TestMode = False
                self.UpdateArchiveOutput(f"Would have archived file '{archiveFilePath}'")
                return False

    def UpdateArchiveOutput(self, message):
        self.lstOutput.addItem(message)

    def ValidateForm(self):
        pass


class ArchiveFileInfo:
    def __init__(self, file_path: str, archive_file_suffix_length: int):
        self.ArchiveFileSuffixLength = archive_file_suffix_length
        self.FilePath = file_path
        self.FileExtension = Path(file_path).suffix
        self.FileName = Path(file_path).stem
        uniqueFileNameLength = len(Path(file_path).stem) - self.ArchiveFileSuffixLength
        self.UniqueFileName = self.FileName[:uniqueFileNameLength]
        self.ArchiveFileSuffix = self.FileName[-self.ArchiveFileSuffixLength:]
        self.Hash = self.UniqueFileName + self.FileExtension

    def __eq__(self, other):
        return other.Hash == self.Hash


def Main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    Main()
