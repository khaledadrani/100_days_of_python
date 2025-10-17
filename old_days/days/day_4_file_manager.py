from tkinter import *
from PIL import ImageTk, Image
import shutil         
import os
import easygui
from tkinter import filedialog
from tkinter import messagebox as mb

# Major functions of file manager

# open a file box window 
# when we want to select a file
def open_window():
    read=easygui.fileopenbox()
    return read

# open file function
def open_file():
    string = open_window()
    
    if string is None:
        return 

    try:
        os.startfile(string) #execute file 
    except:
        mb.showinfo('Confirmation', "File not found!")

# copy file function
def copy_file():
    source1 = open_window()
    destination1=filedialog.askdirectory()
    shutil.copy(source1,destination1) #copy file from source to destination
    mb.showinfo('confirmation', "File Copied !")

# delete file function
def delete_file():
    del_file = open_window()

    if del_file is None:
        return

    if os.path.exists(del_file):
        os.remove(del_file)             
    else:
        mb.showinfo('confirmation', "File not found !")

def enter_user_input(message="Enter a value",title="Value input",default="Enter here..."):
    
    value = easygui.enterbox(message,title,default)
    return value

# rename file function
def rename_file():
    chosenFile = open_window()

    if chosenFile is None:
        return 

    path1 = os.path.dirname(chosenFile)
    extension=os.path.splitext(chosenFile)[1]
    #print("Enter new name for the chosen file")
    try:
        new_name = enter_user_input("Enter new name for the chosen file","New File Name")
        if new_name is None:
            return
        path = os.path.join(path1, new_name+extension)
        print(path)
        os.rename(chosenFile,path) 
        mb.showinfo('confirmation', "File Renamed !")
    except Exception as err:
        mb.showerror('An Error has occured!',str(err))

# move file function
def move_file():
    source = open_window()
    if source is None:
        return
    destination =filedialog.askdirectory()
    if destination is None:
        mb.showerror('Error','You must select a destination!')

    try:
        if(source==destination):
            mb.showinfo('confirmation', "Source and destination are same")
        else:
            shutil.move(source, destination)  
            mb.showinfo('confirmation', "File Moved !")
    except Exception as err:
        mb.showerror('An Error has occured!',str(err))

# function to make a new folder
def make_folder():
    newFolderPath = filedialog.askdirectory()
    message = "Enter name of new folder"
    newFolder= enter_user_input(message,"New Folder Name")
    path = os.path.join(newFolderPath, newFolder)  
    os.mkdir(path)
    mb.showinfo('confirmation', "Folder created !")

# function to remove a folder
def remove_folder():
    delFolder = filedialog.askdirectory()
    if delFolder is None:
        return
    os.rmdir(delFolder)
    mb.showinfo('confirmation', "Folder Deleted!")

# function to list all the files in folder
def list_files():
    folderList = filedialog.askdirectory()
    sortlist=sorted(os.listdir(folderList))
    text = '\n'.join(sortlist)
    output = easygui.textbox(text=text)
    print(output)
    
    

#Creating the UI of our file manager

root = Tk()

# creating label and buttons to perform operations
Label(root, text="Simple File Manager", font=("Helvetica", 16), fg="blue").grid(row = 5, column = 2)

Button(root, text = "Open a File", command = open_file).grid(row=15, column =2)

Button(root, text = "Copy a File", command = copy_file).grid(row = 25, column = 2)

Button(root, text = "Delete a File", command = delete_file).grid(row = 35, column = 2)

Button(root, text = "Rename a File", command = rename_file).grid(row = 45, column = 2)

Button(root, text = "Move a File", command = move_file).grid(row = 55, column =2)

Button(root, text = "Make a Folder", command = make_folder).grid(row = 75, column = 2)

Button(root, text = "Remove a Folder", command = remove_folder).grid(row = 65, column =2)

Button(root, text = "List all Files in Directory", command = list_files).grid(row = 85,column = 2)



root.mainloop()

