from tweepy import StreamListener
import textwrap

__author__ = 'Andre'

class Listener(StreamListener):

    def __init__(self, api=None):
        super(Listener, self).__init__()
        self.searchTweets = 11

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

            if(self.numTweets < self.searchTweets):
                textwrapTweet = ('\n' .join(textwrap.wrap(tweet, 85)))
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
