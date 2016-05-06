import os
import ast

# Concatenate all timeline files into one file of tweets from timeline
def main():
    out = open("./timeline_tweets.txt", "w")
    # Group of timeline tweets to concatenate
    files = [f for f in os.listdir('.') if f.startswith("home-timeline")]
    #files = ["home-timeline1.txt"]
    for file in files:
        with open(file) as currentFile:
            for line in currentFile:
                items = line.split("},{\"created")
                for i in range(0, (len(items) - 1)):
                    if i == 0:
                        out.write(items[i][1:] + "}" + "\n")
                    elif i == (len(items) - 1):
                        out.write("{\"created" + items[i][:-1] + "}" + "\n")
                    else:
                        out.write("{\"created" + items[i] + "}" + "\n")


if __name__ == "__main__":
    main()