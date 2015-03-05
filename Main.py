__author__ = 'Jesse'
from tkinter import *
import webbrowser
import urllib.request
import urllib.parse
import re
import textwrap
import flickrapi
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time


class flickrSearch:
    def __init__(self, userSearchFlickr):
        flKey = '13c592d3851810c8f1a97ed2bd38af90'
        flSecret = 'c3e96f35fe4ef875'
        '''
        Info for flicker API documentation:
        https://code.google.com/p/python-flickr-api/wiki/Tutorial
        http://www.janeriksolem.net/2009/02/using-python-to-download-images-from.html
        '''

        self.numFlick = 1

        saveFileFlickr = open('flickDB.csv', 'w')
        saveFileFlickr.close()

        flickrArray = []

        flickr = flickrapi.FlickrAPI(flKey, flSecret, format='parsed-json')
        photos = flickr.photos.search(tags=userSearchFlickr, title=userSearchFlickr, per_page='10')
        #photoSets = flickr.photosets.getList(user_id=userSearch)
        #photoTitle = photos['photos']['photo']['0']
        #print('First set title: %s' % photos)

        if(self.numFlick < 6):
            textwrapPhotos = ('\n' .join(textwrap.wrap(str(photos), 180)))
            flickrArray.append(str(textwrapPhotos))
            saveFileFlickr = open('flickDB.csv', 'a')
            saveFileFlickr.write(str(self.numFlick) + "." + ")" + " ")
            saveFileFlickr.write(str(textwrapPhotos))
            saveFileFlickr.close()
            self.numFlick += 1


############### Streaming Tweets ######################
cKey = 'xLwpqmwpQLNfkKI5Ux5eHSRAP'
cSecret = '56HR60btiSEjc03GO3Xm0i5VQSVOb9Xs5XQQZi2COQoxhjkqJE'
aToken = '1187764111-LK8d4jwuumvY5XVFx5GKeHSQVcUxJsiEJoE1pMS'
aSecret = 'o30rmM7frd8OONtU2QPZGTsw7s8KmGHEpdFYtEKsfJWjw'

class Listener(StreamListener):

    def __init__(self, api=None):
        super(Listener, self).__init__()
        self.numTweets = 0
        self.i = 1

        #Opens the tDB3 file and overwrites it so you can append it repeatedly
        saveFile2 = open('tDB3.csv', 'w')
        saveFile2.close()

    def on_data(self, raw_data):

        try:

            #Sets tweet array and splits the data at text to the source, and then while numTweets is less than 10 it adds tweets to array
            self.tweetArray = []
            tweet = raw_data.split(',"text":"')[1].split('","source')[0]

            self.numTweets += 1

            if(self.numTweets < 11):
                textwrapTweet = ('\n' .join(textwrap.wrap(tweet, 160)))
                self.tweetArray.append(textwrapTweet)
                #print(self.tweetArray)
                saveFile2 = open('tDB3.csv', 'a')
                saveFile2.write(str(self.i) + "." + ")" + " ")
                saveFile2.write(textwrapTweet + "\n")
                saveFile2.close()
                self.i += 1
                return True
            else:
                return False

        except:
            print("Failed")

    #Prints status of error if error occurs
    def on_error(self, status_code):
        print(status_code)

#Sets consumer keys and access tokens
authorize = OAuthHandler(cKey, cSecret)
authorize.set_access_token(aToken, aSecret)

#Streams the tweets using the Listener class and depending on the criteria of the userSearch
#twitterStream = Stream(authorize, Listener())
#twitterStream.filter(track=[userSearch])


class Main:

    def __init__(self, master):

        #Creates userSearch Variable for storing user input and creates int vars for checkboxes
        self.userSearch = StringVar()
        self.chkVar1 = IntVar()
        self.chkVar2 = IntVar()
        self.chkVar3 = IntVar()

        #sets window to master, sets title, and window size
        self.master = master
        self.master.title("Encyclopedia App")
        self.master.geometry("940x700")
        self.master.resizable(width=FALSE, height=FALSE)
        #self.canvas = Canvas(self.master, borderwidth=0, highlightthickness=0)

        # #Scrollbar
        # scrlBar = Scrollbar(self.master, orient=VERTICAL)
        # scrlBar.grid(row=1, column=10)
        # self.canvas.config(width=1800, height=580)
        # self.canvas.config(yscrollcommand=scrlBar.set)
        # self.canvas.grid(column=0, row=0, sticky=N+S+E+W)

        #Creates Widgets
        lblTitle = Label(self.master, text="Searchster", font=("Times 16 bold"), fg="green", )
        lblSearch = Label(self.master, text="Search: ", font=("Times 10"))
        txtBoxSearch = Entry(self.master, width=17, textvariable=self.userSearch)
        btnSearch = Button(self.master, text="Search", width=14, command=self.search)
        btnQuit = Button(self.master, text="Close", width=14, command=self.close)
        lblBlankLabel = Label(self.master, text="                  ")
        lblWikiLabel = Label(self.master, text="Wikipedia:", font=("Times 10 bold"))
        lblFlickrLabel = Label(self.master, text="Flickr:", font=("Times 10 bold"))
        lblTwitterLabel = Label(self.master, text="Twitter:", font=("Times 10 bold"))
        lblBlankLabel2 = Label(self.master, text="   ")
        chkBtnWikipedia = Checkbutton(self.master, text="Wikipedia", variable=self.chkVar1, justify=LEFT)
        chkBtnFlickr = Checkbutton(self.master, text="Flickr", variable=self.chkVar2, justify=LEFT)
        chkBtnTwitter = Checkbutton(self.master, text="Twitter", variable=self.chkVar3, justify=LEFT)

        #Initialize the Labels and set there position in the grid so they can be reset repeatedly
        self.lblDisplayWikiURL = Label(self.master, text="")
        self.lblDisplayFlickrURL = Label(self.master, text="")
        self.lblDisplayTwitterURL = Label(self.master, text="")
        self.lblDisplayFlickrData = Label(self.master, text="")
        self.lblDisplayTwitterData = Label(self.master, text="")

        #Places Widgets in grid format
        lblTitle.grid(row=1, column=2, sticky=W)
        lblSearch.grid(row=2, column=1, sticky=E)
        txtBoxSearch.grid(row=2, column=2, sticky=W)
        btnSearch.grid(row=7, column=2, sticky=W)
        btnQuit.grid(row=8, column=2, sticky=W)
        lblBlankLabel.grid(row=9, column=2)
        lblWikiLabel.grid(row=10, column=2, sticky=W)
        lblFlickrLabel.grid(row=12, column=2, sticky=W)
        lblTwitterLabel.grid(row=15, column=2, sticky=W)
        lblBlankLabel2.grid(row=7, column=3)
        chkBtnWikipedia.grid(row=3, column=2, sticky=W)
        chkBtnFlickr.grid(row=4, column=2, sticky=W)
        chkBtnTwitter.grid(row=5, column=2, sticky=W)
        self.lblDisplayWikiURL.grid(row=11, column=2, sticky=W)
        self.lblDisplayFlickrURL.grid(row=13, column=2, sticky=W)
        self.lblDisplayTwitterURL.grid(row=16, column=2, sticky=W)


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

    #Twitter Callback Event
    def twittercallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("http://twitter.com/search?q=" + str(userSearch) + "&src=typd")



    #Search Function
    def search(self):
        #Gets text from search textbox
        userSearch = self.userSearch.get()

        #Wikipedia Checkbox
        if(self.chkVar1.get()):
            print("WIkipedia Checked")
            #webbrowser.open("http://en.wikipedia.org/w/index.php?title=" + str(userSearch))

            #Displays Wikipedia hyperlink in label and binds it to left-click event and places in grid
            self.lblDisplayWikiURL.config(text="http://en.wikipedia.org/w/index.php?title=" + str(userSearch), fg="Blue", cursor="hand2")
            self.lblDisplayWikiURL.bind('<Button-1>', self.wikicallback)

        #Flickr Checkbox
        if(self.chkVar2.get()):
            print("Flickr Checked")
            #sets the userSearchFlickr to the userSearch get method
            flickrPull = flickrSearch(userSearchFlickr=str(userSearch))
            flickrPull.userSearch = userSearch
            #webbrowser.open("http://www.flickr.com/search/?q=" + str(userSearch))

            #Opens the flickDB file and reads for displaying in the lblDisplayFlickrData below, and then closes it
            saveFileFlickr = open('flickDB.csv')
            readFileFlickr = saveFileFlickr.read()
            saveFileFlickr.close()

            #Displays Flickr hyperlink in label and binds it to left-click event and places in grid
            self.lblDisplayFlickrURL.config(text="http://www.flickr.com/search/?q=" + str(userSearch), fg="Blue", cursor="hand2")
            self.lblDisplayFlickrURL.bind('<Button-1>', self.flickrcallback)
            self.lblDisplayFlickrData.config(text=readFileFlickr, justify=LEFT)
            self.lblDisplayFlickrData.grid(row=14, column=2, sticky=W)

        #Twitter Checkbox
        if(self.chkVar3.get()):
            print("Twitter checked")
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
            self.lblDisplayTwitterData.config(text=readFile, justify=LEFT)
            self.lblDisplayTwitterData.grid(row=17, column=2, sticky=W)

########Searching and pulling flickr##############
        # myFlickrSearch = flickrSearch()
        # myFlickrSearch.userSearch = userSearch

        #Creates flickr array
        # flickrArray = []
        #
        # #Creates variable for flickr URL and stores the value to be searched in FLickr
        # flickrUrl = "http://www.flickr.com/search/?q=" + str(userSearch)
        # flickrValues = {'s': userSearch}
        #
        # #Encodes the data (Converts to bytes for searching)
        # flickrData = urllib.parse.urlencode(flickrValues)
        # flickrData = flickrData.encode('utf-8')
        #
        # #Requests the data from the url and the response opens that url to search
        # flickrRequest = urllib.request.Request(flickrUrl, flickrData)
        # flickrResponse = urllib.request.urlopen(flickrRequest)
        #
        # #Reads and stores the data
        # flickrRespData = flickrResponse.read()
        #
        # #Search for matching criteria within the respData
        # flickrREGEX = re.findall((userSearch), str(flickrRespData))
        #
        # #Creates array and stores each matching item in that array
        #
        # for eachFlickrItem in flickrREGEX:
        #     if(len(flickrArray)>5):
        #         break
        #     else:
        #         flickrArray.append(eachFlickrItem + "\n")



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




