import webbrowser
import requests
import os
import time
import bs4

# base link where all the lectures are stored
homepage = 'http://pages.stat.wisc.edu/~ifischer/Intro_Stat/stat311/VIDEO_LECTURES/'
statsFolder = '/Users/nandanv/Documents/Spring 2020/STATS 311'

while True:
    # gets the website
    print("\nChecking the stats website... " + time.asctime() + '\n')
    res = requests.get('http://pages.stat.wisc.edu/~ifischer/Intro_Stat/stat311/VIDEO_LECTURES/')
    res.raise_for_status()

    # parses the HTML
    webpage = bs4.BeautifulSoup(res.text, "html.parser")

    # finds all lectures
    allLinks = []
    for link in webpage.find_all('a'):
        allLinks.append(link.get('href'))
    lectures = allLinks[5:]
    print("Lectures on the website: " + str(lectures))
    print('\n')

    # new list of existing lectures in the STATS 311 folder
    existingLectures = os.listdir('/Users/nandanv/Documents/Spring 2020/STATS 311')

    for lecture in lectures:
        if lecture[2:] in existingLectures:
            print(lecture[2:] + " is currently in the folder... \n moving on...\n")
        elif lecture[2:] not in existingLectures:
            try:
                print(lecture[2:] + " is a NEW lecture " + time.asctime())
                lectureLink = os.path.join(homepage, lecture[2:])
                print("lectureLink: " + lectureLink)
                print('\n')
                resVid = requests.get(lectureLink)
                resVid.raise_for_status()
                print("Creating new file... ")
                print('\n')
                videoFile = open(os.path.join(statsFolder, lecture[2:]), 'wb')
                print("Downloading video... ")
                for chunk in resVid.iter_content(10000000):
                    videoFile.write(chunk)
                    print(".")
                print("Downloaded all new lectures!")
                videoFile.close()
                print(5 * '\a')
                print("\nCheck your folder, there's a new video!")
            except Exception as e:
                print("Error: \n" + e)

    print("\nProcess complete!\n")
    print("Last check at - " + time.asctime() + '\n')
    time.sleep(18000)
