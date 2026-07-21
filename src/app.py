import os
import ctypes
import tkinter

#load in the c libary
base_path = os.path.abspath(os.path.dirname(__file__))
c_src = ctypes.CDLL(os.path.join(base_path, "clib.so"))

current_dir_contents: list = []

#setup decorator and type for python function
CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_char_p)

#c function type definitions
c_src.list_current_dir.argtypes = [ctypes.c_char_p, CALLBACK]

#function to append the files to the list in c
@CALLBACK
def python_append_callback(item):
   converted_item = item.decode("utf-8")
   current_dir_contents.append(converted_item)

#call c function
c_src.list_current_dir(".".encode("utf-8"), python_append_callback)