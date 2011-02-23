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


def change():
    while(True):
        ls = os.listdir(wallpaper_home)
        client = gconf.client_get_default()
        for i in range(0, int(len(ls))):
            wallpaper = wallpaper_home +'/'+ls[i]
            if os.path.exists(wallpaper):
                client.set_string('/desktop/gnome/background/picture_filename', wallpaper)
                print 'Wallpaper Changed'
                print 'Next change in '+str(next_change)+'s'
                time.sleep(next_change)
            else:
                print 'Waiting for new wallpapers'
                time.sleep(20)


if __name__ == "__main__":
    if not os.path.exists(wallpaper_home):
        os.mkdir(wallpaper_home)
    create_index().start()
    change()
    sys.exit()
