

def clean_unique_tracks(file_name):

	with open("unique_tracks_clean.txt", 'w+') as WRITE_FILE:
		with open(file_name, 'r') as SONGS:

			# variable for saving the track name
			line_1_save = ""

			for line in SONGS:

				# remove ID from line
				line = line[46:]

				# split into list [artist name, track name]
				line = line.split("<SEP>")

				# Often multiple artists are separated by / and underscores are used as commas
				# Some electronic songs have multiple artists separated by vs.
				line[0] = line[0].replace(" / ", ", ").replace("_", ",").replace(" vs. ", ", ").replace("/", ", ")

				# if artist has a semicolon, keep only text before the semicolon
				for i, char in enumerate(line[0]):
					if char == ';':
						line[0] = line[0][:i]
						break

				# Underscores used as commas in track name
				line[1] = line[1].replace("_", ",")

				# save the track name in case the next step makes it empty
				line_1_save = line[1]

				# remove everything after parentheses in track name.
				# NOTE: some songs have parentheses as the first thing in the name and this is why line_1_save is used
				for i, char in enumerate(line[1]):
					if char == '(' or char == '[' or char == '\n':
						line[1] = line[1][:i]
						break

				if not line[1]:
					# for i, char in enumerate(line_1_save):
					# 	if char == ')':
					# 		line_1_save = line_1_save[i+1:]
					# 		break
					line[1] = line_1_save
					line[1] = line[1].rstrip()

				# print(line[0], "-", line[1])
				WRITE_FILE.write(line[0]+" - "+line[1]+"\n")

		SONGS.close()
	WRITE_FILE.close()


if __name__ == "__main__":

	file_name = "unique_tracks.txt"

	clean_unique_tracks(file_name)

