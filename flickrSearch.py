from tkinter import messagebox
import flickrapi

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

        try:
            #While loop that opens the flickDB files to overwrite them so you can continuously search
            saveFileFlickr = open('flickDB.csv', 'w')
            saveFileFlickr.close()


            #Sets flickr key, secret, and format and then searches using the user input and sets how many images to display
            flickr = flickrapi.FlickrAPI(flKey, flSecret, format='parsed-json')
            photos = flickr.photos.search(tags=userSearchFlickr, title=userSearchFlickr, per_page='10')

            #While loop that gets specific data of the images for building the photo URL while i < 10
            while i < searchPhotos:
                photoFarm = str(photos['photos']['photo'][i]['farm'])
                photoServer = str(photos['photos']['photo'][i]['server'])
                photoID = str(photos['photos']['photo'][i]['id'])
                photoSecret = str(photos['photos']['photo'][i]['secret'])

                #Builds the photo URL
                buildPhotoURL = ("http://farm" + photoFarm + ".static.flickr.com/" + photoServer + "/" + photoID + "_" + photoSecret + "_m.jpg\n")

                #Adds the built image URLs to the flickrArray
                self.flickrArray.append(buildPhotoURL)

                i += 1

            #For loop that writes the photo URLS to the flickDB file
            saveFileFlickr = open('flickDB.csv', 'a')
            for hyperlink in self.flickrArray:
                saveFileFlickr.write(hyperlink)
            saveFileFlickr.close()


        except:
            messagebox.showinfo("Error", "No Results returned")