import os
from Model.FileInfo import *


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def list_filesTree(startpath):
    file_objects = []
    file_id = 1

    for root, dirs, files in os.walk(startpath):
        folder_name = os.path.basename(root)
        file_name = folder_name
        file_path = os.path.join(root, file_name)
        file = FileInfo(file_name, file_id, file_path)
        file_objects.append(file)
        file_id += 1
        for f in files:
            file = FileInfo(f, file_id, file_path)
            file_objects.append(file)
            file_id += 1

    return file_objects


def list_filesTree2(startpath):
    file_objects = []
    file_id = 1

    for root, dirs, files in os.walk(startpath):
        folder_name = os.path.basename(root)
        file_name = folder_name
        file_path = os.path.join(root, file_name)
        file = FileInfo(file_name, file_id, file_path)
        file_objects.append(file)
        file_id += 1

        level_files = []  # Almacenar archivos en el mismo nivel
        for f in files:
            file = FileInfo(f, file_id, file_path)
            level_files.append(file)
            file_id += 1

        # Asignar ID incremental a los archivos en el mismo nivel
        for level_file in level_files:
            level_file.id = file_id
            file_objects.append(level_file)
            file_id += 1

    return file_objects


startpath = "C:\Root"
#list_files(startpath)
# files = list_filesTree(startpath)
files = list_filesTree2(startpath)

for file in files:
    print(file.name + " - " + str(file.id) )
