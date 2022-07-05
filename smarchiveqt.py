from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
from operator import attrgetter
from pathlib import Path
from datetime import datetime
import sys
from SmArchive_UI import Ui_SmArchiveMainWindow

class SmArchiveMainWindow(QtWidgets.QMainWindow, Ui_SmArchiveMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnSourceDirectory.clicked.connect(self.btnSourceDirectory_Clicked)
        self.btnArchiveDirectory.clicked.connect(self.btnArchiveDirectory_Clicked)
        self.chkOverwriteMode.stateChanged.connect(self.chkOverwriteMode_Checked)
        self.chkSkipMode.stateChanged.connect(self.chkSkipMode_Checked)
        self.btnExecute.clicked.connect(self.btnExecute_Clicked)



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

        size = sourceFile.stat().st_size
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
    ui=SmArchiveMainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    Main()
