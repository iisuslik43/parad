#include "../src/huffman.h"
#include "../src/options.h"
using namespace std;

void read_counts(vector<Node>& count, ifstream& in, size_t number_of_unique_codes){
    for(size_t i = 0; i < number_of_unique_codes; i++){
        uint8_t c;
        size_t a;
        in.read((char*)&c, sizeof(char));
        in.read((char*)&a, sizeof(std::size_t));
        count[c].count = a;
        count[c].code = c;
    }
}



Tree::Tree(const vector<Node>& counts){
    codes_tree = counts;
    sort(codes_tree.begin(), codes_tree.end());
    fake_codes_tree = vector<Node>(counts.size());
    codes.resize(256);
    int i = 0;
    int j = 0;
    int k = 0;
    while(codes_tree[i].count != INF || (fake_codes_tree[j].count != INF && fake_codes_tree[j + 1].count != INF)){
        Node* min_count1, *min_count2;

        if(codes_tree[i] < fake_codes_tree[j]){
            min_count1 = &codes_tree[i];
            if(codes_tree[i + 1] < fake_codes_tree[j]){
                min_count2 = &codes_tree[i + 1];
                i += 2;
            }
            else{
                min_count2 = &fake_codes_tree[j];
                i++;
                j++;
            }
        }
        else{
            min_count1 = &fake_codes_tree[j];
            if(fake_codes_tree[j + 1] < codes_tree[i]){
                min_count2 = &fake_codes_tree[j + 1];
                j += 2;
            }
            else{
                min_count2 = &codes_tree[i];
                i++;
                j++;
            }
        }
        fake_codes_tree[k].node_1 = min_count1;
        fake_codes_tree[k].node_0 = min_count2;
        fake_codes_tree[k].count = min_count1->count + min_count2->count;
        k++;

    }
    root = &fake_codes_tree[k - 1];
}


void Tree::dfs(Node* v, vector<bool>& tree_path_code){
    if(!v->node_0 && !v->node_0){
        codes[v->code] = tree_path_code;
        return;
    }
    if(v->node_0){
        tree_path_code.push_back(false);
        dfs(v->node_0, tree_path_code);
        tree_path_code.pop_back();
    }
    if(v->node_1){
        tree_path_code.push_back(true);
        dfs(v->node_1, tree_path_code);
        tree_path_code.pop_back();
    }
    return;

}

void Tree::count_codes(){
vector<bool> tree_path_code;
    dfs(root, tree_path_code);
}



size_t Tree::decode_file(ifstream& in, ofstream& out, size_t no_huffman_size){
    uint8_t c;
    size_t i = 0;
    bool f = true;
    Node* now;
    size_t huffman_size = 0;
    while(in.peek() != std::ifstream::traits_type::eof() && i < no_huffman_size){
        in.read((char*)&c, sizeof(char));
        for(int j = 0; j < 8 && i < no_huffman_size; j++){
            if(f){
                now = root;
                f = false;
            }
            if((1 << j) & c){
                now = now->node_1;
            }
            else{
                now = now->node_0;
            }
            if(!now->node_0 && !now->node_1 && i < no_huffman_size){
                out.write((char*)&now->code, sizeof(char));
                i++;
                f = true;
            }
        }
        huffman_size++;
    }
    return huffman_size;
}

vector<vector<bool>> Tree::get_codes(){
    return codes;
}
size_t Tree::code_file(ifstream& in, ofstream& out){
    uint8_t c;
    count_codes();
    size_t j = 0;
    char write = 0;
    size_t huffman_size = 0;;
    while(in.peek() != std::ifstream::traits_type::eof()){
        in.read((char*)&c, sizeof(char));
        vector<bool> bite_code = codes[c];
        for(size_t h = 0; h < bite_code.size(); h++){
            if(j == 8){
                j = 0;
                out.write((char*)&write, sizeof(char));
                write = 0;
                huffman_size++;
            }
            write |= (static_cast<int>(bite_code[h]) << j);
            j++;
        }
    }
    if(j != 0){
        out.write((char*)&write, sizeof(char));
        huffman_size++;
    }
    return huffman_size;
}

void archive(string in_file, string out_file){
        ifstream in(in_file, ios::binary);
        if(!in.is_open()){
            throw runtime_error("problems with in_file");
        }
        ofstream out(out_file, ios::binary);
        if(!out.is_open()){
            throw runtime_error("problems with out_file");
        }
        if(isEmptyFile(in)){
            cout << "0\n0\n0";
            return;
        }
        vector<Node> counts(512);
        uint8_t c;
        size_t number_of_unique_codes = 0;
        size_t no_huffman_size = 0;
        while(in.peek() != std::ifstream::traits_type::eof()){
            in.read((char*)&c, sizeof(char));
            if(counts[c].count == INF){
                number_of_unique_codes++;
                counts[c].code = c;
                counts[c].count = 0;
            }
            counts[c].count++;
            no_huffman_size++;
        }
        Tree tree(counts);

        out.write((char*)&number_of_unique_codes, sizeof(std::size_t));
        out.write((char*)&no_huffman_size, sizeof(std::size_t));
        for(size_t i = 0; i < counts.size(); i++){
            if(counts[i].count != INF){
                out.write((char*)&i, sizeof(char));
                out.write((char*)&counts[i].count, sizeof(std::size_t));
            }
        }
        in.clear();
        in.seekg(0);
        size_t huffman_size = tree.code_file(in, out);
        cout << no_huffman_size  << endl;
        cout << huffman_size << endl;
        cout << sizeof(size_t) + number_of_unique_codes * (1 + sizeof(size_t)) << endl;
        in.close();
        out.close();
}
void unarchive(string in_file, string out_file){
    ifstream in(in_file, ios::binary);
    if(!in.is_open()){
        throw runtime_error("problems with in_file");
    }
    ofstream out(out_file, ios::binary);
    if(!out.is_open()){
        throw runtime_error("problems with out_file");
    }
    if(isEmptyFile(in)){
        cout << "0\n0\n0";
        return;
    }
    std::size_t number_of_unique_codes, no_huffman_size;
    in.read((char*)&number_of_unique_codes, sizeof(std::size_t));
    in.read((char*)&no_huffman_size, sizeof(std::size_t));


    std::vector<Node> count(260);
    read_counts(count ,in, number_of_unique_codes);
    Tree tree(count);
    size_t huffman_size = tree.decode_file(in, out, no_huffman_size);

    cout << huffman_size << endl;
    cout << no_huffman_size  << endl;
    cout << sizeof(size_t) + number_of_unique_codes * (1 + sizeof(size_t)) << endl;
    in.close();
    out.close();
}
