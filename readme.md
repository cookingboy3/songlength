# songlength

## what is this thing?

songlength is a tiny thing I developed to take a big list of songs and find the lengths of all of them

## how do it do?

it uses the last.fm API and a big list of (hopefully properly typed) song names/artists.

## do I need anything for it?

yeah, you'll need [an API key from last.fm](https://www.last.fm/api), and all the dependencies listed in the pipfile (the only one you should actually need to install is requests, though)

## how do I use it?

feed it a lists of tracks with their artists (see songs-stripped.csv) and an api key. I haven't tried very hard with this, so a misspelled name or a name that last.fm can't find just completely borks. there's a command line argument (try `python ./songlength.py -h`) that lets you select a row to start from if you think that's why it crashed, but I can't promise that csv will work very well with your file. it's probably a good idea to rerun entirely.

## why?

I have a stats project centering around songs and their length, and after using a random website to get a list of songs (and painfully typing each. and. every. one. down.) it turned out that the website wouldn't tell me the lengths, so I had to do that myself. as you might expect, spending 3 hours writing an automated solution to the problem instead of spending the 90 minutes to do it manually was totally worth it.  
more accurately, because I wanted to. I don't often find good opportunities to write code for legitimate real life tasks, so this was a nice change and it was a lot of fun to get it working. so, why not? ~~because I have a lot of deadlines to hit.~~

## can I help?

yeah! it's open source for a reason. PR any changes. something in general that I was thinking of was adding in a feature to search for a song if it's not found by name the first time. another feature is figuring out a good way to get a random song, for some reason none of the databases seem to just have a get_random feature.

## what's this licensed under?

the MIT license. do what you want with it (although a head nod to me would be nice if you somehow find a use for this.)
