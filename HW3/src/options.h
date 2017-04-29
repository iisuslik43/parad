#ifndef OPTIONS_H
#define OPTIONS_H
#include "huffman.h"
class Options{
public:
    Options(int argc, char** argv);
    std::string in_file, out_file;
    int is_archive;
};

bool isEmptyFile(std::ifstream& in);
bool isEmptyFile(std::string filename);
#endif
