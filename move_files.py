from distutils.dir_util import copy_tree

def copy_files(from_path):
    copy_tree(from_path, "myapp/static/images")
copy_files("images")
