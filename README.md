# GSync

Simple PyDrive wrapper

## Settings

Set `settings.yaml` below in `$HOME/.gdrive`. The client codes are available from [Google APIs](https://console.developers.google.com/apis/).

You need to modify the 3rd, 4th and 8th line.

```
client_config_backend: settings
client_config:
  client_id: CLIENT_ID_HERE
  client_secret: CLIENT_SECRET_HERE

save_credentials: True
save_credentials_backend: file
save_credentials_file: FULL_PATH_WHERE_YOU_SAVE/credentials.json
get_refresh_token: True
oauth_scope:
  - https://www.googleapis.com/auth/drive.file
  - https://www.googleapis.com/auth/drive.install
```

## Usage

### Python

```python
from gsync import Drive
drive = Drive()
drive.upload("this.png", "somewhere")
```

### Command Line

```shell
gsync README.md [--dir directory]
```

## Todo

- [ ] Add features other than uploading (currently it's not *sync*)
- [ ] Fast uploading (currently it's not fast)
- [ ] Enable logging
