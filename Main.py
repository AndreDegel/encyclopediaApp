__author__ = 'Jesse'
from tkinter import *
import webbrowser
import urllib.request
import urllib.parse
import re
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


class Main:
    def __init__(self, master):

        #Creates userSearch Variable for storing user input
        self.userSearch = StringVar()

        #sets window to master, sets title, and window size
        self.master = master
        self.master.title("Encyclopedia App")
        self.master.geometry("500x430")

        #Creates labels, buttons, and textbox
        lblTitle = Label(self.master, text="Searchster", font=("Times 16 bold"), fg="green", )
        lblSearch = Label(self.master, text="Search: ", font=("Times 10"))
        txtBoxSearch = Entry(self.master, width=17, textvariable=self.userSearch)
        btnSearch = Button(self.master, text="Search", width=14, command=self.search)
        btnQuit = Button(self.master, text="Close", width=14, command=self.close)
        lblWikiLabel = Label(self.master, text="           Wikipedia URL", font=("Times 10 bold"))
        lblFlickrLabel = Label(self.master, text="            Flickr URL", font=("Times 10 bold"))
        lblTwitterLabel = Label(self.master, text="          Twitter URL", font=("Times 10 bold"))

        #Initialize the URL Labels and set there position in the grid
        self.lblDisplayWikiURL = Label(self.master, text=" ")
        self.lblDisplayWikiURL.grid(row=2, column=4, sticky=W)
        self.lblDisplayFlickrURL = Label(self.master, text=" ")
        self.lblDisplayFlickrURL.grid(row=4, column=4, sticky=W)
        self.lblDisplayTwitterURL = Label(self.master, text=" ")
        self.lblDisplayTwitterURL.grid(row=8, column=4, sticky=W)

        #Places labels, buttons, and textbox in grid format
        lblTitle.grid(row=1, column=2)
        lblSearch.grid(row=2, column=1, sticky=E)
        txtBoxSearch.grid(row=2, column=2)
        btnSearch.grid(row=3, column=2)
        btnQuit.grid(row=4, column=2)
        lblWikiLabel.grid(row=1, column=4, sticky=W)
        lblFlickrLabel.grid(row=3, column=4, sticky=W)
        lblTwitterLabel.grid(row=7, column=4, sticky=W)


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

        #Searching and pulling flickr##############
        #Creates flickr array
        flickrArray = []

        #Creates variable for flickr URL and stores the value to be searched in FLickr
        flickrUrl = "http://www.flickr.com/search/?q=" + str(userSearch)
        flickrValues = {'s': userSearch}

        #Encodes the data (Converts to bytes for searching)
        flickrData = urllib.parse.urlencode(flickrValues)
        flickrData = flickrData.encode('utf-8')

        #Requests the data from the url and the response opens that url to search
        flickrRequest = urllib.request.Request(flickrUrl, flickrData)
        flickrResponse = urllib.request.urlopen(flickrRequest)

        #Reads and stores the data
        flickrRespData = flickrResponse.read()

        #Search for matching criteria within the respData
        flickrREGEX = re.findall((userSearch), str(flickrRespData))

        #Creates array and stores each matching item in that array

        for eachFlickrItem in flickrREGEX:
            if(len(flickrArray)>5):
                break
            else:
                flickrArray.append(eachFlickrItem + "\n")

        #Searching and pulling twitter tweets##############
        #Creates twitter array
        twitterArray = []

        #Creates variable for twitter URL and stores the value to be searched in twitter
        twitterUrl = "http://twitter.com/search?q=" + str(userSearch) + "&src=typd"
        twitterValues = {'s': userSearch}

        #Encodes the data (Converts to bytes for searching)
        twitterData = urllib.parse.urlencode(twitterValues)
        twitterData = twitterData.encode('utf-8')

        #Requests the data from the url and the response opens that url to search
        twitterRequest = urllib.request.Request(twitterUrl, twitterData)
        twitterResponse = urllib.request.urlopen(twitterRequest)

        #Reads and stores the data
        TwitterRespData = twitterResponse.read()

        #Search for matching criteria within the respData
        twitterREGEX = re.findall((userSearch), str(TwitterRespData))

        #For loop that adds the twitter item to twitter array
        for eachTwitterItem in twitterREGEX:
            if(len(twitterArray)>10):
                break
            else:
                twitterArray.append(eachTwitterItem + "\n")


        #Opens the webbrowsers
        webbrowser.open("http://en.wikipedia.org/w/index.php?title=" + str(userSearch))
        webbrowser.open("http://www.flickr.com/search/?q=" + str(userSearch))
        webbrowser.open("http://twitter.com/search?q=" + str(userSearch) + "&src=typd")

        #Displays Wikipedia hyperlink in label and binds it to left-click event and places in grid
        self.lblDisplayWikiURL.config(text="http://en.wikipedia.org/w/index.php?title=" + str(userSearch), fg="Blue", cursor="hand2")
        self.lblDisplayWikiURL.bind('<Button-1>', self.wikicallback)

        '''I'll leave the original format for the URL's in here in case anybody need it or we have to change back'''
        #lblDisplayWikiURL = Label(self.master, text="http://en.wikipedia.org/w/index.php?title=" + str(userSearch), fg="Blue", cursor="hand2")
        #lblDisplayWikiURL.bind('<Button-1>', self.wikicallback)
        #lblDisplayWikiURL.grid(row=2, column=4, sticky=W)
        #lblDisplayFlickrURL = Label(self.master, text="http://www.flickr.com/search/?q=" + str(userSearch), fg="Blue", cursor="hand2")
        #lblDisplayFlickrURL.bind('<Button-1>', self.flickrcallback)
        #lblDisplayFlickrURL.grid(row=4, column=4, sticky=W)
        #lblDisplayTwitterURL = Label(self.master, text="http://twitter.com/search?q=" + str(userSearch) + "&src=typd", fg="Blue", cursor="hand2")
        #lblDisplayTwitterURL.bind('<Button-1>', self.twittercallback)
        #lblDisplayTwitterURL.grid(row=8, column=4, sticky=W)


        #Displays Flickr hyperlink in label and binds it to left-click event and places in grid
        self.lblDisplayFlickrURL.config(text="http://www.flickr.com/search/?q=" + str(userSearch), fg="Blue", cursor="hand2")
        self.lblDisplayFlickrURL.bind('<Button-1>', self.flickrcallback)
        lblDisplayFlickrData = Label(self.master, text=flickrArray)
        lblDisplayFlickrData.grid(row=6, column=4, sticky=W)

        #Displays Twitter hyperlink in label and binds it to left-click event and places in grid
        self.lblDisplayTwitterURL.config(text="http://twitter.com/search?q=" + str(userSearch) + "&src=typd", fg="Blue", cursor="hand2")
        self.lblDisplayTwitterURL.bind('<Button-1>', self.twittercallback)
        lblDisplayTwitterData = Label(self.master, text=twitterArray)
        lblDisplayTwitterData.grid(row=9, column=4, sticky=W)


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


############### Streaming Tweets ######################
cKey = 'xLwpqmwpQLNfkKI5Ux5eHSRAP'
cSecret = '56HR60btiSEjc03GO3Xm0i5VQSVOb9Xs5XQQZi2COQoxhjkqJE'
aToken = '1187764111-LK8d4jwuumvY5XVFx5GKeHSQVcUxJsiEJoE1pMS'
aSecret = 'o30rmM7frd8OONtU2QPZGTsw7s8KmGHEpdFYtEKsfJWjw'

userSearch = str(input("Enter search criteria: "))

class Listener(StreamListener):

    def on_data(self, raw_data):
        try:
            tweet = raw_data.split(',"text":"')[1].split('","source')[0]
            print(tweet)

            # saveThisTweet = tweet
            # saveFile2 = open('twitterDataBase3.csv', 'a')
            # saveFile2.write(saveThisTweet)
            # saveFile2.write('\n')
            # saveFile2.close()
            return True
        except:
            print("Failed")

    def on_error(self, status_code):
        print(status_code)

authorize = OAuthHandler(cKey, cSecret)
authorize.set_access_token(aToken, aSecret)

twitterStream = Stream(authorize, Listener())
twitterStream.filter(track=[str(userSearch)])