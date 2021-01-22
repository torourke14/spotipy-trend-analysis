



with open("custom_test.csv", mode = 'r') as SONG_DATA:

	counter = 0

	for line in SONG_DATA:
		if line[:11] == "*NOT_FOUND*":
			counter += 1

SONG_DATA.close()

print("Not Found:", counter)
print("Found:", 1000000-counter)