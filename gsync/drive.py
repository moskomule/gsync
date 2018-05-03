import os
from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from .file import LocalFile, DriveFile
from .logger import get_logger

logger = get_logger(name="gsync", stdout_filter_level="info")
__all__ = ["Drive"]


class Drive(object):
    _parents = {}

    def __init__(self):
        # authorize
        self.drive = None
        self._authorize()
        http = self.drive.auth.Get_Http_Object()
        self.param = {"http": http}

    def create_directory(self, name, parent_id=None):
        new_dir = LocalFile(self.drive, name, is_directory=True,
                            parent_id=parent_id)
        new_dir.upload()
        return new_dir.file_id

    def upload(self, path, parent=None):
        if parent is None:
            self._upload(path)
        else:
            # todo what if parent is like /foo/bar ?
            self._parents[parent] = self.create_directory(parent)
            self._upload(path, self._parents[parent])

    def _upload(self, path, parent_id=None):
        # internal process
        path = Path(path).expanduser()

        logger.info(f"Uploading: {path.name}")
        file = LocalFile(self.drive, path.name, path.is_dir(), parent_id)
        if path.is_file():
            file.set_content(path)

        try:
            file.upload(param=self.param)
        except Exception as e:
            logger.warning(e)

        if path.is_dir():
            for p in path.iterdir():
                self._upload(p, parent_id=file.file_id)

    def download(self, id, save_dir):
        save_dir = Path(save_dir)
        file = DriveFile(self.drive, id)
        logger.info(f"Downloaded: {file.name} in {str(save_dir)}")
        file.download(save_dir)

    def list(self, parent=None, max_size=10):
        meta_data = {"q": "trashed=false",
                     "maxResults": max_size}
        if parent is not None:
            meta_data["q"] += f" and '{parent}' in parents "
        try:
            file_list = self.drive.ListFile(meta_data).GetList()
            return [(f["title"], f["id"], f['mimeType']) for f in file_list]
        except Exception as e:
            logger.warning(e)

    def _authorize(self):
        env = os.getenv("GDRIVE_PATH")
        if env is None:
            yaml = Path("~/.gdrive/settings.yaml").expanduser()
        else:
            yaml = Path(env) / "settings.yaml"
        gauth = GoogleAuth(yaml)
        gauth.CommandLineAuth()
        self.drive = GoogleDrive(gauth)
