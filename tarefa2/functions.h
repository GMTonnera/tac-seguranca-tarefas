#include <bits/stdc++.h>

using namespace std;

struct Nibble {
    private:
        uint8_t value;
    
    public:
        Nibble(uint8_t n = 0);
        void set(uint8_t n);
        uint8_t get();
};

struct Block {
    private:
        vector<vector<Nibble>> value;
    
    public:
        Block(Nibble n1, Nibble n2, Nibble n3, Nibble n4);
        Block(string s);
        Block();
        void set(Nibble n1, Nibble n2, Nibble n3, Nibble n4);
        vector<vector<Nibble>> get();
        void print();
        string toString();
};


extern vector<Nibble> sbox;

extern vector<vector<uint8_t>> gf16_mutiplication;

extern vector<Nibble> rcon;

Block addRoundKey(Block key, Block plainText);

Block subNibbles(Block plainText);

Block shiftRows(Block plainText);

Block mixColumns(Block plainText);

vector<Block> keyExpansion(Block key);

int hexChar2Numero(char c);

string stringToBase64(const string& s);