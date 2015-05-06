__author__ = 'Andre'
from tkinter import *
import webbrowser
from tweepy import Stream
from tweepy import OAuthHandler
import threading
import sqlite3
from flickrSearch import flickrSearch
from twitterSearch import Listener
# create a new database and connect to it
cxn = sqlite3.connect('EncyclopediaDB')
# initialize a cursor object to run execute commands on the connected database.
cur = cxn.cursor()
try:
    # create the table and fill it with data
    cur.execute('CREATE TABLE flickr(search VARCHAR(50), result VARCHAR(200))')
    print("Successfully created the flickr table.")
    cur.execute('CREATE TABLE wiki(search VARCHAR(50), result VARCHAR(200))')
    print("Successfully created the wiki table.")
    cur.execute('CREATE TABLE twitter(search VARCHAR(50), result VARCHAR(200))')
    print("Successfully created the twitter table.")
except sqlite3.OperationalError:
    print("The table could not be created or exists already")

# Read the Key and secret from a file and add it to an array for security
# read out of array for authentication
twitterAuth = open('twitterAuth')
authArray = []
for line in twitterAuth:
    key = line.strip("\n")
    authArray.append(key)
twitterAuth.close()

cKey = authArray[0]
cSecret = authArray[1]
aToken = authArray[2]
aSecret = authArray[3]

#Sets consumer keys and access tokens
authorize = OAuthHandler(cKey, cSecret)
authorize.set_access_token(aToken, aSecret)

#Boolean variable for the search thread that sets the variable to true while running and false when you quit the program
alive = True

class Main(Frame):

    def __init__(self, master):

        Frame.__init__(self, master)

        #Creates userSearch Variable for storing user input and creates int vars for checkboxes
        self.userSearch = StringVar()
        self.chkWiki = IntVar()
        self.chkFlickr = IntVar()
        self.chkTwitter = IntVar()
        self.flickrData = 10

        #sets window to master, sets title, and window size
        self.master = master
        self.master.title("Encyclopedia App")
        self.master.resizable(width=FALSE, height=FALSE)
        self.canvas = Canvas(self.master, borderwidth=0, highlightthickness=0)
        self.frame = Frame(self.canvas)
        self.vertScrollBar = Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vertScrollBar.set)

        #Puts scrollbar and canvas in grid and creates window
        self.vertScrollBar.grid(row=0, column=10, sticky="NS")
        self.canvas.grid(row=0, column=0)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw", tags="self.frame")

        widgetArray = []
        # Creates Widgets and put them in an array to put them onto the window
        lblTitle = Label(self.frame, text="Searchster", font="Times 18 bold", fg="green")
        widgetArray.append(lblTitle)
        lblSearch = Label(self.frame, text="Search: ", font="Times 10")
        widgetArray.append(lblSearch)
        txtBoxSearch = Entry(self.frame, width=17, textvariable=self.userSearch)
        widgetArray.append(txtBoxSearch)
        btnSearch = Button(self.frame, text="Search", width=14, command=self.threadedSearch)
        widgetArray.append(btnSearch)
        btnClear = Button(self.frame, text="Clear", width=14, command=self.clear)
        widgetArray.append(btnClear)
        btnQuit = Button(self.frame, text="Close", width=14, command=self.close)
        widgetArray.append(btnQuit)
        chkBtnWikipedia = Checkbutton(self.frame, text="Wikipedia", variable=self.chkWiki, justify=LEFT)
        widgetArray.append(chkBtnWikipedia)
        chkBtnFlickr = Checkbutton(self.frame, text="Flickr", variable=self.chkFlickr, justify=LEFT)
        widgetArray.append(chkBtnFlickr)
        chkBtnTwitter = Checkbutton(self.frame, text="Twitter", variable=self.chkTwitter, justify=LEFT)
        widgetArray.append(chkBtnTwitter)
        lblBlankLabel = Label(self.frame, text="                  ")
        widgetArray.append(lblBlankLabel)
        lblWikiLabel = Label(self.frame, text="Wikipedia:", font="Times 10 bold")
        widgetArray.append(lblWikiLabel)
        lblFlickrLabel = Label(self.frame, text="Flickr:", font="Times 10 bold")
        widgetArray.append(lblFlickrLabel)
        lblTwitterLabel = Label(self.frame, text="Twitter:", font="Times 10 bold")
        widgetArray.append(lblTwitterLabel)

        row = 1
        columns = 2
        #Places Widgets in grid format
        for widget in widgetArray:

            if widget == lblSearch:
                widget.grid(row=row, column=1, sticky=E)
                row -= 1
            elif widget == lblBlankLabel:
                widget.grid(row=row, column=columns)
            elif widget == lblTwitterLabel:
                widget.grid(row=25, column=columns, sticky=W)
            else:
                widget.grid(row=row, column=columns, sticky=W)
            if row == 11 or row == 5:
                row += 1
            row += 1


        #Initialize the Labels and set there position in the grid so they can be reset repeatedly
        self.lblDisplayWikiURL = Label(self.frame, text="")
        self.lblDisplayFlickrURL = Label(self.frame, text="")
        self.lblDisplayTwitterURL = Label(self.frame, text="")
        self.lblDisplayFlickrData = Label(self.frame, text="")
        self.lblDisplayTwitterData = Label(self.frame, text="")
        self.lblDisplayWikiURL.grid(row=12, column=2, sticky=W)
        self.lblDisplayFlickrURL.grid(row=14, column=2, sticky=W)
        self.lblDisplayTwitterURL.grid(row=26, column=2, sticky=W)

        self.frame.bind("<Configure>", self.OnFrameConfigure)

    def OnFrameConfigure(self, event):
        #Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), height=400, width=600)

    #Wikipedia Callback Event
    def wikicallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("http://en.wikipedia.org/w/index.php?title=" + str(userSearch))

    #Flickr Callback Event
    def flickrcallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("http://www.flickr.com/search/?q=" + str(userSearch))

    #Opens the flickr image
    def flickrDisplayPhotocallback(self, event):
        saveFileFlickr = open('flickDB.csv')
        readFileFlickr = saveFileFlickr.read()
        saveFileFlickr.close()
        webbrowser.open(readFileFlickr)


    #Twitter Callback Event
    def twittercallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("http://twitter.com/search?q=" + str(userSearch) + "&src=typd")

    #Threading for search function
    def threadedSearch(self):

        #Search Function
        def search():

            #Gets text from search textbox
            userSearch = self.userSearch.get()

            #Wikipedia Checkbox
            if self.chkWiki.get():
                #webbrowser.open("http://en.wikipedia.org/w/index.php?title=" + str(userSearch))

                #Displays Wikipedia hyperlink in label and binds it to left-click event and places in grid
                self.lblDisplayWikiURL.config(text="http://en.wikipedia.org/w/index.php?title=" + str(userSearch), font="Times 10", fg="Blue", cursor="hand2")
                self.lblDisplayWikiURL.bind('<Button-1>', self.wikicallback)

            #Flickr Checkbox
            if self.chkFlickr.get():
                #sets the userSearchFlickr to the userSearch get method
                flickrPull = flickrSearch(userSearchFlickr=str(userSearch))
                flickrPull.userSearch = userSearch
                #webbrowser.open("http://www.flickr.com/search/?q=" + str(userSearch))

                #Opens the flickDB files and reads them for displaying in the lblDisplayFlickrData labels below, and then closes it
                saveFileFlickr = open('flickDB.csv')
                readFileFlickr = saveFileFlickr.read()
                saveFileFlickr.close()

                #Displays Flickr hyperlink in label and binds it to left-click event and places in grid
                self.lblDisplayFlickrURL.config(text="http://www.flickr.com/search/?q=" + str(userSearch), fg="Blue", cursor="hand2")
                self.lblDisplayFlickrURL.bind('<Button-1>', self.flickrcallback)

                self.lblDisplayFlickrData.config(text=readFileFlickr, font="Times 10", fg="Blue", cursor="hand2", justify=LEFT)
                self.lblDisplayFlickrData.bind('<Button-1>', self.flickrDisplayPhotocallback)
                self.lblDisplayFlickrData.grid(row=15, column=2, sticky=W)

            #Twitter Checkbox
            if self.chkTwitter.get():
                #webbrowser.open("http://twitter.com/search?q=" + str(userSearch) + "&src=typd")1q

                #Streams the tweets using the Listener class and searches with the criteria of the userSearch
                twitterStream = Stream(authorize, Listener())

                #Filters the twitter results with the user search input
                twitterStream.filter(track=[userSearch])

                #Opens the tDB3 file and reads for displaying in the lblDisplayTwitterData below, and then closes it
                saveFile2 = open('tDB3.csv')
                readFile = saveFile2.read()
                saveFile2.close()

                #Displays Twitter hyperlink in label and binds it to left-click event and places in grid
                self.lblDisplayTwitterURL.config(text="http://twitter.com/search?q=" + str(userSearch) + "&src=typd", fg="Blue", cursor="hand2")
                self.lblDisplayTwitterURL.bind('<Button-1>', self.twittercallback)
                self.lblDisplayTwitterData.config(text=readFile, font="Times 10", justify=LEFT)
                self.lblDisplayTwitterData.grid(row=27, column=2, sticky=W)


        multi = threading.Thread(target=search)
        multi.start()
        # fill and show the database has to be outside of the thread otherwise it is not working
        self.fillDB()
        self.showDB()

    def fillDB(self):
        userSearch = self.userSearch.get()
        flickrAddress = "http://www.flickr.com/search/?q=" + str(userSearch)
        wikiAddress = "http://en.wikipedia.org/w/index.php?title=" + str(userSearch)
        twitterAddress = "http://twitter.com/search?q=" + str(userSearch) + "&src=typd"
        cur.execute('INSERT INTO flickr VALUES(?, ?);', (userSearch, flickrAddress))
        cur.execute('INSERT INTO wiki VALUES(?, ?);', (userSearch, wikiAddress))
        cur.execute('INSERT INTO twitter VALUES(?, ?);', (userSearch, twitterAddress))
        cxn.commit()
        print('Successfully committed')

    def showDB(self):

        cur.execute('SELECT * FROM flickr')
        for eachUser in cur.fetchall():
            print("Flickr table.")
            print(eachUser)

        cur.execute('SELECT * FROM wiki')
        for eachUser in cur.fetchall():
            print("Wiki table.")
            print(eachUser)

        cur.execute('SELECT * FROM twitter')
        print("Twitter table.")
        for eachUser in cur.fetchall():

            print(eachUser)



    #Function for clearing the labels
    def clear(self):
        self.lblDisplayWikiURL.config(text="")
        self.lblDisplayFlickrURL.config(text="")
        self.lblDisplayTwitterURL.config(text="")
        self.lblDisplayFlickrData.grid_forget()
        self.lblDisplayTwitterData.grid_forget()

    #Function for closing the window
    def close(self):
        alive = False
        cur.execute('DROP TABLE flickr')
        cur.execute('DROP TABLE wiki')
        cur.execute('DROP TABLE twitter')
        cur.close()
        cxn.close()
        self.master.destroy()


def main():
    root = Tk()
    Main(root)
    root.mainloop()


#Loops the code so the windows stay open
if __name__ == "__main__":
    main()
