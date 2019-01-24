import csv

with open("songs-stripped.csv", 'r', newline='') as f:
    reader = csv.reader(f, dialect='excel')
    artistMaxLen = -1
    titleMaxLen = -1
    for row in reader:
        if len(row[0]) > titleMaxLen:
            titleMaxLen = len(row[0])
        if len(row[1]) > artistMaxLen:
            artistMaxLen = len(row[1])
    print(f"title max: {titleMaxLen}")
    print(f"artist max: {artistMaxLen}")    