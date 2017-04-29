#include "options.h"

using namespace std;

Options::Options(int argc, char** argv){
    for(int i = 1; i < argc; i++){
            if(!strcmp(argv[i], "-c")){
                    is_archive = 1;
            }
            else if(!strcmp(argv[i], "-u")){
                    is_archive = -1;
            }
            else if(!strcmp(argv[i], "-f") || !strcmp(argv[i], "--file")){
                    i++;
                    if(i >= argc)
                        throw runtime_error("no in or out");
                    in_file = argv[i];
            }
            else if(!strcmp(argv[i], "-o") || !strcmp(argv[i], "--output")){
                    i++;
                    if(i >= argc)
                        throw runtime_error("no in or out");
                    out_file = argv[i];
            }
            else{
                    throw runtime_error("wrong option");
            }
    }
    if(!is_archive){
        throw runtime_error("no -c or -u");
    }
    if(in_file == "" || out_file == ""){
        throw runtime_error("no in or out");
    }
}

bool isEmptyFile(ifstream& in){
    size_t now = in.tellg();
    in.seekg(0, ios::end);
    size_t res = in.tellg();
    in.seekg(now);
    return !res;
}

bool isEmptyFile(string filename){
    ifstream in(filename, ios::binary);
    size_t now = in.tellg();
    in.seekg(0, ios::end);
    size_t res = in.tellg();
    in.seekg(now);
    return !res;
}
