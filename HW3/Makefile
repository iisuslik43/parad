all: 
	make --file=Makefile_huffman
test:
	cd ./test/ && cmake CMakeLists.txt && make
clean:
	rm -rf bin huffman ./test/test ./test/CMakeFiles ./test/CMakeCache.txt ./test/cmake_install.cmake ./test/Makefile
.PHONY: clean all test
