from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
from operator import attrgetter
from pathlib import Path
from datetime import datetime
import sys
from SmArchive_UI import Ui_SmArchiveMainWindow


def showErrorMessage(message, title):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Icon.Critical)
    msgBox.setText(message)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
    msgBox.exec()


def showDuplicateFileDialog(source_file_path, archive_file_path):
    sourceFile = Path(source_file_path)
    archiveFile = Path(archive_file_path)

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


def getFilePathViaDialog():
    dialog = QFileDialog()
    returnPath = dialog.getExistingDirectory()
    return str(Path(returnPath).absolute()) + "\\"


class SmArchiveMainWindow(QtWidgets.QMainWindow, Ui_SmArchiveMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnSourceDirectory.clicked.connect(self.btnSourceDirectory_Clicked)
        self.btnArchiveDirectory.clicked.connect(self.btnArchiveDirectory_Clicked)
        self.chkOverwriteMode.stateChanged.connect(self.chkOverwriteMode_Checked)
        self.chkSkipMode.stateChanged.connect(self.chkSkipModeChecked)
        self.btnExecute.clicked.connect(self.btnExecute_Clicked)

    def btnArchiveDirectory_Clicked(self):
        self.txtArchiveDirectory.setText(getFilePathViaDialog())

    def btnSourceDirectory_Clicked(self):
        self.txtSourceDirectory.setText(getFilePathViaDialog())

    def chkOverwriteMode_Checked(self, state):
        if QtCore.Qt.CheckState(state) == Qt.CheckState.Checked:
            self.chkSkipMode.setChecked(False)

    def chkSkipModeChecked(self, state):
        if QtCore.Qt.CheckState(state) == Qt.CheckState.Checked:
            self.chkOverwriteMode.setChecked(False)

    def btnExecute_Clicked(self):
        source_directory = self.txtSourceDirectory.text()
        archive_directory = self.txtArchiveDirectory.text()
        self.lstOutput.clear()
        if not Path(source_directory).exists():
            showErrorMessage("Source Directory does not exist.", "Error")
            return

        if not Path(archive_directory).exists():
            showErrorMessage("Archive Directory does not exist.", "Error")
            return

        if str(source_directory).strip().upper() == str(archive_directory).strip().upper():
            showErrorMessage("Source Directory and Archive Directory cannot be the same directory.", "Error")
            return

        if self.txtFileExtension.text()[0] == "*":
            file_extension = self.txtFileExtension.text()[1:]
        else:
            file_extension = self.txtFileExtension.text()
        overwrite_mode = self.chkOverwriteMode.isChecked()
        test_mode = self.chkTestMode.isChecked()
        skip_mode = self.chkSkipMode.isChecked()
        file_suffix_length = int(self.lblFileNameSuffixLengthValue.text())
        self.archiveFiles(source_directory, archive_directory, file_suffix_length, file_extension, overwrite_mode, skip_mode, test_mode)

    def archiveFiles(self, source_directory, archive_directory, file_suffix_length, file_extension, overwrite_mode,
                     skip_mode,
                     test_mode):
        allSourceFilesList = []
        uniqueSourceFilesList = []
        numberOfArchivedFiles = 0

        sourceFiles = Path(source_directory)
        for x in sourceFiles.iterdir():
            if not x.is_file():
                continue
            if (file_extension == ".*") or (x.suffix == file_extension):
                archive_file = ArchiveFileInfo(str(x.absolute()), file_suffix_length)
                allSourceFilesList.append(archive_file)
                if not uniqueSourceFilesList.__contains__(archive_file):
                    uniqueSourceFilesList.append(archive_file)

        for y in uniqueSourceFilesList:
            filteredFileList = [s for s in allSourceFilesList if s.Hash == y.Hash]
            maxFilteredFile = max(filteredFileList, key=attrgetter('ArchiveFileSuffix'))
            for z in filteredFileList:
                if z.ArchiveFileSuffix != maxFilteredFile.ArchiveFileSuffix:
                    newFilePath = archive_directory + z.FileName + z.file_extension
                    if self.archiveFile(z.FilePath, newFilePath, overwrite_mode, skip_mode, test_mode):
                        numberOfArchivedFiles += 1

        self.updateArchiveOutput(f"Total number of files moved: {numberOfArchivedFiles}")

    def archiveFile(self, source_file_path, archive_file_path, overwrite_mode, skip_mode, test_mode):
        if Path(archive_file_path).exists():
            if skip_mode is True:
                return False
            if overwrite_mode:
                if not test_mode:
                    Path(source_file_path).replace(archive_file_path)
                    self.updateArchiveOutput(f"Archived file '{archive_file_path}'")
                    return True
                else:
                    # test_mode = True
                    self.updateArchiveOutput(f"Would have archived file '{archive_file_path}'")
                    return False
            else:
                # overwrite_mode =  False
                if not test_mode:
                    if showDuplicateFileDialog(source_file_path, archive_file_path):
                        Path(source_file_path).replace(archive_file_path)
                        self.updateArchiveOutput(f"Archived file '{archive_file_path}'")
                        return True
                    else:
                        # User did not enter 'Y'
                        self.updateArchiveOutput(f"Skipped file '{archive_file_path}'")
                        return False
                else:
                    # test_mode = True
                    if showDuplicateFileDialog(source_file_path, archive_file_path):
                        self.updateArchiveOutput(f"Would have archived file '{archive_file_path}'")
                        return False
                    else:
                        # User did not enter 'Y'
                        self.updateArchiveOutput(f"Skipped file '{archive_file_path}'")
                        return False

        else:
            # Archive File does not already exist.
            if not test_mode:
                Path(source_file_path).replace(archive_file_path)
                self.updateArchiveOutput(f"Archived file '{archive_file_path}'")
                return True
            else:
                # test_mode = False
                self.updateArchiveOutput(f"Would have archived file '{archive_file_path}'")
                return False

    def updateArchiveOutput(self, message):
        self.lstOutput.addItem(message)


class ArchiveFileInfo:
    def __init__(self, file_path: str, archive_file_suffix_length: int):
        self.Archivefile_suffix_length = archive_file_suffix_length
        self.FilePath = file_path
        self.file_extension = Path(file_path).suffix
        self.FileName = Path(file_path).stem
        uniqueFileNameLength = len(Path(file_path).stem) - self.Archivefile_suffix_length
        self.UniqueFileName = self.FileName[:uniqueFileNameLength]
        self.ArchiveFileSuffix = self.FileName[-self.Archivefile_suffix_length:]
        self.Hash = self.UniqueFileName + self.file_extension

    def __eq__(self, other):
        return other.Hash == self.Hash


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = SmArchiveMainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
