__author__ = 'Jesse'
from tkinter import *
import urllib.request
import webbrowser


class Main:
    def __init__(self, master):

        #Creates userSearch Variable for storing user input
        self.userSearch = StringVar()

        #sets window to master, sets title, and window size
        self.master = master
        self.master.title("Encyclopedia App")
        self.master.geometry("500x230")

        #Creates labels, buttons, and textbox
        lblTitle = Label(self.master, text="Searchster", font=("Times 16 bold"), fg="green", )
        lblSearch = Label(self.master, text="Search: ", font=("Times 10"))
        txtBoxSearch = Entry(self.master, width=17, textvariable=self.userSearch)
        btnSearch = Button(self.master, text="Search", width=14, command=self.search)
        btnQuit = Button(self.master, text="Close", width=14, command=self.close)
        lblWikiLabel = Label(self.master, text="           Wikipedia URL", font=("Times 10 bold"))
        lblFlickrLabel = Label(self.master, text="            Flickr URL", font=("Times 10 bold"))
        lblTwitterLabel = Label(self.master, text="          Twitter URL", font=("Times 10 bold"))

        #Places labels, buttons, and textbox in grid format
        lblTitle.grid(row=1, column=2)
        lblSearch.grid(row=2, column=1, sticky=E)
        txtBoxSearch.grid(row=2, column=2)
        btnSearch.grid(row=3, column=2)
        btnQuit.grid(row=4, column=2)
        lblWikiLabel.grid(row=1, column=4, sticky=W)
        lblFlickrLabel.grid(row=3, column=4, sticky=W)
        lblTwitterLabel.grid(row=5, column=4, sticky=W)


    #Wikipedia Callback Event
    def wikicallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("http://en.wikipedia.org/w/index.php?title=" + str(userSearch))

    #Flickr Callback Event
    def flickrcallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("https://www.flickr.com/search/?q=" + str(userSearch))

    #Twitter Callback Event
    def twittercallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("https://twitter.com/search?q=" + str(userSearch) + "&src=typd")


    #Search Function
    def search(self):
        #Gets text from search textbox
        userSearch = self.userSearch.get()

        #Opens the webbrowsers
        webbrowser.open("http://en.wikipedia.org/w/index.php?title=" + userSearch)
        webbrowser.open("https://www.flickr.com/search/?q=" + userSearch)
        webbrowser.open("https://twitter.com/search?q=" + userSearch + "&src=typd")

        #Displays Wikipedia hyperlink in label and binds it to left-click event and places in grid
        lblDisplayWikiURL = Label(self.master, text="http://en.wikipedia.org/w/index.php?title=" + userSearch, fg="Blue", cursor="hand2")
        lblDisplayWikiURL.bind('<Button-1>', self.wikicallback)
        lblDisplayWikiURL.grid(row=2, column=4, sticky=W)

        #Displays Flickr hyperlink in label and binds it to left-click event and places in grid
        lblDisplayFlickrURL = Label(self.master, text="https://www.flickr.com/search/?q=" + userSearch, fg="Blue", cursor="hand2")
        lblDisplayFlickrURL.bind('<Button-1>', self.flickrcallback)
        lblDisplayFlickrURL.grid(row=4, column=4, sticky=W)

        #Displays Twitter hyperlink in label and binds it to left-click event and places in grid
        lblDisplayTwitterURL = Label(self.master, text="https://twitter.com/search?q=" + userSearch + "&src=typd", fg="Blue", cursor="hand2")
        lblDisplayTwitterURL.bind('<Button-1>', self.twittercallback)
        lblDisplayTwitterURL.grid(row=6, column=4, sticky=W)



    #Function for closing the window
    def close(self):
        self.master.destroy()




#Creates the root window and loops it
def main():
    root = Tk()
    Main(root)
    root.mainloop()

#Loops the code so the windows stay open
if __name__ == "__main__":
    main()