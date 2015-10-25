import xml.etree.ElementTree as etree
import urllib.request as pagegrab
import sys
import audiotranscode as at

def getPuzzleInformation(text):
    puzzleinfo = {}
    try:
        with pagegrab.urlopen('https://s3.amazonaws.com/shadowpuzzle/' + text + '.xml') as response:
            theXML = response.read()
            root = etree.fromstring(theXML)
    except:
        #print('This puzzle does not exist.')
        return 'Not found. Make sure the string has no spaces and is uppercase.'

    resource = root.findall('./views/view/datasources/FileDataProvider/property[@name=\'data-location\']')[0].text
    hint = root.findall('./views/view/widgets/RFLayoutWidget[@id=\'modalhint\']/widgets/RFTextWidget/property')[0].text
    
    puzzleinfo['hint'] = hint

    print('Main Resource: ' + resource)



    if resource[-4:] == '.txt': ### Is text
        with pagegrab.urlopen(resource) as file:
            text = str(file.read())[2:-1]
            puzzleinfo['resource'], puzzleinfo['type'] = text, 'text'
            

    elif resource[-4:] == '.jpg' or resource[-4:] == '.png' or resource[-4:] == '.gif': ### Is a picture
        with pagegrab.urlopen(resource) as file:
            pic = file.read()
        with open('temp', 'wb') as fileout:
            fileout.write(pic)

        puzzleinfo['resource'], puzzleinfo['type'] = 'image' + resource[-4:], 'img'

    elif resource[-4:] == '.mp4': ### Is video
        with pagegrab.urlopen(resource) as file:
            vid = file.read()
        with open('temp', 'wb') as fileout:
            fileout.write(vid)

        puzzleinfo['resource'], puzzleinfo['type'] = 'video' + resource[-4:], 'vid'

    elif resource[-4:] == '.m4a' or resource[-4:] == '.wav': ### Is sound
        with pagegrab.urlopen(resource) as file:
            sound = file.read()
        with open('temp', 'wb') as fileout:
            fileout.write(sound)

        '''if resource[-4:] == '.m4a':
            atc = at.AudioTranscode()
            atc.transcode('sound.' + resource[-3:],'sound.wav')'''

        textHintThing = root.findall('.views/view/widgets/Text[@id=\'Text1\']/property[@name=\'text\']')[0].text
        puzzleinfo['resource'], puzzleinfo['type'] = ['sound.wav', textHintThing], 'sound'

    return puzzleinfo
        
