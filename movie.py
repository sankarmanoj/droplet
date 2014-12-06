import tmdbsimple as tmdb
import getpass
import MySQLdb as msd
import hashlib,time
password = getpass.getpass("Enter the password")
con = msd.connect('192.168.0.100','root',password,'droplet')
name = raw_input("Enter the name")
path = raw_input("Enter the path")
path = path.strip('"')
tmdb.API_KEY = ""
search = tmdb.Search()
response = search.movie(query=name)
s = search.results[0]
id = s['id']

def sha1_hash(file):
	BLOCKSIZE = 65536
	hasher = hashlib.sha1()
	with open(file, 'rb') as afile:
		buf = afile.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = afile.read(BLOCKSIZE)
	a=hasher.hexdigest()
	return a
hash = sha1_hash(path)
print "Done hashing"
movie = tmdb.Movies(id)
mi = movie.info()
ct= movie.credits()['cast']
print "Movie Database query completed"
cast = ""
query = "insert into movie values ("
for c in ct[0:5]:
	cast += c['name']+"  "
gen = ""
for g in mi['genres']:
	gen+=g['name']+"  "
x = mi
x['overview']=x['overview'].replace('"',"'")
x['tagline']=x['tagline'].replace('"',"'")

'''
query+=' name = "'+x['title']+'", '
query+=' overview = "'+x['overview']+'", '
query+=' tagline = "'+x['tagline']+'", '
query+=' rating = "'+str(x['vote_average'])+'", '
query+=' released = "'+str(x['release_date'])+'", '
query+=' genres = "'+gen+'",'
query+=' hash = "'+hash+'",'
query+=' cast = "'+cast+'" '
query+=");"
'''
query+='"'+x['title']+'", '
query+='"'+gen+'",'
query+='"'+cast+' ", '
query+='"'+x['overview']+' ", '
query+='"'+x['tagline']+' ", '
query+=str(x['vote_average'])+', '
query+='"'+str(x['release_date'])+'", '
query+=str(x['runtime'])+', '
query+=str(x['id'])+', '
query+='"'+hash+'"'

query+=");"
print query

cursor = con.cursor()
cursor.execute(query)
con.commit()
con.close()


		