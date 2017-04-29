#include "../src/huffman.h"
#include "../src/options.h"
#include <gtest/gtest.h>
using namespace std;

string bool_vector_to_string(vector<bool>& v){
    string ans;
    for(size_t i = 0; i < v.size(); i++){
	if(v[i])
	    ans += "1";
	else
	    ans += "0";
    }
    return ans;
}

/*
TEST(TreeTest, IsCorrect){
    vector<Node> counts(260);
    counts['a'].count = 10;
    counts['a'].code = 'a';
    counts['b'].count = 1;
    counts['b'].code = 'b';
    counts['c'].count = 2;
    counts['c'].code = 'c';
    Tree tree(counts);
    Node* root = tree.root;
    ASSERT_TRUE(root);
    ASSERT_TRUE(root->node_1 && root->node_0);
    ASSERT_TRUE(root->node_1->code == 'a' || root->node_0->code == 'a');

    if(root->node_1->code == 'a'){
        ASSERT_TRUE(!root->node_1->node_0 && !root->node_1->node_1);
        EXPECT_EQ(root->node_1->count, 5);
        root = root->node_0;
    }
    else{
        ASSERT_TRUE(!root->node_0->node_1 && !root->node_0->node_0);
        root = root->node_1;
    }
    EXPECT_EQ(root->count, 3);
    ASSERT_TRUE(root->node_1 && root->node_0);
    ASSERT_TRUE(root->node_1->code == 'c' || root->node_0->code == 'c');
    ASSERT_TRUE(root->node_1->code == 'b' || root->node_0->code == 'b');

}
*/
TEST(TreeTest, IsCorrectGetCodes){
    vector<Node> counts(260);
    counts['a'].count = 10;
    counts['a'].code = 'a';

    counts['b'].count = 1;
    counts['b'].code = 'b';

    counts['c'].count = 2;

    counts['c'].code = 'c';
    Tree tree(counts);
    tree.count_codes();
    vector<vector<bool>> codes = tree.get_codes();
    ASSERT_TRUE(codes.size() > 3);
    ASSERT_TRUE(codes['a'].size() == 1);
    ASSERT_TRUE(codes['b'].size() == 2 && codes['c'].size() == 2);
    string b_code = bool_vector_to_string(codes['b']);
    string c_code = bool_vector_to_string(codes['c']);
    if(codes['a'][0] == true){
        ASSERT_TRUE((b_code == "01" && c_code == "00") || (b_code == "00" && c_code == "01"));
    }
    else{
        ASSERT_TRUE((b_code == "10" && c_code == "11") || (b_code == "11" && c_code == "10"));
    }
}



TEST(OptionsTest, WithNOcOru){
    bool wasException = true;
    char** argv = new char*[5];
    argv[0] = const_cast<char*>("huffman.exe");
    argv[1] = const_cast<char*>("-f");
    argv[2] = const_cast<char*>("file1");
    argv[3] = const_cast<char*>("-o");
    argv[4] = const_cast<char*>("file2");
    try{
        Options o1(5, argv);
        wasException = false;
    }
    catch(runtime_error& e){
        EXPECT_EQ(wasException, true);
        ASSERT_TRUE(!strcmp(e.what(), "no -c or -u"));
    }
    delete [] argv;
}

TEST(OptionsTest, WrongSequence){
    bool wasException = true;
    char** argv = new char*[6];
    argv[0] = const_cast<char*>("huffman.exe");
    argv[1] = const_cast<char*>("-u");
    argv[2] = const_cast<char*>("-f");
    argv[3] = const_cast<char*>("-o");
    argv[4] = const_cast<char*>("file1");
    argv[5] = const_cast<char*>("file2");
    try{
        Options o1(6, argv);
        wasException = false;
    }
    catch(runtime_error& e){
        EXPECT_EQ(wasException, true);
        ASSERT_TRUE(!strcmp(e.what(), "wrong option"));
    }
    delete [] argv;
}

TEST(OptionsTest, WithNOFile2){
    bool wasException = true;
    char** argv = new char*[5];
    argv[0] = const_cast<char*>("huffman.exe");
    argv[1] = const_cast<char*>("-c");
    argv[2] = const_cast<char*>("-f");
    argv[3] = const_cast<char*>("file1");
    argv[4] = const_cast<char*>("-o");
    try{
        Options o1(5, argv);
        wasException = false;
    }
    catch(runtime_error& e){
        EXPECT_EQ(wasException, true);
        ASSERT_TRUE(!strcmp(e.what(), "no in or out"));
    }
    delete [] argv;
}

TEST(OptionsTest, WithNOo){
    bool wasException = true;
    char** argv = new char*[4];
    argv[0] = const_cast<char*>("huffman.exe");
    argv[1] = const_cast<char*>("-f");
    argv[2] = const_cast<char*>("-o");
    argv[3] = const_cast<char*>("file1");
    try{
        Options o1(4, argv);
        wasException = false;
    }
    catch(runtime_error& e){
        EXPECT_EQ(wasException, true);
        ASSERT_TRUE(!strcmp(e.what(), "wrong option"));
    }
    delete [] argv;
}

TEST(OptionsTest, WrongOPtion){
    bool wasException = true;
    char** argv = new char*[6];
    argv[0] = const_cast<char*>("huffman.exe");
    argv[1] = const_cast<char*>("-c");
    argv[2] = const_cast<char*>("-lol");
    argv[3] = const_cast<char*>("-file1");
    argv[4] = const_cast<char*>("-o");
    argv[5] = const_cast<char*>("file2");
    try{
        Options o1(6, argv);
        wasException = false;
    }
    catch(runtime_error& e){
        EXPECT_EQ(wasException, true);
        ASSERT_TRUE(!strcmp(e.what(), "wrong option"));
    }
    delete [] argv;
}

TEST(OptionsTest, NotWrongOption2){
    bool wasException = true;
    char** argv = new char*[6];
    argv[0] = const_cast<char*>("huffman.exe");
    argv[1] = const_cast<char*>("-c");
    argv[2] = const_cast<char*>("--file");
    argv[3] = const_cast<char*>("-file1");
    argv[4] = const_cast<char*>("--output");
    argv[5] = const_cast<char*>("file2");
    try{
        Options o1(6, argv);
        wasException = false;
    }
    catch(runtime_error& e){
        ASSERT_TRUE(!strcmp(e.what(), "wrong option"));
    }
    EXPECT_EQ(wasException, false);
    delete [] argv;
}

TEST(ArchieveTest, Empty){
    ofstream out("test/empty");
    out.close();
    archive("test/empty", "test/empty.kek");
    ASSERT_TRUE(isEmptyFile("test/empty.kek"));
    unarchive("test/empty.kek", "test/empty2");
    ASSERT_TRUE(isEmptyFile("test/empty2"));
    system("rm test/empty.kek");
    system("rm test/empty2");
    system("rm test/empty");    

}

TEST(ArchieveTest, Easy){
    ofstream out("test/test_file");
    out << "abccccaaaaaabbbb";
    out.close();
    archive("test/test_file", "test/test_file.kek");
    unarchive("test/test_file.kek", "test/test_file_u");
    ASSERT_FALSE(system("diff -s test/test_file test/test_file_u"));
    system("rm test/test_file.kek");
    system("rm test/test_file");
    system("rm test/test_file_u"); 
}
