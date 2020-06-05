import pyperclip
import sys
from tkinter import *
from tkinter import ttk
import hashlib
import requests
import string
import random


class Password:
    def __init__(self, phrase, size, password):
        self.phrase = " "
        self.size = ""
        self.password = " "


def lookup_pwned_api(pwd):
    """Returns hash and number of times password was seen in pwned database.
    Args:
        pwd: password to check
    Returns:
        A (sha1, count) tuple where sha1 is SHA-1 hash of pwd and count is number
        of times the password was seen in the pwned database.  count equal zero
        indicates that password has not been found.
    Raises:
        RuntimeError: if there was an error trying to fetch data from pwned
            database.
        UnicodeError: if there was an error UTF_encoding the password.
    """
    sha1pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
    head, tail = sha1pwd[:5], sha1pwd[5:]
    url = 'https://api.pwnedpasswords.com/range/' + head
    res = requests.get(url)
    if not res.ok:
        raise RuntimeError('Error fetching "{}": {}'.format(
            url, res.status_code))
    hashes = (line.split(':') for line in res.text.splitlines())
    count = next((int(count) for t, count in hashes if t == tail), 0)
    return sha1pwd, count

def char_generator(size, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def gen_pass(input,psswrd,length,rw):
    length=10
    new_string = ''
    input =  input.replace(" ", "")
    replacements = (('a','4'), ('e','3'),('i','!'), ('o','0'), ('t','+'),('u',"U"),('l','1'))
    for old, new in replacements:
        input = input.replace(old, new)

    #Cuts down password if it's too long
    input = (input[:length]) if len(input) > length else input

    #Generates additional characters for password if it's too short
    if(len(input) < length):
        temp = length - len(input)
        new_string= char_generator(temp) 
        print(new_string)        

    new_string = input + new_string

    #Checks to see if it's been cracked before
    sha1pwd, count = lookup_pwned_api(new_string)
    if count:
        rw.passlbl.config(text="Bad Password. Run Again.")
        psswrd.password = ''
        return 0
        
    psswrd.password = new_string
    return 1


def copy_to_clipboard(str):
    pyperclip.copy(str)
    pyperclip.paste(str)

def copy_clicked(str):
    copy_to_clipboard(str)


class ResizableWindow:
    def __init__(self, parent,psswrd):
        self.parent = parent
        self.f1_style = ttk.Style()
        self.f1_style.configure('My.TFrame', background='#607D8B')
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
        psswrd.size = rw.size.get()
        print(psswrd.size)
        
        #Convert length to int somehow 
        length = psswrd.size
        if(length == ''):
            length=10
        else:
            length = int(length)
        
        state = gen_pass(rw.name.get(),psswrd,length,rw)
        if(state == 1):
            rw.passlbl.config(text=psswrd.password)


def main(argv):
    root = Tk()
    root.title("Password Generator")
    psswrd = Password(" ", '10', " ")
    rw = ResizableWindow(root,psswrd)
    root.mainloop()
    
if __name__ == "__main__":
    main(sys.argv)