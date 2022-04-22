all: clear marvelmind.o c_api_plugin.so c_api_plugin_global.so clean

clear:
	rm -rf *.so

marvelmind.o:
	gcc -g -fPIC -pthread -c marvelmind.c -o marvelmind.o

c_api_plugin_old.so:
	gcc -g -fPIC -pthread -c Read_to_py.c -o plugin.o
	gcc -o c_api_plugin_old.so plugin.o marvelmind.o -fPIC -pthread -shared
	
c_api_plugin.so:
	gcc -g -fPIC -pthread -c Read_to_py_voided.c -o plugin.o
	gcc -o c_api_plugin.so plugin.o marvelmind.o -fPIC -pthread -shared

c_api_plugin_global.so:
	gcc -g -fPIC -pthread -c Read_to_py_void_global.c -o plugin_global.o
	gcc -o c_api_plugin_global.so plugin_global.o marvelmind.o -fPIC -pthread -shared

clean:
	rm -rf *.o

