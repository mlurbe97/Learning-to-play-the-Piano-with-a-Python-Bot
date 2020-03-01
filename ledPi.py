#!/usr/bin/python3
# -*- coding: utf-8 -*-

#	Learning to play the Piano with a Python Bot  Copyright (C) 2020  Manel Lurbe Sempere
#	This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#	This is free software, and you are welcome to redistribute it
#	under certain conditions; type `show c' for details.

########################################
#		Imports		       #
########################################
import busio
import time
import sys
from adafruit_pca9685 import PCA9685
from board import SCL, SDA

########################################
#	Initialize I2C bus             #
########################################

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA);

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus);

# Set the PWM frequency to 60hz.
pca.frequency = 60;

########################################
#	Global variables               #
########################################

# Led brightness.
on = 0xffff;
off = 0;
# Song to be played.
song = [];

########################################
#	Music notes available          #
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

########################################
#	Tempo notes defines            #
########################################

# Values of each type of note.
redonda = 0.8;
blanca = 0.4;
negra = 0.3;
corchea = 0.2;
semicorchea = 0.1;

# Each tempo with each value.
tempo_notes = {
	"r":redonda,
	"b":blanca,
	"n":negra,
	"c":corchea,
	"sc":semicorchea
};

########################################
#	play_note function             #
########################################
def usage(program_name):
	print("Usage:\n\tpython3 "+program_name+" partitures/partiture.txt\nor:\n\t./"+program_name+" partitures/partiture.txt");

########################################
#	play_note function             #
########################################
def play_note(the_note):
	the_note[0].duty_cycle = on;
	time.sleep(the_note[1]);
	the_note[0].duty_cycle = off;

########################################
#	    reset function             #
########################################
def reset():
	for note in music_notes:
		music_notes[note].duty_cycle = off;

########################################
#	get_partitures function        #
########################################
def get_partiture(partiture):
	try:
		song_file = open(partiture,"r");
	except:
		print("No partiture called partitures/"+str(partiture)+" found.");
		sys.exit(1);
	song_content = song_file.read().split("\n");
	for note in song_content:
		try:
			values = note.split(",");	
			tupla = (music_notes[values[0]],tempo_notes[values[1]]);
			song.append(tupla);
		except:
			continue;

#########################################
#    Read arguments and get partiture   #
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

#########################################
#		Play Song		#
#########################################
print('Playing piano, press Ctrl-C to quit...')
while True:
	reset();
	for note in song:
		play_note(note);
	
