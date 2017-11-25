avrhello.hex: avrhello.S
	avra avrhello.S -o avrhello.hex
 
 upload: avrhello.hex
 	avrdude -c arduino -p ATMEGA328P -P /dev/ttyACM0 -b 115200 -U flash:w:avrhello.S.hex
 	
 clean:
 	rm *.cof
 	rm *.hex
 	rm *.obj