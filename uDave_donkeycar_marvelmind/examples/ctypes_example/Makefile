all: clear test_lib.so clean

clear:
	rm -rf *.so

test_lib.so:
	gcc -g -fPIC -c test.c -o test.o
	gcc -g -fPIC -c called.c -o called.o
	gcc -o test_lib.so test.o called.o -fPIC -shared

clean:
	rm -rf *.o

