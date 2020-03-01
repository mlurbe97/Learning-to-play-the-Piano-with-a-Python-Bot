#!/usr/bin/python3
# -*- coding: utf-8 -*-

#	Learning to play the Piano with a Python Bot  Copyright (C) 2020  Manel Lurbe Sempere
#	This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#	This is free software, and you are welcome to redistribute it
#	under certain conditions; type `show c' for details.

########################################
#		Imports		       #
########################################
import time
import sys
import RPi.GPIO as GPIO

########################################
#	Initialize buzzer      #
########################################

#Disable warnings (optional)
GPIO.setwarnings(False);

#Select GPIO mode
GPIO.setmode(GPIO.BCM);

#Set BUZZER  - pin 23 as output
BUZZER =23;
GPIO.setup(BUZZER,GPIO.OUT);

########################################
#	Global variables               #
########################################

# Song to be played.
song = [];

########################################
#	Music notes available          #
########################################

# Frecuency of each note.
do = 261.63;
re = 293.66;
mi = 329.63;
fa = 349.23;
sol = 392.00;
la = 440.00;
si = 493.88;
do2 = 523.25;

# Each note with each frecuency.
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
	halveWaveTime = 1 / (the_note[0] * 2 );
	waves = int(the_note[1] * the_note[0]);
	for i in range(waves):
		GPIO.output(BUZZER, True);
		time.sleep(halveWaveTime);
		GPIO.output(BUZZER, False);
		time.sleep(halveWaveTime);
	time.sleep(the_note[1] *0.1);

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

# Get the partiture.
get_partiture(partiture);

#########################################
#		Play Song		#
#########################################
print('Playing piano, press Ctrl-C to quit...')
while True:
	for note in song:
		play_note(note);