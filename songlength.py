import requests, csv, json, time, sys, argparse, math

class Const:
    useragent = {'user-agent': 'song-length-finder/1.0.0'}

# command line argument parser garbage
parser = argparse.ArgumentParser(description="get the lengths for a CSV list of songs (with artists)")
parser.add_argument('file', help='CSV to load songs from')
parser.add_argument('--startAt', help='row to start processing at in the CSV', action='store', type=int)
parser.add_argument('--apikey', help='API key to use for this run - set this more permanently by editing the secrets file.', action='store')
parser.add_argument('-sp', '--stemplot', help='Generate a stem plot of the song lengths while collecting data.', action='store_true')
parser.add_argument('-v', '--verbose', help='Ruin your pretty table by dumping debug info to stdout.', action='store_true')
args = parser.parse_args()

apikey = ""
if args.apikey == None:
    with open("secrets.json", 'r', newline='') as secrets:
        jsonsecrets = json.load(secrets)
        if len(jsonsecrets['apikey']) != 32:
            print("The API key you provided in the secrets file isn't the right length.")
            sys.exit(1)
        apikey = jsonsecrets['apikey']
elif len(apikey) == 32:
    apikey = args.apikey
else:
    print("The API key you provided doesn't look quite right. Check it and try again.")
    sys.exit(1)

"""
return the JSON response for a song's info
"""
def getSongInfo(track, artist):
    payload = {'method':'track.getInfo', 'api_key':apikey,
    'artist':artist, 'track':track, 'format':'json'}
    r = requests.get("http://ws.audioscrobbler.com/2.0", params=payload,
    headers=Const.useragent)
    return r.json()

class Stemplot:
    internalPlot = {}
    def addData(self, number):
        if not args.stemplot: return
        dbgPrint(f"adding {number} to stemplot")
        # stringify the number so we can do splitting on it because I'm too lazy to use mod
        number = str(number)
        leftSplit = int(number[0:2])
        rightSplit = int(number[2:3])
        dbgPrint(f"number splits as {leftSplit}|{rightSplit}")
        if leftSplit not in self.internalPlot:
            dbgPrint(f"added new list to dict for {leftSplit}.")
            self.internalPlot[leftSplit] = []
        self.internalPlot[leftSplit].append(rightSplit)

    def dumpPlot(self):
        dbgPrint("presorting plot lists")
        for key in iter(self.internalPlot):
            self.internalPlot[key] = sorted(self.internalPlot[key])

        dbgPrint("dumping the plot")
        for key in iter(sorted(self.internalPlot)):
            print(f"{key} | ", end='')
            for value in self.internalPlot[key]:
                print(f"{value} ", end='')
            print("")

def dbgPrint(string):
    if args.verbose:
        print(string)

# real code
file = args.file
outfile = time.strftime("output-%d%m%y-%H%M.csv", time.localtime())
print("started songlength.py")
print("opening flie {} as read-only".format(file))
print("outputting to file {}".format(outfile))
if args.stemplot: print("generating stemplot for data")
with open(file, 'r', newline='') as oldlist:
    with open(outfile, 'w', newline='') as newlist:
        try:
            songreader = csv.reader(oldlist, dialect='excel')
            songwriter = csv.writer(newlist, dialect='excel')
            rowcount = 0
            stem = Stemplot()
            for row in songreader:

                if args.startAt != None:
                    rowtgt = args.startAt
                else:
                    rowtgt = 0
                
                if rowcount < rowtgt:
                    rowcount += 1
                    continue

                if rowcount > 0:
                    si = getSongInfo(row[0], row[1])
                    track = si['track']['name']
                    artist = si['track']['artist']['name']
                    duration = int(si['track']['duration']) / 1000
                    print("{:3d} | {:>40} | {:>30} | {}:{:02.0f} | {}".format(rowcount, track, artist, math.ceil(duration/60), duration%60, duration))
                    if int(si['track']['duration']) < 1:
                        dbgPrint("not recording this song, it has no duration.")
                    else:
                        songwriter.writerow([track, artist, duration, track[0]])
                        # hacking some stem plot code on to this
                        stem.addData(duration)
                        # end hacky stem plot code
                    time.sleep(0.2)
                rowcount += 1
            stem.dumpPlot()
        except Exception:
            print("HIT EXCEPTION!")
            print('TRACEBACK -------------------------------------------')
            exinfo = sys.exc_info()
            sys.excepthook(exinfo[0], exinfo[1], exinfo[2])
            print('END TRACEBACK ---------------------------------------')
            print(si)
            print(row)
            sys.exit(1)