#include <iostream>
#include <fstream>
#include <string>
#include <openssl/evp.h>
#include <openssl/evp.h>
#include <sstream>
#include <openssl/sha.h> 
using namespace std;
bool readfile(string fname){
        string line;
        ifstream file (fname);
        if (file.is_open()){
                while (getline (file,line)){
                cout<<line<<"\n";
                }
                file.close();
                return true;
        }
        else{
                cout<<"Unable to open the file";
                return false;
        }
}
string to_hex(unsigned char s) {
    stringstream ss;
    ss << hex << (int) s;
    return ss.str();
}   

string sha256(string line) {    
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, line.c_str(), line.length());
    SHA256_Final(hash, &sha256);

    string output = "";    
    for(int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        output += to_hex(hash[i]);
    }
    return output;
}

int sha() {
     std::ifstream t("test.txt");
     std::stringstream buffer;
     buffer << t.rdbuf();
     cout << sha256(buffer.str()) << endl;
     return 0;
}


