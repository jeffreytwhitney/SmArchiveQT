from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
from operator import attrgetter
from pathlib import Path
from datetime import datetime
import sys
from typing import List
from SmArchive_UI import Ui_SmArchiveMainWindow


def show_error_message(message, title):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setText(message)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()


def show_duplicate_file_dialog(source_file_path, archive_file_path):
    source_file = Path(source_file_path)
    archive_file = Path(archive_file_path)

    source_file_size = "{:,} bytes".format(source_file.stat().st_size)
    source_file_last_modified = datetime.fromtimestamp(source_file.stat().st_mtime)

    archive_file_size = "{:,} bytes".format(archive_file.stat().st_size)
    archive_file_last_modified = datetime.fromtimestamp(archive_file.stat().st_mtime)

    detailed_text = f"SourceFile {source_file.name}: \n\tFileSize: {source_file_size}\n\t" \
                    f"Last Modified: {source_file_last_modified}\n" \
                    f"ArchiveFile {archive_file.name}: \n\tFileSize: {archive_file_size}\n\t" \
                    f"Last Modified: {archive_file_last_modified}"

    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Information)
    msg_box.setText(f"File {archive_file.name} already exists in archive directory. Replace?")
    msg_box.setWindowTitle("Duplicate Archive File")
    msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg_box.setDetailedText(detailed_text)
    msg_box.exec()
    return msg_box.clickedButton().text() == "&Yes"


def get_file_path_via_dialog():
    dialog = QFileDialog()
    return_path = dialog.getExistingDirectory()
    return str(Path(return_path).absolute()) + "\\"


class SmArchiveMainWindow(QtWidgets.QMainWindow, Ui_SmArchiveMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnSourceDirectory.clicked.connect(self.btn_source_directory_clicked)
        self.btnArchiveDirectory.clicked.connect(self.btn_archive_directory_clicked)
        self.chkOverwriteMode.stateChanged.connect(self.chk_overwrite_mode_checked)
        self.chkSkipMode.stateChanged.connect(self.chk_skip_mode_checked)
        self.btnExecute.clicked.connect(self.btn_execute_clicked)

    def btn_archive_directory_clicked(self):
        self.txtArchiveDirectory.setText(get_file_path_via_dialog())

    def btn_source_directory_clicked(self):
        self.txtSourceDirectory.setText(get_file_path_via_dialog())

    def chk_overwrite_mode_checked(self, state):
        if QtCore.Qt.CheckState(state) == Qt.CheckState.Checked:
            self.chkSkipMode.setChecked(False)

    def chk_skip_mode_checked(self, state):
        if QtCore.Qt.CheckState(state) == Qt.CheckState.Checked:
            self.chkOverwriteMode.setChecked(False)

    def btn_execute_clicked(self):
        source_directory = self.txtSourceDirectory.text()
        archive_directory = self.txtArchiveDirectory.text()
        self.lstOutput.clear()
        if not Path(source_directory).exists():
            show_error_message("Source Directory does not exist.", "Error")
            return

        if not Path(archive_directory).exists():
            show_error_message("Archive Directory does not exist.", "Error")
            return

        if str(source_directory).strip().upper() == str(archive_directory).strip().upper():
            show_error_message("Source Directory and Archive Directory cannot be the same directory.", "Error")
            return

        if self.txtFileExtension.text()[0] == "*":
            file_extension = self.txtFileExtension.text()[1:]
        else:
            file_extension = self.txtFileExtension.text()

        overwrite_mode = self.chkOverwriteMode.isChecked()
        test_mode = self.chkTestMode.isChecked()
        skip_mode = self.chkSkipMode.isChecked()
        file_suffix_length = int(self.lblFileNameSuffixLengthValue.text())
        self.archive_files(source_directory, archive_directory, file_suffix_length,
                           file_extension, overwrite_mode, skip_mode, test_mode)

    def archive_files(self, source_directory: str, archive_directory: str, file_suffix_length: int,
                      file_extension: str, overwrite_mode: bool, skip_mode: bool, test_mode: bool):

        allSourceFilesList: List[ArchiveFileInfo] = []
        uniqueSourceFilesList = set([])
        numberOfArchivedFiles: int = 0

        sourceFiles = Path(source_directory)
        for x in sourceFiles.iterdir():
            if not x.is_file():
                continue
            if (file_extension == ".*") or (x.suffix == file_extension):
                archive_file = ArchiveFileInfo(str(x.absolute()), file_suffix_length)
                allSourceFilesList.append(archive_file)
                uniqueSourceFilesList.add(archive_file)

        for y in uniqueSourceFilesList:
            filteredFileList = [s for s in allSourceFilesList if s == y]
            maxFilteredFile = max(filteredFileList, key=attrgetter('ArchiveFileSuffix'))
            for z in filteredFileList:
                if z.ArchiveFileSuffix != maxFilteredFile.ArchiveFileSuffix:
                    newFilePath = archive_directory + z.FileName + z.FileExtension
                    if self.archive_file(z.FilePath, newFilePath, overwrite_mode, skip_mode, test_mode):
                        numberOfArchivedFiles += 1

        self.update_archive_output(f"Total number of files moved: {numberOfArchivedFiles}")

    def archive_file(self, source_file_path: str, archive_file_path: str, overwrite_mode: bool, skip_mode: bool,
                     test_mode: bool):
        if Path(archive_file_path).exists():
            if skip_mode is True:
                return False
            if overwrite_mode:
                if not test_mode:
                    Path(source_file_path).replace(archive_file_path)
                    self.update_archive_output(f"Archived file '{archive_file_path}'")
                    return True
                else:
                    # test_mode = True
                    self.update_archive_output(f"Would have archived file '{archive_file_path}'")
                    return False
            else:
                # overwrite_mode =  False
                if not test_mode:
                    if show_duplicate_file_dialog(source_file_path, archive_file_path):
                        Path(source_file_path).replace(archive_file_path)
                        self.update_archive_output(f"Archived file '{archive_file_path}'")
                        return True
                    else:
                        # User did not enter 'Y'
                        self.update_archive_output(f"Skipped file '{archive_file_path}'")
                        return False
                else:
                    # test_mode = True
                    if show_duplicate_file_dialog(source_file_path, archive_file_path):
                        self.update_archive_output(f"Would have archived file '{archive_file_path}'")
                        return False
                    else:
                        # User did not enter 'Y'
                        self.update_archive_output(f"Skipped file '{archive_file_path}'")
                        return False

        else:
            # Archive File does not already exist.
            if not test_mode:
                Path(source_file_path).replace(archive_file_path)
                self.update_archive_output(f"Archived file '{archive_file_path}'")
                return True
            else:
                # test_mode = True
                self.update_archive_output(f"Would have archived file '{archive_file_path}'")
                return False

    def update_archive_output(self, message):
        self.lstOutput.addItem(message)


class ArchiveFileInfo:

    def __init__(self, file_path: str, archive_file_suffix_length: int):
        self.FileSuffixLength = archive_file_suffix_length
        self.FilePath = file_path
        self.FileExtension = Path(file_path).suffix
        self.FileName = Path(file_path).stem
        uniqueFileNameLength = len(Path(file_path).stem) - self.FileSuffixLength
        self.UniqueFileName = self.FileName[:uniqueFileNameLength]
        self.ArchiveFileSuffix = self.FileName[-self.FileSuffixLength:]

    def __eq__(self, other):
        return other.UniqueFileName == self.UniqueFileName and other.FileExtension == self.FileExtension

    def __hash__(self):
        return hash((self.UniqueFileName, self.FileExtension))


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = SmArchiveMainWindow()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
