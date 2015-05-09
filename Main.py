__author__ = 'Andre'

from tkinter import *
from tkinter import messagebox
import webbrowser
from tweepy import Stream
from tweepy import OAuthHandler
import threading
from flickrSearch import flickrSearch
from twitterSearch import Listener
from PIL import ImageTk
from wikipedia import *
import textwrap

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
        self.imageArray = []

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
            # Put search label left next to text box
            if widget == lblSearch:
                widget.grid(row=row, column=1, sticky=E)
                row -= 1
            # have twitter label after flicker pictures
            elif widget == lblTwitterLabel:
                widget.grid(row=27, column=columns, sticky=W)
            # give an extra space for the wiki text and then put the flickr label
            elif widget == lblFlickrLabel:
                widget.grid(row=14, column=columns, sticky=W)
            # otherwise put all the widgets one after another
            else:
                widget.grid(row=row, column=columns, sticky=W)
            row += 1


        #Initialize the Labels and set there position in the grid so they can be reset repeatedly
        self.lblDisplayWikiURL = Label(self.frame, text="")
        self.lblDisplayFlickrURL = Label(self.frame, text="")
        self.lblDisplayTwitterURL = Label(self.frame, text="")
        self.lblDisplayWikiData = Label(self.frame, text="")
        self.lblDisplayFlickrData = Label(self.frame, text="")
        self.lblDisplayTwitterData = Label(self.frame, text="")
        self.lblDisplayWikiURL.grid(row=12, column=2, sticky=W)
        self.lblDisplayWikiData.grid(row=13, column=2, sticky=W)
        self.lblDisplayFlickrURL.grid(row=16, column=2, sticky=W)
        self.lblDisplayTwitterURL.grid(row=28, column=2, sticky=W)

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
    def flickrDisplayPhotocallback(self, event, url):
        webbrowser.open(url)


    #Twitter Callback Event
    def twittercallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("http://twitter.com/search?q=" + str(userSearch) + "&src=typd")

    #Threading for search function
    def threadedSearch(self):

        #Search Function
        def search():
            # clear the last search in case it hasn't been cleared manually.
            self.clear()
            #Gets text from search textbox
            userSearch = self.userSearch.get()

            #Wikipedia Checkbox
            if self.chkWiki.get():

                #Displays Wikipedia hyperlink in label and binds it to left-click event and places in grid
                self.lblDisplayWikiURL.config(text="http://en.wikipedia.org/w/index.php?title=" + str(userSearch), font="Times 10", fg="Blue", cursor="hand2")
                # display the first two sentences of the wiki page using the wikipedia api
                # http://stackoverflow.com/questions/4460921/extract-the-first-paragraph-from-a-wikipedia-article-python
                try:
                    # get the first two sentences from wikipedia
                    summary = wikipedia.summary(userSearch, sentences=2)
                    # format them so it is not one continuouse line
                    # using the wrap function of the TextWrap class to split ino a list with 70 chars each
                    wrapped = textwrap.wrap(summary, width=90)
                    # since the wrap method returns a list, we have to reasemble the text
                    # and ad the wanted newline characters
                    wrappedSummary = ""
                    for part in wrapped:
                        wrappedSummary += part + "\n"

                    self.lblDisplayWikiData.config(text=wrappedSummary, font="Times 10", justify=LEFT)
                # Catch disambiguous pages
                except DisambiguationError:
                    messagebox.showwarning("Warning", "Articles are ambiguous. Try something more specific or check the Wiki page")
                # Catch page not found
                except PageError:
                    messagebox.showerror("Error", "Sorry, but there is no such page on Wikipedia")
                # Catch no connection as general error because it cant be cought
                # as connection error because too many processes
                except:
                    messagebox.showerror("Error", "Could not connect to Wikipedia. Please check your Internet connection.")
                self.lblDisplayWikiURL.bind('<Button-1>', self.wikicallback)

            #Flickr Checkbox
            if self.chkFlickr.get():
                #sets the userSearchFlickr to the userSearch get method
                flickrPull = flickrSearch(userSearchFlickr=str(userSearch))
                flickrPull.userSearch = userSearch


                #Displays Flickr hyperlink in label and binds it to left-click event and places in grid
                self.lblDisplayFlickrURL.config(text="http://www.flickr.com/search/?q=" + str(userSearch), fg="Blue", cursor="hand2")
                self.lblDisplayFlickrURL.bind('<Button-1>', self.flickrcallback)

                # Presets the counters for the photo getter
                row = 17
                count = 0
                urlNr = 0
                # checks if the twitter checkbox is clicked and if so, sets the column for
                # every other image different, to have it evenly displayed (otherwise pictures out of frame)
                if self.chkTwitter.get() or self.chkWiki.get():
                    columns = 2
                else:
                    columns = 3


                #Gets the images that are stored in the imageArray, then opens them with PIL, and then displays them in a label
                #Also binds the images to the URLS so they can be clicked on and open URL
                for image in flickrPull.imageArray:
                    count += 1
                    showImage = ImageTk.PhotoImage(image)
                    url = flickrPull.flickrArray[urlNr]
                    urlNr += 1


                    if count == 1:
                        self.imageLabel = Label(self.frame, image=showImage, cursor="hand2")
                        self.imageLabel.image = showImage #keep a reference so that garbage collection doesn't make transparent
                        self.imageLabel.grid(row=row, column=2, sticky=W)
                        self.imageArray.append(self.imageLabel)     #store the widgets in an array to be able to clear them out later
                        self.imageLabel.bind('<Button-1>', lambda event, arg=url: self.flickrDisplayPhotocallback(event, arg))


                    elif count == 2:
                        self.imageLabel2 = Label(self.frame, image=showImage, cursor="hand2")
                        self.imageLabel2.image = showImage #keep a reference so that garbage collection doesn't make transparent
                        self.imageLabel2.grid(row=row, column=columns, sticky=E)
                        self.imageArray.append(self.imageLabel2)
                        self.imageLabel2.bind('<Button-1>', lambda event, arg=url: self.flickrDisplayPhotocallback(event, arg))
                        row += 1
                        count = 0



            #Twitter Checkbox
            if self.chkTwitter.get():

                #Streams the tweets using the Listener class and searches with the criteria of the userSearch
                twitterStream = Stream(authorize, Listener())
                try:
                # Try Filters the twitter results with the user search input and retrieve accordingly
                    twitterStream.filter(track=[userSearch])
                # we catch a runtime error because it does not throw any specific exception
                # due to the fact that many processes are running and tweepys handling is not good
                except RuntimeError:
                    messagebox.showerror("Error", "Could not retrieve anything from Twitter")

                #Opens the tDB3 file and reads for displaying in the lblDisplayTwitterData below, and then closes it
                saveFile2 = open('tDB3.csv')
                readFile = saveFile2.read()
                saveFile2.close()

                #Displays Twitter hyperlink in label and binds it to left-click event and places in grid
                self.lblDisplayTwitterURL.config(text="http://twitter.com/search?q=" + str(userSearch) + "&src=typd", fg="Blue", cursor="hand2")
                self.lblDisplayTwitterURL.bind('<Button-1>', self.twittercallback)
                self.lblDisplayTwitterData.config(text=readFile, font="Times 10", justify=LEFT)
                self.lblDisplayTwitterData.grid(row=29, column=2, sticky=W)


        multi = threading.Thread(target=search)
        multi.start()

    #Function for clearing the labels
    def clear(self):
        for image in self.imageArray:
            image.grid_forget()
        self.lblDisplayWikiURL.config(text="")
        self.lblDisplayFlickrURL.config(text="")
        self.lblDisplayTwitterURL.config(text="")
        self.lblDisplayWikiData.config(text="")
        self.lblDisplayFlickrData.grid_forget()
        self.lblDisplayTwitterData.grid_forget()


    #Function for closing the window
    def close(self):
        alive = False
        self.master.destroy()


def main():
    root = Tk()
    Main(root)
    root.mainloop()


#Loops the code so the windows stay open
if __name__ == "__main__":
    main()
