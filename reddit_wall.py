import sys
import os
import gconf
import simplejson as json
import urllib
import subprocess
import time
import threading

reddit_url = 'http://www.reddit.com/r/wallpapers/top/.json'
ext = ['jpg', 'png']
wallpaper_home = os.getenv('HOME')+'/wallpapers'
#the change will occurs after every 'next_change' seconds
next_change = 10 

def setter_gnome():
    client = gconf.client_get_default()
    return lambda wallpaper: client.set_string('/desktop/gnome/background/picture_filename', wallpaper)

def setter_feh():
    import os
    return lambda wallpaper: os.system("feh --bg-center %s" % wallpaper)

#ugly dispatch table
#initializes the setter before returning it
def get_setter(name):
    try:
        return {"gnome": setter_gnome,
                "feh":   setter_feh   }[name]()
    except KeyError:
        print "No such setter"
        raise   

class create_index(threading.Thread):
    def run(self):
        while(True):
            change = False
            ls = os.listdir(wallpaper_home)
            feed = urllib.urlopen(reddit_url)
            data = json.loads(str(feed.read()))
            for i in range(0, int(len(data['data']['children']))):
                url = data['data']['children'][i]['data']['url']
                if url.rsplit("/")[-1].rsplit(".")[-1] in ext:
                    if url.rsplit("/")[-1] not in ls:
                        subprocess.call(['wget', '--directory-prefix',wallpaper_home, url])
                        change = True
            if not change:
                print 'Fetching suspended for 5hrs'
                time.sleep(3600*5)


def change(setter):
    while(True):
        ls = os.listdir(wallpaper_home)
        for i in range(0, int(len(ls))):
            wallpaper = wallpaper_home +'/'+ls[i]
            if os.path.exists(wallpaper):
                setter(wallpaper)
                print 'Wallpaper Changed'
                print 'Next change in '+str(next_change)+'s'
                time.sleep(next_change)
            else:
                print 'Waiting for new wallpapers'
                time.sleep(20)


if __name__ == "__main__":
    from optparse import OptionParser
    args = OptionParser()
    args.add_option("-s", "--setter", default="gnome")
    (options, args) = args.parse_args()
    setter = get_setter(options.setter)

    if not os.path.exists(wallpaper_home):
        os.mkdir(wallpaper_home)    
    create_index().start()
    change(setter)
    sys.exit()
