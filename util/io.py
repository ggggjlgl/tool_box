import os


def find_files(directory: str):
    for entry in os.scandir(directory):
        if entry.is_dir(follow_symlinks=False):
            yield from find_files(entry.path)
        else:
            yield os.path.normpath(os.path.join(directory, entry.name))


def get_files_by_dir(directory: str):
    files = list(find_files(directory))
    files.sort(key=len, reverse=True)
    return files


def find_dirs(directory: str):
    for entry in os.scandir(directory):
        if entry.is_dir(follow_symlinks=False):
            yield os.path.normpath(entry.path)
            yield from find_dirs(entry.path)


def get_dirs_by_dir(directory: str):
    dirs = list(find_dirs(directory))
    dirs.sort(key=len, reverse=True)
    return dirs


def modify_file_path(org_abs_path: str, new_file_name: str):
    os.rename(os.path.normpath(org_abs_path),
              os.path.normpath(os.path.join(os.path.dirname(org_abs_path), new_file_name)))


def get_new_target_path(origin_path: str, want_target_path: str, exist_func=os.path.exists):
    if exist_func(want_target_path):
        tmp = origin_path.replace('\\', '-').replace('/', '-')
        ps = f'-from-{tmp}'
        font, back = os.path.splitext(want_target_path)
        return os.path.normpath(font + ps + back)
    else:
        return want_target_path


def get_target_path_with_dn(origin_path: str, target_dir: str):
    tmp = origin_path.replace('\\', '-').replace('/', '-')
    ps = f'-from-{tmp}'
    base_name = os.path.basename(origin_path)
    font, back = os.path.splitext(base_name)
    new_base_name = font + ps + back
    return os.path.normpath(os.path.join(target_dir, new_base_name))
