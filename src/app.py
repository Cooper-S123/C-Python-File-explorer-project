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

class Main_Page:
   def __init__(self):
      self.root = tkinter.Tk()
      self.root.minsize(700, 400)
      self.root.maxsize(700, 400)
      self.root.geometry("700x400+50+50")
      self.root.configure(background="white")
      self.root.title("File Manager")
      self.header_shadow = tkinter.Frame(self.root, width=700, height=40, bg="#646665")
      self.header_shadow.place(x=0, y =3)
      self.header = tkinter.Frame(self.root, width=700, height=40, bg="#c9c8c1").pack()

#call c function
c_src.list_current_dir(".".encode("utf-8"), python_append_callback)

if __name__ == "__main__":
   main_page = Main_Page()
   main_page.root.mainloop()