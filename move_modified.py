import pathlib
import os
import datetime
from glob import glob
from shutil import copyfile


def loadtime():
    return datetime.datetime.fromtimestamp(float(pathlib.Path("lastest_time").read_text()))


def get_file_path_only(src_folder, full_path):
    return os.path.relpath(full_path, src_folder)


def move_to_export_folder(list_files, src_folder, dest_folder):
    pathlib.Path(dest_folder).mkdir(parents=True, exist_ok=True)
    for f in list_files:
        pf = pathlib.Path(f)
        file_path_only = get_file_path_only(src_folder, f)

        if pf.is_dir():
            full_dir_path = os.path.join(dest_folder, file_path_only)
            pathlib.Path(full_dir_path).mkdir(parents=True, exist_ok=True)
            print("DIR", f, full_dir_path)
        elif pf.is_file():
            dest_file = os.path.join(dest_folder, file_path_only)
            copyfile(f, dest_file)
            print("FILE", f, dest_file)


if __name__ == "__main__":
    src_d = "d:/workspace/testarti/download"
    dest_d = "d:/workspace/testarti/export"
    src_d_all_files_pattern = src_d + "/**"

    more_than_timestamp = datetime.datetime.fromisoformat("2021-05-21T12:26:59")
    #more_than_timestamp = loadtime()
    newest_time = more_than_timestamp

    print(more_than_timestamp)
    paths = glob(src_d_all_files_pattern, recursive=True)
    files_to_move = []
    for p in paths:
        fp = pathlib.Path(p)
        m_time = datetime.datetime.fromtimestamp(fp.stat().st_mtime)
        if m_time > more_than_timestamp:
            print(p, m_time)
            files_to_move.append(p)
            if m_time > newest_time:
                newest_time = m_time

    move_to_export_folder(files_to_move, src_d, dest_d)
    #pathlib.Path("lastest_time").write_text(str(newest_time.timestamp()))