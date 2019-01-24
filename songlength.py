import requests, csv, json, time, sys, argparse, math

class Const:
    useragent = {'user-agent': 'song-length-finder/1.0.0'}

# command line argument parser garbage
parser = argparse.ArgumentParser(description="get the lengths for a CSV list of songs (with artists)")
parser.add_argument('file', help='CSV to load songs from')
parser.add_argument('--startAt', help='row to start processing at in the CSV', action='store', type=int)
parser.add_argument('--apikey', help='API key to use for this run - set this more permanently by editing the secrets file.', action='store')
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

# real code
file = args.file
outfile = time.strftime("output-%d%m%y-%H%M.csv", time.localtime())
print("started songlength.py")
print("opening flie {} as read-only".format(file))
print("outputting to file {}".format(outfile))
with open(file, 'r', newline='') as oldlist:
    with open(outfile, 'w', newline='') as newlist:
        try:
            songreader = csv.reader(oldlist, dialect='excel')
            songwriter = csv.writer(newlist, dialect='excel')
            rowcount = 0
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
                    print("{:3d} | {:>40} | {:>30} | {}:{:02.0f}".format(rowcount, track, artist, math.ceil(duration/60), duration%60))
                    if int(si['track']['duration']) < 1:
                        print("not recording this song, it has no duration.")
                    else:
                        songwriter.writerow([track, artist, duration])
                    time.sleep(0.5)
                rowcount += 1
        except Exception:
            print("HIT EXCEPTION!")
            exinfo = sys.exc_info()
            sys.excepthook(exinfo[0], exinfo[1], exinfo[2])
            print(si)
            print(row)
            sys.exit(1)