import os
from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from .logger import get_logger

logger = get_logger(name="gsync", stdout_filter_level="info")
__all__ = ["Drive"]


class Drive(object):

    @staticmethod
    def _get_settings_yaml():
        env = os.getenv("GDRIVE_PATH")
        if env is None:
            return Path("~/.gdrive/settings.yaml").expanduser()
        else:
            return Path(env) / "settings.yaml"

    def __init__(self):
        # authorize
        gauth = GoogleAuth(self._get_settings_yaml())
        gauth.CommandLineAuth()
        self.drive = GoogleDrive(gauth)
        logger.info("Authenticated!")

    def upload(self, path, parent=None):
        if parent is None:
            self._upload(path)
        else:
            dir = self.drive.CreateFile({"title": parent,
                                         "mimeType": "application/vnd.google-apps.folder"})
            dir.Upload()
            self._upload(path, dir["id"])

    def _upload(self, path, parent_id=None):
        path = Path(path).expanduser()
        if path.is_file():
            logger.info(f"Uploading {path.name}")
            metadata = {"title": path.name}
            if parent_id is not None:
                metadata.update({"parents": [{"kind": "drive#fileLink",
                                              "id": parent_id}]})

            file = self.drive.CreateFile(metadata)
            file.SetContentFile(str(path))
            file.Upload()

        else:
            metadata = {"title": path.name,
                        "mimeType": "application/vnd.google-apps.folder"}
            if parent_id is not None:
                metadata.update({"parents": {"kind": "drive#fileLink",
                                             "id": parent_id}})
            dir = self.drive.CreateFile(metadata)
            dir.Upload()
            for p in path.iterdir():
                self._upload(p, parent_id=dir["id"])
