import os
from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from .logger import get_logger

logger = get_logger(name="gsync", stdout_filter_level="info")
__all__ = ["Drive"]


class Drive(object):
    _parents = {}

    @staticmethod
    def _get_settings_yaml():
        env = os.getenv("GDRIVE_PATH")
        if env is None:
            return Path("~/.gdrive/settings.yaml").expanduser()
        else:
            return Path(env) / "settings.yaml"

    def _authorize(self):
        gauth = GoogleAuth(self._get_settings_yaml())
        gauth.CommandLineAuth()
        self.drive = GoogleDrive(gauth)

    def __init__(self):
        # authorize
        self.drive = None
        self._authorize()

    def upload(self, path, parent=None):
        if parent is None:
            self._upload(path)
        else:
            # use self._parents to save files in an identical parent directory.
            if self._parents.get(parent) is None:
                dir = self.drive.CreateFile({"title": parent,
                                             "mimeType": "application/vnd.google-apps.folder"})
                try:
                    dir.Upload()
                except Exception as e:
                    logger.warning(e)
                self._parents[parent] = dir["id"]
            self._upload(path, self._parents[parent])

    def _upload(self, path, parent_id=None):
        http = self.drive.auth.Get_Http_Object()
        path = Path(path).expanduser()
        if path.is_file():
            logger.info(f"Uploading {path.name}")
            metadata = {"title": path.name}
            if parent_id is not None:
                metadata.update({"parents": [{"kind": "drive#fileLink",
                                              "id": parent_id}]})

            file = self.drive.CreateFile(metadata)
            file.SetContentFile(str(path))
            try:
                file.Upload(param={"http": http})
            except Exception as e:
                logger.warning(e)

        else:
            metadata = {"title": path.name,
                        "mimeType": "application/vnd.google-apps.folder"}
            if parent_id is not None:
                metadata.update({"parents": [{"kind": "drive#fileLink",
                                              "id": parent_id}]})
            dir = self.drive.CreateFile(metadata)
            try:
                dir.Upload(param={"http": http})
            except Exception as e:
                logger.warning(e)
            for p in path.iterdir():
                self._upload(p, parent_id=dir["id"])

    def download(self, id, save_dir):
        raise NotImplementedError

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
