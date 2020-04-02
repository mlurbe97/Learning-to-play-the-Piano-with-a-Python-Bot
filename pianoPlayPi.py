#!/usr/bin/python3
# -*- coding: utf-8 -*-

#	Learning to play the Piano with a Python Bot  Copyright (C) 2020  Manel Lurbe Sempere
#	This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#	This is free software, and you are welcome to redistribute it
#	under certain conditions; type `show c' for details.

########################################
#			Imports					   #
########################################
import time
import sys
from adafruit_servokit import ServoKit
#end Imports.

########################################
#		Initialize I2C bus             #
########################################

# Create the servo connection.
kit = ServoKit(channels=16)
#end Initialize I2C bus.

########################################
#		Global variables               #
########################################

# Servo angles.
left = 0;
off = 90;
right = 180;

# Song to be played.
song = [];
song2 = [];
#end Global variables.

########################################
#		Music notes available          #
########################################

# Channel of each servo motor.
mt0 = kit.servo[0];
mt1 = kit.servo[1];
mt2 = kit.servo[2];
mt3 = kit.servo[3];
mt4 = kit.servo[4];
mt5 = kit.servo[5];
mt6 = kit.servo[6];
mt7 = kit.servo[7];
mt8 = kit.servo[8];
mt9 = kit.servo[9];
mt10 = kit.servo[10];
mt11 = kit.servo[11];
mt12 = kit.servo[12];
mt13 = kit.servo[13];
mt14 = kit.servo[14];
mt15 = kit.servo[15];

# Servo motors available.
motor_list = [mt0,mt1,mt2,mt3,mt4,mt5,mt6,mt7,mt8,mt9,mt10,mt11,mt12,mt13,mt14,mt15]


# Each note with each channel.
music_notes = {
	"sil":(mt15,off),
	
	# Examples for flat notes.
	#"sib":(mt0,left),
	#"lab":(mt0,right),
	#"re2b":(mt1,right),
	#"mi2b":(mt1,left),
	
	"do0":(mt0,right),
	"re0":(mt0,left),
	"mi0":(mt1,right),
	"fa0":(mt1,left),
	"sol0":(mt2,left),
	"la0":(mt2,right),
	"si0":(mt3,right),

	"do1":(mt3,left),
	"re1":(mt4,right),
	"mi1":(mt4,left),
	"fa1":(mt5,right),
	"sol1":(mt5,left),
	"la1":(mt6,right),
	"si1":(mt6,left),

	"do":(mt7,left),
	"re":(mt7,right),
	"mi":(mt8,right),
	"fa":(mt8,left),
	"sol":(mt9,right),
	"la":(mt9,left),
	"si":(mt10,left),

	"do2":(mt10,right),
	"re2":(mt11,left),
	"mi2":(mt11,right),
	"fa2":(mt12,left),
	"sol2":(mt12,right),
	"la2":(mt13,left),
	"si2":(mt13,right),
	"do3":(mt14,left)
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
	print("Usage:\n\tpython3 "+program_name+" music_sheets/music_sheet.txt\nor:\n\t./"+program_name+" music_sheets/music_sheet.txt");
#end usage function.

########################################
#		play_note function             #
########################################
def play_note(the_notes):
	for note in the_notes:
		(note[0])[0].angle = (note[0])[1];
		time.sleep(0.01); # Wait for servo motor change.
	time.sleep((the_notes[0])[1]);
	for note in the_notes:
		(note[0])[0].angle = off;
		time.sleep(0.01); # Wait for servo motor change.
#end play_note function.

########################################
#			reset function             #
########################################
def reset():
	for motor in motor_list:
		motor.angle = off;
#end reset function.

########################################
#		get_music_sheets function        #
########################################
def get_music_sheet(music_sheet):
	try:
		song_file = open(music_sheet,"r");
	except:
		print("No music_sheet called music_sheets/"+str(music_sheet)+" found.");
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
#end get_music_sheets function.

########################################
#		get_music_sheetsAcomp function   #
########################################
def get_music_sheetAcomp(music_sheet):
	try:
		song_file = open(music_sheet,"r");
	except:
		print("No music_sheet called music_sheets/"+str(music_sheet)+" found.");
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
			song2.append(list_notes);
		except:
			continue;
#end get_music_sheetsAcomp function.

#########################################
#    Read arguments and get music_sheets  #
#########################################

# Get program name.
program_name = sys.argv[0].replace("./","");

# Get number of arguments.
num_args = len(sys.argv);

# Exit program if no music_sheet are selected.
if num_args <= 1:
	print("No music_sheet selected");
	usage(program_name);
	sys.exit(1);
 
# Get music_sheet name.
music_sheet = sys.argv[1];

# Get second music_sheet name if is available.
if num_args == 3:
	music_sheet2 = sys.argv[2];

# If music_sheet name is reset, reset motors and end program.
if music_sheet == "reset":
	reset();
	print("Reset notes");
	sys.exit(1);

# Get the music_sheet.
get_music_sheet(music_sheet);

# Get the second music_sheet if is available.
if num_args == 3:
	get_music_sheetAcomp(music_sheet2);
#end Read arguments and get music_sheets.

#########################################
#		Play Song Threaded				#
#########################################
def worker(num_thread):	
	try:
		while True:
			reset();
			if num_thread == 0:
				for note in song:
					time.sleep(0.06);
					play_note(note);
				print("The song has ended, playing again...");
			if num_thread == 1:
				for note in song2:
					time.sleep(0.06);
					play_note(note);
				print("The song has ended, playing again...");
	except KeyboardInterrupt:
		if num_thread == 0:
			reset();
			print("Turning off the piano.");
		sys.exit(1);
#end function worker.

if num_args == 3:
	# import thread feature.
	import threading
	threads = list();
	print('Playing piano, press Ctrl-C to quit...')
	for i in range(2):
	    t = threading.Thread(target=worker,args=(i,))
	    threads.append(t);
	    t.start();
#end Play Song Threaded

else:
#########################################
#		Play Song non-Threaded			#
#########################################
	print('Playing piano, press Ctrl-C to quit...')
	try:
		while True:
			reset();
			for note in song:
				time.sleep(0.06); # Modify to your servo motor delay in position changing.
				play_note(note);
			print("The song has ended, playing again...");
	except KeyboardInterrupt:
		reset();
		print("Turning off the piano.");
		sys.exit(1);
#end Play Song non-Threaded.

#end Program.