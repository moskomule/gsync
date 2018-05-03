import argparse
from .drive import Drive


def upload(args):
    drive = Drive()
    for s in args.sources:
        drive.upload(s, args.dir)


def download(args):
    drive = Drive()
    for id in args.fileids:
        drive.download(id, args.output)


def list(args):
    drive = Drive()
    file_list = drive.list(args.parent, args.max + 1)
    if len(file_list) == 0:
        print("No file found!")
    else:
        max_length = max([len(f[0]) for f in file_list])
        for file in file_list[: args.max]:
            print(f"name: {file[0]:<{max_length + 5}} id: {file[1]}")
        if len(file_list) > args.max:
            print("and more...")


def main():
    p = argparse.ArgumentParser()
    p_sub = p.add_subparsers()

    # upload
    p_upload = p_sub.add_parser("upload")
    p_upload.add_argument("sources", nargs="+", help="Source _parents/files")
    p_upload.add_argument("--dir", default=None, help="Optional directory")
    p_upload.set_defaults(func=upload)

    # download
    p_download = p_sub.add_parser("download")
    p_download.add_argument("fileids", nargs="+", help="IDs")
    p_download.add_argument("--output", default=".", help="Output directory")
    p_download.set_defaults(func=download)

    # list
    p_list = p_sub.add_parser("list")
    p_list.add_argument("--max", type=int, default=10, help="Maximum number of contents to be shown")
    p_list.add_argument("--parent", default=None, help="Parent directory name")
    p_list.set_defaults(func=list)

    # parse
    args = p.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
