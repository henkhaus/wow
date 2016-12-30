import urllib.request, json, time


#Variables
apikey = "8sv23p3ruq39kfng2phrrau3nstevp4j"
#realm = "Shadow-Council"

#Build url for auction data requests
def auctionurl (server):
    key = "8sv23p3ruq39kfng2phrrau3nstevp4j"
    realm = server
    base = "https://us.api.battle.net/wow/auction/data/"
    mid = "?locale=en_US&apikey="
    url =(base + realm+mid + key)
    print(url)

    #grab header file
   
    #req = urllib.request(url)
    weburl = urllib.request.urlopen(url).read()

    encoding = weburl.decode('UTF-8')

    data = json.loads(encoding)

    #gather data from initial return
    time = (data['files'][0]['lastModified'])
    url = (data['files'][0]['url'])


    #get auction data
    #req = urllib.request(url)
    weburl = urllib.request.urlopen(url).read()
    encoding = weburl.decode('UTF-8')

    data = json.loads(encoding)
    
    return data['auctions']


#query users for guild and character indfo. returns Raw Json
def char_query(name, realm):
    key = "8sv23p3ruq39kfng2phrrau3nstevp4j"
    base = 'https://us.api.battle.net/wow/character/'
    mid = '?fields=guild&locale=en_US&apikey='
    server = realm.replace(' ','-')
    url = (base + server+ "/"+name+mid+key)
    print (url)
    #req = urllib2.Request(url)
    weburl = urllib.request.urlopen(url).read()

    encoding = weburl.decode('UTF-8')

    data = json.loads(encoding)

    return data

def guild_query(guild, realm):
    guild = guild.replace(" ","%20")
    key = "8sv23p3ruq39kfng2phrrau3nstevp4j"
    base = 'https://us.api.battle.net/wow/guild/'
    mid = '?fields=members&locale=en_US&apikey='
    server = realm.replace(' ','-')
    url = (base + server+ "/"+guild+mid+key)
    #print (url)
    #req = urllib2.Request(url)
    weburl = urllib.request.urlopen(url).read()

    encoding = weburl.decode('UTF-8')

    data = json.loads(encoding)

    return data

def itemquery(itemnumber):
    item = str(itemnumber)
    key = "8sv23p3ruq39kfng2phrrau3nstevp4j"
    base = 'https://us.api.battle.net/wow/item/'
    mid = '?locale=en_US&apikey='
    #server = realm.replace(' ','-')
    url = (base +item +mid+key)
    print (url)
    #req = urllib2.Request(url)
    weburl = urllib.request.urlopen(url).read()

    encoding = weburl.decode('UTF-8')

    data = json.loads(encoding)

    return data

def print_time(unixtime):
    human_time = time.strftime("%D %H:%M", time.localtime(int(unixtime)))
    return  human_time

