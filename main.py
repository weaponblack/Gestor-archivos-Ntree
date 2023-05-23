import os
from Model.FileInfo import *


def list_filesTree2(startpath):
    file_objects = []
    file_id = 0

    for root, dirs, files in os.walk(startpath):
        folder_name = os.path.basename(root)
        file_name = folder_name
        level = root.count(os.sep)
        file_path = os.path.join(root)
        file_path = os.path.dirname(file_path)
        file = FileInfo(file_name, file_id, file_path, level)
        file_objects.append(file)
        file_id += 1
        level_files = []  # Almacenar archivos en el mismo nivel
        for f in files:
            file = FileInfo(f, file_id, file_path, level + 1)
            level_files.append(file)

        # Asignar ID incremental a los archivos en el mismo nivel
        for level_file in level_files:
            level_file.id = file_id
            file_objects.append(level_file)
            file_id += 1

    return file_objects


def Ordenar(list_objects):
    list_objects = sorted(list_objects, key=lambda x: x.level)
    return list_objects


startpath = "C:\Root"
files = list_filesTree2(startpath)
files = Ordenar(files)

for file in files:
    ultima_palabra = file.path.split("\\")[-1]
    # print(file.name + " - " + str(file.id) + " Level: " + str(file.level) + " - " + ultima_palabra)
    print(file.name + " - " + str(file.id) + " Level: " + str(file.level) + " - " + file.path)
