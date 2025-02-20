import shutil

def init(path: str):
    shutil.copy("skel", path)