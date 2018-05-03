from pathlib import Path
import os
from pydrive import auth, drive


def _authorize():
    env = os.getenv("GDRIVE_PATH")
    if env is None:
        yaml = Path("~/.gdrive/settings.yaml").expanduser()
    else:
        yaml = Path(env) / "settings.yaml"
    gauth = auth.GoogleAuth(yaml)
    gauth.CommandLineAuth()
    return drive.GoogleDrive(gauth)
