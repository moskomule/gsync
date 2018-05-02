import argparse
from .drive import Drive


def parse_arguments():
    p = argparse.ArgumentParser()
    p.add_argument("source", help="Source directory/file path")
    p.add_argument("--dir", default=None, help="Optional directory name")
    args = p.parse_args()
    return args


def main():
    args = parse_arguments()
    drive = Drive()
    drive.upload(args.source, args.dir)
