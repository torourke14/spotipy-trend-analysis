

import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint
import sqlite3 as dbInterface
import json



def makeTrackDictFromFile():

	songDict = dict()

	with open("song_search_results_fix.txt", mode='r') as SONGS:

		# with open("duplicates.txt", mode='w') as DUPES:
		for i, line in enumerate(SONGS):

			line = line.rstrip()

			line = line.split("<+>")

			line[0] = line[0][14:36]

			if line[0] in songDict:
				# DUPES.write("Line "+str(i+1)+" is a duplicate.\n")
				pass
			else:
				songDict[line[0]] = {
					"name": line[1],
					"artist": line[2],
					"date": line[3],
					"duration_ms": int(line[4]),
					"explicit": int(line[5]),
					"acousticness": None,
					"danceability": None,
					"energy": None,
					"instrumentalness": None,
					"key": None,
					"liveness": None,
					"loudness": None,
					"mode": None,
					"speechiness": None,
					"time_signature": None,
					"tempo": None,
					"valence": None
				}

		# DUPES.close()

	SONGS.close()

	return songDict


def pullAudioFeatures(songDict):

	all_song_ids = list(songDict.keys())

	# makes list of all song ids into a 2d list with 50 ids in each sublist (except last)
	split_50_ids = [all_song_ids[i:i+50] for i in range(0, len(all_song_ids), 50)]

	# print(len(split_50_ids))
	# print(len(split_50_ids[0]))
	# print(len(split_50_ids[-1]))

	client_id = "5dd9d9e3032745c9b5672da897eca6c8"
	client_secret = "d31b6c98b28944fa92dcb19a29dc0a9e"

	client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

	for sublist in split_50_ids:

		api_resp = sp.audio_features(sublist)

		if api_resp is None:
			print("Response is none.")
			continue

		for features in api_resp:

			if features is None:
				print("Features are none.")
				continue

			track_dict = songDict[features['id']]

			track_dict['acousticness'] = None if features['acousticness'] is None else float(features['acousticness'])
			track_dict['danceability'] = None if features['danceability'] is None else float(features['danceability'])
			track_dict['energy'] = None if features['energy'] is None else float(features['energy'])
			track_dict['instrumentalness'] = None if features['instrumentalness'] is None else float(features['instrumentalness'])
			track_dict['key'] = None if features['key'] is None else int(features['key'])
			track_dict['liveness'] = None if features['liveness'] is None else float(features['liveness'])
			track_dict['loudness'] = None if features['loudness'] is None else float(features['loudness'])
			track_dict['mode'] = None if features['mode'] is None else int(features['mode'])
			track_dict['speechiness'] = None if features['speechiness'] is None else float(features['speechiness'])
			track_dict['time_signature'] = None if features['time_signature'] is None else int(features['time_signature'])
			track_dict['tempo'] = None if features['tempo'] is None else float(features['tempo'])
			track_dict['valence'] = None if features['valence'] is None else float(features['valence'])
				

			# track_dict['acousticness'] = float(features['acousticness'])
			# track_dict['danceability'] = float(features['danceability'])
			# track_dict['energy'] = float(features['energy'])
			# track_dict['instrumentalness'] = float(features['instrumentalness'])
			# track_dict['key'] = int(features['key'])
			# track_dict['liveness'] = float(features['liveness'])
			# track_dict['loudness'] = float(features['loudness'])
			# track_dict['mode'] = int(features['mode'])
			# track_dict['speechiness'] = float(features['speechiness'])
			# track_dict['time_signature'] = int(features['time_signature'])
			# track_dict['tempo'] = float(features['tempo'])
			# track_dict['valence'] = float(features['valence'])

			songDict[features['id']] = track_dict

	return songDict


def create_song_db(songDict):

	dbConnection = dbInterface.connect("spotify_song_data.db")

	cursor = dbConnection.cursor()

	create_sql = "CREATE TABLE IF NOT EXISTS song_analysis (id VARCHAR(25) PRIMARY KEY," \
		  "name VARCHAR(300) NOT NULL," \
		  "artist VARCHAR(500) NOT NULL," \
		  "rel_date VARCHAR(25) NOT NULL," \
		  "explicit INTEGER NOT NULL," \
		  "time_signature INTEGER," \
		  "key INTEGER," \
		  "tempo REAL," \
		  "mode INTEGER," \
		  "duration_ms INTEGER NOT NULL," \
		  "danceability REAL," \
		  "valence REAL," \
		  "energy REAL," \
		  "loudness REAL," \
		  "speechiness REAL," \
		  "acousticness REAL," \
		  "instrumentalness REAL," \
		  "liveness REAL)"

	try:
		cursor.execute(create_sql, [])
		dbConnection.commit()
	# If any errors occur, return the no info dictionary
	except Exception as error:
		raise DatabaseError("Failed to execute SQL statement.  " + str(error))


	for song_id in songDict.keys():

		track_dict = songDict[song_id]

		variables = [song_id, track_dict['name'], track_dict['artist'], track_dict['date'], track_dict['explicit'], track_dict['time_signature'],
					track_dict['key'], track_dict['tempo'], track_dict['mode'], track_dict['duration_ms'], track_dict['danceability'],
					track_dict['valence'], track_dict['energy'], track_dict['loudness'], track_dict['speechiness'], track_dict['acousticness'],
					track_dict['instrumentalness'], track_dict['liveness']]

		insert_sql = "INSERT INTO song_analysis (id, name, artist, rel_date, explicit, time_signature, key, tempo, mode, duration_ms, danceability," \
			  "valence, energy, loudness, speechiness, acousticness, instrumentalness, liveness) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

		try:
			cursor.execute(insert_sql, variables)
			dbConnection.commit()
		# If any errors occur, return the no info dictionary
		except Exception as error:
			raise DatabaseError("Failed to execute SQL statement.  " + str(error))

	cursor.close()

	dbConnection.close()




if __name__ == "__main__":

	songDict = makeTrackDictFromFile()

	print("Unique Songs:", len(songDict.keys()))

	new_songDict = pullAudioFeatures(songDict)

	create_song_db(new_songDict)