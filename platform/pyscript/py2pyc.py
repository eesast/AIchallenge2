#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import compileall
import os
import shutil

DIR = '.'

list_dirs = os.walk(DIR)
for root, _, files in list_dirs:
    py_files = filter(lambda name: name[-3:] == '.py', files)
    for py_file in py_files:
        file_path = os.path.join(root, py_file)
        if os.path.samefile(__file__, file_path):
            continue
        if compileall.compile_file(file_path, optimize=2):
            try:
                src= os.path.join(root, '__pycache__',
                                         py_file[:-3] + '.cpython-36.opt-2.pyc')
                shutil.move(src, file_path + 'c')
                os.remove(file_path)
            except:
                print('compile', file_path,
                      'error. Make sure Python VERSION == 3.6')
                exit()
        try:
            shutil.rmtree(os.path.join(root, '__pycache__'))
        finally:
            pass
