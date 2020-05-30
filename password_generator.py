import pyperclip
import sys
from tkinter import *
from tkinter import ttk

class Password:
    def __init__(self, phrase, size, password):
        self.phrase = phrase
        self.size = 10
        self.password = " "


def gen_pass(input,psswrd):
    psswrd.password = "password" + input.replace(" ", "")

def copy_to_clipboard(str):
    pyperclip.copy(str)
    pyperclip.paste(str)

def copy_clicked(str):
    copy_to_clipboard(str)



class ResizableWindow:
    def __init__(self, parent,psswrd):
        self.parent = parent
        self.f1_style = ttk.Style()
        self.f1_style.configure('My.TFrame', background='#334333')
        self.f1 = ttk.Frame(self.parent, style='My.TFrame', padding=(3, 3, 12, 12))  
        self.f1.grid(column=0, row=0, sticky=(N, S, E, W))  
        
        self.namelbl = ttk.Label(self.f1, text="Phrase")
        self.name = ttk.Entry(self.f1)
        self.namelbl.grid(column=0, row=0, columnspan=2, sticky=(N,W), padx=5)  
        self.name.grid(column=0, row=1, columnspan=2, sticky=(N, E, W), pady=5, padx=5)  # added sticky, pady, padx

        self.passlbl = Label(self.f1, height=2,width=30,justify=CENTER)
        self.copy_btn = Button(self.f1, text="Copy to Clipboard",command=lambda: copy_clicked(psswrd.password))
        self.passlbl.grid(column=4,row=1, padx=5, pady=5)
        self.copy_btn.grid(column=2, row=35, padx=5, pady=5)

        self.runbtn = ttk.Button(self.f1, text="Run",command=lambda: run_clicked(self,psswrd))
        self.runbtn.grid(column=2, row=5, padx=5, pady=5, sticky=(N,E,W))   

        self.sizelbl = ttk.Label(self.f1, text="Size")
        self.size = ttk.Spinbox(self.f1,from_= 10, to= 100, width=19)
        self.sizelbl.grid(column=0,row=2,columnspan=2,sticky=(N,W),padx=5)
        self.size.grid(column=0,row=3,columnspan=2,sticky=(N, E, W),pady=5, padx=5)

        #Resizes configurations
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        self.f1.columnconfigure(0, weight=3)
        self.f1.columnconfigure(1, weight=3)
        self.f1.columnconfigure(2, weight=3)
        self.f1.columnconfigure(3, weight=1)
        self.f1.columnconfigure(4, weight=1)
        self.f1.rowconfigure(1, weight=1)



def run_clicked(rw,psswrd):
        gen_pass(rw.name.get(),psswrd)
        rw.passlbl.config(text=psswrd.password)
        print(psswrd.password) 


def main(argv):
    root = Tk()
    root.title("Password Generator")
    psswrd = Password(" ", 0, " ")
    rw = ResizableWindow(root,psswrd)
    root.mainloop()
    
if __name__ == "__main__":
    main(sys.argv)