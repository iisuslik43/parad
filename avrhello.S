.device ATmega328p
 
 .equ PORTB = 0x05

main:
	clr r16
	clr r17
    ldi r16, 0x20
    out 0x04, r16

mainloop:
	call writeH
	call writeE
	call writeL
	call writeL
	call writeO
	call waitTire
	call waitTire
	rjmp mainloop


writeH:
	call tochka
	call tochka
	call tochka
	call tochka
	call waitAfterLetter
	ret

writeE:
	call tochka
	call waitAfterLetter
	ret

writeL:
	call tochka
	call tire
	call tochka
	call tochka
	call waitAfterLetter
	ret

writeO:
	call tire
	call tire
	call tire
	call waitAfterLetter
	ret


tochka:
	ser r16
	out PORTB, r16
	call wait
	clr r16
	out PORTB, r16
	call wait
	ret

tire:
	ser r16
	out PORTB, r16
	call waitTire
	clr r16
	out PORTB, r16
	call wait
	ret


wait:
 	ldi r17,0x10
    ldi r18,0x00
    ldi r19,0x00
     
    call _w0
    ret

waitTire:
	call wait
	call wait
	call wait
	ret

waitAfterLetter:
	call wait
	call wait
	ret

_w0:
    dec r19
    brne _w0
    dec r18
    brne _w0
    dec r17
    brne _w0
    
    ret