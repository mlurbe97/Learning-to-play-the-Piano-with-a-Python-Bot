#!/usr/bin/python3
# -*- coding: utf-8 -*-

#	Learning to play the Piano with a Python Bot  Copyright (C) 2020  Manel Lurbe Sempere
#	This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#	This is free software, and you are welcome to redistribute it
#	under certain conditions; type `show c' for details.

########################################
#			Imports					   #
########################################
import busio
import time
import sys
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
#end Imports.

########################################
#		Initialize I2C bus             #
########################################

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA);

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus);

# Set the PWM frequency to 60hz.
pca.frequency = 60;
#end Initialize I2C bus.

########################################
#		Global variables               #
########################################

# Led brightness.
on = 0xffff;
off = 0;

# Song to be played.
song = [];
#end Global variables.

########################################
#		Music notes available          #
########################################

# Channel of each LED.
do = pca.channels[0];
re = pca.channels[1];
mi = pca.channels[2];
fa = pca.channels[3];
sol = pca.channels[4];
la = pca.channels[5];
si = pca.channels[6];
do2 = pca.channels[7];

# Each note with each channel.
music_notes = {
	"do":do,
	"re":re,
	"mi":mi,
	"fa":fa,
	"sol":sol,
	"la":la,
	"si":si,
	"do2":do2
};
#end Music notes available.

########################################
#		Note tempo defines             #
########################################

# Values of each type of note.
dobleredonda = 3.2
redonda = 1.6;
blancaplus = 1.2;
blancasemi = 1;
blanca = 0.8;
negraplus = 0.6;
negrasemi = 0.5;
negra = 0.4;
corchea = 0.2;
semicorchea = 0.1;
ssemicorchea = 0.05;
sssemicorchea = 0.025;

# Each tempo with each value.
tempo_notes = {
	"dr":dobleredonda,
	"r":redonda,
	"b+":blancaplus,
	"b-":blancasemi,
	"b":blanca,
	"n+":negraplus,
	"n-":negrasemi,
	"n":negra,
	"c":corchea,
	"sc":semicorchea,
	"ssc":ssemicorchea,
	"sssc":sssemicorchea
};
#end Note tempo defines.

########################################
#			usage function             #
########################################
def usage(program_name):
	print("Usage:\n\tpython3 "+program_name+" partitures/partiture.txt\nor:\n\t./"+program_name+" partitures/partiture.txt");
#end usage function.

########################################
#		play_note function             #
########################################
def play_note(the_note):
	for note in the_notes:
		note[0].duty_cycle = on;
	time.sleep(the_notes[1]);
	for note in the_notes:
		note[0].duty_cycle = off;
#end play_note function.

########################################
#			reset function             #
########################################
def reset():
	for note in music_notes:
		music_notes[note].duty_cycle = off;
#end reset function.

########################################
#		get_partitures function        #
########################################
def get_partiture(partiture):
	try:
		song_file = open(partiture,"r");
	except:
		print("No partiture called partitures/"+str(partiture)+" found.");
		sys.exit(1);
	song_content = song_file.read().split("\n");
	for notes in song_content:
		try:
			tuple_notes = notes.split("\t");
			list_notes = [];
			for note in tuple_notes:
				values = note.split(",");
				tupla = (music_notes[values[0]],tempo_notes[values[1]]);
				list_notes.append(tupla);
			song.append(list_notes);
		except:
			continue;
#end get_partitures function.

#########################################
#    Read arguments and get partitures  #
#########################################

# Get program name.
program_name = sys.argv[0].replace("./","");

# Get number of arguments.
num_args = len(sys.argv);

# Exit program if no partiture are selected.
if num_args <= 1:
	print("No partiture selected");
	usage(program_name);
	sys.exit(1);
 
# Get partiture name.
partiture = sys.argv[1];

# If partiture name is reset, reset motors and end program.
if partiture == "reset":
	reset();
	print("Reset notes");
	sys.exit(1);

# Get the partiture.
get_partiture(partiture);
#end Read arguments and get partitures.

#########################################
#			Play Song					#
#########################################
print('Playing piano, press Ctrl-C to quit...')
try:
	while True:
		reset();
		for note in song:
			play_note(note);
		print("The song has ended, playing again...");
except KeyboardInterrupt:
	reset();
	print("Turning off the piano.");
	sys.exit(1);
#end Play Song.

#end Program.