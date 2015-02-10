__author__ = 'Jesse'
from tkinter import *
import urllib.request
import webbrowser


class Main:
    def __init__(self, master):

        #Creates userSearch Variable for storing user input
        global userSearch
        userSearch = StringVar()

        #sets window to master, sets title, and window size
        self.master = master
        self.master.title("Encyclopedia App")
        self.master.geometry("180x200")

        #Creates labels, buttons, and textbox
        lblTitle = Label(self.master, text="Encyclopedia", font=("Purisa", 12, "bold"), fg="green")
        lblSearch = Label(self.master, text="Search: ")
        txtBoxSearch = Entry(self.master, textvariable=userSearch)
        btnSearch = Button(self.master, text="Search", width=10, command=self.search)
        btnQuit = Button(self.master, text="Close", width=10, command=self.close)

        #Places labels, buttons, and textbox in grid format
        lblTitle.grid(row=1, columnspan=3)
        lblSearch.grid(row=2, column=1, sticky=W)
        txtBoxSearch.grid(row=2, column=2)
        btnSearch.grid(row=3, columnspan=3)
        btnQuit.grid(row=4, columnspan=3)


    #Search Function
    def search(self):
        global userSearch
        userSearch = userSearch.get()

        webbrowser.open("http://en.wikipedia.org/w/index.php?title=" +userSearch)


    #Function for closing the window
    def close(self):
        self.master.destroy()












# opener = urllib.request
# opener.addheaders = [('User-agent', 'Mozilla/5.0')]
# infile = opener.urlopen("http://en.wikipedia.org/w/index.php?title=" +userSearch)
# page = infile.read()







#Creates the root window and loops it
def main():
    root = Tk()
    Main(root)
    root.mainloop()

#Loops the code so the windows stay open
if __name__ == "__main__":
    main()