import os
import fnmatch


def get_json_paths(root_path):
    json_paths = [
        os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(root_path)
        for f in fnmatch.filter(files, '*.json')
    ]
    return json_paths
