from pydrive.drive import GoogleDrive
from pathlib import Path

DIRECTORY_MIME = "application/vnd.google-apps.folder"


class File(object):
    def __init__(self, drive: GoogleDrive, name: str, is_directory: bool, parent_id: str):
        self.drive = drive
        self.name = name
        self.is_directory = is_directory
        self.parent_id = parent_id
        self.metadata = {"title": name}


class LocalFile(File):
    def __init__(self, drive: GoogleDrive, name: str, is_directory: bool, parent_id: str = None):
        super(LocalFile, self).__init__(drive, name, is_directory, parent_id)
        if parent_id is not None:
            self.metadata["parents"] = [{"id": parent_id}]
        if self.is_directory:
            self.metadata["mimeType"] = DIRECTORY_MIME
        self.file = self.drive.CreateFile(self.metadata)

    def set_content(self, path: Path):
        self.file.SetContentFile(str(path))

    def upload(self, **kwargs):
        self.file.Upload(**kwargs)

    @property
    def file_id(self):
        return self.file.get("id")

    def __repr__(self):
        return f"{self.name} ({'directory' if self.is_directory else 'file'}) \n" \
               f"meta: {self.metadata}"


class DriveFile(File):
    def __init__(self, drive, file_id):
        self.file = drive.CreateFile({"id": file_id})
        super(DriveFile, self).__init__(drive, self.file["title"], False,
                                        self.file["mimeType"] == DIRECTORY_MIME)

    def download(self, save_dir: Path, **kwargs):
        self.file.GetContentFile(save_dir / self.name, **kwargs)
