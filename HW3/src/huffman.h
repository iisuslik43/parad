#ifndef HUFFMAN_H
#define HUFFMAN_H

#include <stdint.h>
#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <vector>
#include <string.h>
#include <exception>
#include <stdexcept>
static std::size_t INF = (std::size_t)(1e10);

class Node{
public:
    Node(){
        count = INF;
        node_1 = NULL;
        node_0 = NULL;
    }

    std::size_t count;
    uint8_t code;
    Node* node_0,* node_1;
    bool operator<(Node& a){
        if(count != a.count)
            return count < a.count;
        return code < a.code;
    }
};

class Tree{
public:
    Tree(const std::vector<Node>& counts);
    size_t decode_file(std::ifstream& in, std::ofstream& out, std::size_t no_huffman_size);
    size_t code_file(std::ifstream& in, std::ofstream& out);
    std::vector<std::vector<bool>> get_codes();
    void count_codes();

private:
    std::vector<bool> ans;
    std::vector<std::vector<bool>> codes;
    std::vector<Node> codes_tree;
    std::vector<Node> fake_codes_tree;
    Node* root;

    void dfs(Node* v, std::vector<bool>& tree_path_code);

};

void archive(std::string in_file, std::string out_file);
void unarchive(std::string in_file, std::string out_file);

#endif
