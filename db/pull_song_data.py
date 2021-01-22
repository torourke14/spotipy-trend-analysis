import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint
import csv


# uri = 'spotify:track:6I6NX6tjGsxFAsIfGzY9lJ' #J cole deja vu

client_id = "5dd9d9e3032745c9b5672da897eca6c8"
client_secret = "d31b6c98b28944fa92dcb19a29dc0a9e"
# file = "subset_unique_tracks.txt"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

with open("song_search_results.csv", 'r') as SPOTIFY_URIS:

	with open("song_search_results_fix.txt", mode = 'w') as RESULTS:

		fifty_uris = list()

		next(SPOTIFY_URIS)

		for line in SPOTIFY_URIS:

			# print(line[:14])
			if line[:14] == "spotify:track:":
				# print(line[14:36])
				search_uri = line[14:36]

				fifty_uris.append(search_uri)

				if len(fifty_uris) == 50:

					fifty_tracks = sp.tracks(fifty_uris)

					# process tracks here

					for track in fifty_tracks['tracks']:

						artists = list()

						for artist in track['artists']:
							artists.append(artist['name'])

						all_artists = "/".join(artists)

						song_name = track['name']

						duration_ms = track['duration_ms']

						explicit_bool = 0

						if track['explicit']:
							explicit_bool = 1

						track_uri = track['uri']

						release_date = track['album']['release_date']

						write_string = track_uri+"<+>"+song_name+"<+>"+all_artists+"<+>"+release_date+"<+>"+str(duration_ms)+"<+>"+str(explicit_bool)

						RESULTS.write(write_string+"\n")


					fifty_uris = list()


		end_tracks = sp.tracks(fifty_uris)

		for track in end_tracks['tracks']:

			artists = list()

			for artist in track['artists']:
				artists.append(artist['name'])

			all_artists = "/".join(artists)

			song_name = track['name']

			duration_ms = track['duration_ms']

			explicit_bool = 0

			if track['explicit']:
				explicit_bool = 1

			track_uri = track['uri']

			release_date = track['album']['release_date']

			write_string = track_uri+"<+>"+song_name+"<+>"+all_artists+"<+>"+release_date+"<+>"+str(duration_ms)+"<+>"+str(explicit_bool)

			RESULTS.write(write_string+"\n")


	RESULTS.close()

SPOTIFY_URIS.close()

