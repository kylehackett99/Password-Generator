import pyperclip
import sys
from tkinter import *


class Password:
    def __init__(self, phrase, size, password):
        self.phrase = phrase
        self.size = size
        self.password = password 


def gen_pass(input,self):
    self.password = "password" + input.replace(" ", "")


def copy_to_clipboard(str):
    #str = self.password
    pyperclip.copy(str)
    pyperclip.paste(str)

def copy_clicked(str):
    copy_to_clipboard(str)

def main(argv):
    window = Tk()
    window.title("Password Generator")
    window.geometry('350x200')
    self = Password(" ",0," ")
    genned = FALSE

    Label(window, text=" Containing Phrase").grid(row=10)
    Label(window, text="Size").grid(row=12)

    phrase = Entry(window)
    size_of_pass = Spinbox(window, from_= 10, to= 100, width=19)

    phrase.grid(row=10, column=1)
    size_of_pass.grid(row=12, column=1)

    def run_clicked():
            gen_pass(phrase.get(),self)
            lbl = Label(window, text = "Password: " + self.password).grid(row=30, column=1);
            self.genned = TRUE
            copy_btn = Button(window, text="Copy to Clipboard", command=copy_clicked(self.password))
            copy_btn.grid(column=1, row=35)
            

    run_btn = Button(window, text="Generate", command=run_clicked)
    run_btn.grid(column=1, row=15)
    print("!")
    


   

    

    window.mainloop()
    pass

if __name__ == "__main__":
    main(sys.argv)