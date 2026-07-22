import os
import ctypes
import tkinter

#load in the c libary
base_path = os.path.abspath(os.path.dirname(__file__))
c_src = ctypes.CDLL(os.path.join(base_path, "clib.so"))

current_dir_contents: list = []
current_dir_data: list = []

#setup decorator and type for python function
CALLBACK = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_char_p)

#c function type definitions
c_src.list_current_dir.argtypes = [ctypes.c_char_p, CALLBACK]

#function to append the files to the list in c
@CALLBACK
def python_append_callback(item, type):
   converted_item = item.decode("utf-8")
   current_dir_contents.append(converted_item)
   current_dir_data.append(type.decode("utf-8"))

#class for the gui
class Main_Page:
   def __init__(self):
      self.root = tkinter.Tk()
      self.root.minsize(700, 400)
      self.root.maxsize(700, 400)
      self.root.geometry("700x400+50+50")
      self.root.configure(background="#373837")
      self.root.title("File Manager")
      self.header_shadow = tkinter.Frame(self.root, width=700, height=40, bg="#646665")
      self.header_shadow.place(x=0, y =3)
      self.header = tkinter.Frame(self.root, width=700, height=40, bg="#373837").pack()

   def load_files(self):
      dark = "#373837"
      light = "#636463"
      current = dark
      for i, content in enumerate(current_dir_contents):
         if current == dark: current = light
         else: current = dark
         file_block = tkinter.Frame(self.root, width=80, height=20, bg=current)
         file_block.propagate(flag=False)
         file_block.pack(fill="x", pady=1)
         file_block.bind("<Double-1>", self.change_dir)
         file_text = tkinter.Label(file_block, text=content, bg=current, fg="#f8f6f6", font=("arial", 12 ,"bold"), anchor="w")
         file_text.pack(expand=True, side="left", anchor="w", padx=10)
         file_text.bind("<Double-1>", self.change_dir)
         type_text = tkinter.Label(file_block, text=current_dir_data[i], bg=current, fg="#f8f6f6", font=("arial", 12 ,"bold"), anchor="e")
         type_text.pack(expand=True, side="right", anchor="e", padx=10)
         type_text.bind("<Double-1>", self.change_dir)

   def change_dir(self, event):
      global current_dir_contents, current_dir_data
      current = int(str(event.widget)[7]) - 3
      temp_arr = [current_dir_contents[current], current_dir_data[current]]
      if temp_arr[1] == "folder":
         current_dir_contents = []
         dir = os.getcwd() + "/" + temp_arr[0] 
         print(dir)
         c_src.list_current_dir(dir.encode("utf-8"), python_append_callback)
         main_page.load_files()
      else:
         pass

if __name__ == "__main__":
   #call c function
   c_src.list_current_dir(".".encode("utf-8"), python_append_callback)

   #gui loop
   main_page = Main_Page()
   main_page.load_files()
   main_page.root.mainloop()