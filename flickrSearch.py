from tkinter import messagebox
from urllib.request import urlopen
import flickrapi
import io
from PIL import Image

__author__ = 'Andre'

# Read the Key and secret from a file and add it to an array for security
# read out of array for authentication
flickrArray = []
flickrAuth = open('flickerAuth')
for line in flickrAuth:
    key = line.strip("\n")
    flickrArray.append(key)
flickrAuth.close()

flKey = flickrArray[0]
flSecret = flickrArray[1]


class flickrSearch:
    def __init__(self, userSearchFlickr):
        searchPhotos = 10       #number of photos searched
        i = 0
        self.flickrArray = []
        self.imageArray = []

        try:
            #Sets flickr key, secret, and format and then searches using the user input and sets how many images to display
            flickr = flickrapi.FlickrAPI(flKey, flSecret, format='parsed-json')
            photos = flickr.photos.search(tags=userSearchFlickr, title=userSearchFlickr, per_page=searchPhotos)
        # catch exception if not connected to the internet
        # since it also runs in a thread I could not find the correct exception.
        except:
            messagebox.showinfo("Flickr Error", "Flicker could not connect and return any data. Check if you are connected to the internet")

        try:
            #While loop that gets specific data of the images for building the photo URL while i < 10
            while i < searchPhotos:
                photoFarm = str(photos['photos']['photo'][i]['farm'])
                photoServer = str(photos['photos']['photo'][i]['server'])
                photoID = str(photos['photos']['photo'][i]['id'])
                photoSecret = str(photos['photos']['photo'][i]['secret'])

                #Builds the photo URL
                buildPhotoURL = ("http://farm" + photoFarm + ".static.flickr.com/" + photoServer + "/" + photoID + "_" + photoSecret + "_m.jpg\n")

                #Gets the bytes of images, opens them with PIL,
                # and safes them to an array to store them for retrieving
                hyperlink = buildPhotoURL.strip("\n")
                imageBytes = urlopen(hyperlink).read()
                dataStream = io.BytesIO(imageBytes)
                pilImage = Image.open(dataStream)

                #Adds the built image URLs to the flickrArray
                self.flickrArray.append(buildPhotoURL)
                self.imageArray.append(pilImage)

                i += 1
        # catch exception if less then 10 results are returned
        except IndexError:
            messagebox.showerror("Flickr Error", "Could not return all 10 results")
        # catch exception if no results are returned due to no connction
        except UnboundLocalError:
            messagebox.showerror("Flickr Error", "Could not return anything because there is no connection")