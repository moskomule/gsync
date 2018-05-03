from pathlib import Path

from .file import LocalFile, DriveFile
from .logger import get_logger
from .backends import _authorize

logger = get_logger(name="gsync", stdout_filter_level="info")
__all__ = ["Drive"]


class Drive(object):
    _parents = {}

    def __init__(self):
        # authorize
        self.drive = _authorize()
        http = self.drive.auth.Get_Http_Object()
        self.param = {"http": http}

    def create_directory(self, name: str, parent_id: str = None):
        """
        Create an empty directory
        :param name: name of the directory
        :param parent_id: id of the parent directory. If None, the parent is the root. (default: None)
        :return: id of the created directory
        """
        new_dir = LocalFile(self.drive, name, is_directory=True,
                            parent_id=parent_id)
        new_dir.upload()
        id = new_dir.file_id
        self._parents[name] = id
        return id

    def upload(self, path: str or Path, parent_name: str = None):
        """
        Upload a file
        :param path: path to the file to be uploaded
        :param parent_name: name of the parent directory. If None, the parent is the root. (default: None)
        """
        if parent_name is None:
            self._upload(path)
        else:
            # todo what if parent_name is like /foo/bar ?
            self._parents[parent_name] = self.create_directory(parent_name)
            self._upload(path, self._parents[parent_name])

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
            # recursively upload the contents
            for p in path.iterdir():
                self._upload(p, parent_id=file.file_id)

    def download(self, id, save_dir=None):
        """
        Download a file
        :param id: file id of the file to be downloaded
        :param save_dir: the directory path the downloaded file to be saved. If None, save in the current directory.
        """
        save_dir = Path("." if save_dir is None else save_dir)
        file = DriveFile(self.drive, id)
        logger.info(f"Downloaded: {file.name} in {str(save_dir)}")
        file.download(save_dir)

    def list(self, parent=None, max_size=10):
        """
        List files in Drive
        :param parent: parent name. If None, parent is not set (default: None)
        :param max_size: the number of contents to be listed (default: 10)
        """
        meta_data = {"q": "trashed=false",
                     "maxResults": max_size}
        if parent is not None:
            meta_data["q"] += f" and '{parent}' in parents "
        try:
            file_list = self.drive.ListFile(meta_data).GetList()
            return [(f["title"], f["id"], f['mimeType']) for f in file_list]
        except Exception as e:
            logger.warning(e)
