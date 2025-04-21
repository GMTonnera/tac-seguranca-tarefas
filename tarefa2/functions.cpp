#include <bits/stdc++.h>

#include "functions.h"

using namespace std;

Nibble::Nibble(uint8_t n) {
    set(n);
};

void Nibble::set(uint8_t n) {
    if(n > 0x0F) {
        throw out_of_range("Value error: Nibble value must be between 0 and 15.");
    }
    value = n;
};

uint8_t Nibble::get() {
    return value;
};

Block::Block(Nibble n1, Nibble n2, Nibble n3, Nibble n4) {
    set(n1, n2, n3, n4);
};

Block::Block(string s) {
    if (s.size() != 2) {
        throw out_of_range("Value error: The string's length must equal to 2.");
    }
    unsigned char c1 = static_cast<unsigned char>(s[0]);
    unsigned char c2 = static_cast<unsigned char>(s[1]);
    
    uint8_t n1 = (c1 >> 4) & 0x0F; 
    uint8_t n2 = c1 & 0x0F;
    uint8_t n3 = (c2 >> 4) & 0x0F;
    uint8_t n4 = c2 & 0x0F;

    set(Nibble(n1), Nibble(n2), Nibble(n3), Nibble(n4));
};

Block::Block(){};

void Block::set(Nibble n1, Nibble n2, Nibble n3, Nibble n4) {
    value = {
        {n1, n2},
        {n3, n4}
    };
};

vector<vector<Nibble>> Block::get() {
    return value;
};

void Block::print() {
    cout << "0x" << hex << uppercase << setw(2) << setfill('0') << static_cast<int>(value[0][0].get()) << " "
            << "0x" << hex << uppercase << setw(2) << setfill('0') << static_cast<int>(value[0][1].get()) << "\n" 
            << "0x" << hex << uppercase << setw(2) << setfill('0') << static_cast<int>(value[1][0].get()) << " "
            << "0x" << hex << uppercase << setw(2) << setfill('0') << static_cast<int>(value[1][1].get()) << "\n"; 
};

string Block::toString() {
    char c1 = static_cast<char>((value[0][0].get() << 4) + value[0][1].get());
    char c2 = static_cast<char>((value[1][0].get() << 4) + value[1][1].get());

    return string({c1,c2});
}

vector<Nibble> sbox = {
    Nibble(0x09), Nibble(0x04), Nibble(0x0A), Nibble(0x0B),
    Nibble(0x0D), Nibble(0x01), Nibble(0x08), Nibble(0x05),
    Nibble(0x06), Nibble(0x02), Nibble(0x00), Nibble(0x03),
    Nibble(0x0C), Nibble(0x0E), Nibble(0x0F), Nibble(0x07)
};

vector<vector<uint8_t>> gf16_mutiplication = {
    {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00},
    {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F},
    {0x00, 0x02, 0x04, 0x06, 0x08, 0x0A, 0x0C, 0x0E, 0x03, 0x01, 0x07, 0x05, 0x0B, 0x09, 0x0F, 0x0D},
    {0x00, 0x03, 0x06, 0x05, 0x0C, 0x0F, 0x0A, 0x09, 0x08, 0x0D, 0x0E, 0x07, 0x04, 0x01, 0x02, 0x0B},
    {0x00, 0x04, 0x08, 0x0C, 0x03, 0x07, 0x0B, 0x0F, 0x06, 0x02, 0x0E, 0x0A, 0x05, 0x01, 0x0D, 0x09},
    {0x00, 0x05, 0x0A, 0x0F, 0x07, 0x02, 0x0D, 0x08, 0x0E, 0x0B, 0x04, 0x01, 0x09, 0x0C, 0x03, 0x06},
    {0x00, 0x06, 0x0C, 0x0A, 0x0B, 0x0D, 0x07, 0x01, 0x05, 0x03, 0x09, 0x0F, 0x0E, 0x08, 0x02, 0x04},
    {0x00, 0x07, 0x0E, 0x09, 0x0F, 0x08, 0x01, 0x06, 0x0D, 0x0A, 0x03, 0x04, 0x02, 0x05, 0x0C, 0x0B},
    {0x00, 0x08, 0x03, 0x0B, 0x06, 0x0E, 0x05, 0x0D, 0x0C, 0x04, 0x0F, 0x07, 0x0A, 0x02, 0x09, 0x01},
    {0x00, 0x09, 0x01, 0x08, 0x02, 0x0B, 0x03, 0x0A, 0x04, 0x0D, 0x05, 0x0C, 0x06, 0x0F, 0x07, 0x0E},
    {0x00, 0x0A, 0x07, 0x0D, 0x0E, 0x04, 0x09, 0x03, 0x0F, 0x05, 0x08, 0x02, 0x01, 0x0B, 0x06, 0x0C},
    {0x00, 0x0B, 0x05, 0x0E, 0x0A, 0x01, 0x0F, 0x04, 0x07, 0x0C, 0x02, 0x09, 0x0D, 0x06, 0x08, 0x03},
    {0x00, 0x0C, 0x0B, 0x07, 0x05, 0x09, 0x0E, 0x02, 0x0A, 0x06, 0x01, 0x0D, 0x0F, 0x03, 0x04, 0x08},
    {0x00, 0x0D, 0x09, 0x04, 0x01, 0x0C, 0x08, 0x05, 0x02, 0x0F, 0x0B, 0x06, 0x03, 0x0E, 0x0A, 0x07},
    {0x00, 0x0E, 0x0F, 0x01, 0x0D, 0x03, 0x02, 0x0C, 0x09, 0x07, 0x06, 0x08, 0x04, 0x0A, 0x0B, 0x05},
    {0x00, 0x0F, 0x0D, 0x02, 0x09, 0x06, 0x04, 0x0B, 0x01, 0x0E, 0x0C, 0x03, 0x08, 0x07, 0x05, 0x0A}
};

vector<Nibble> rcon = {Nibble(0x08), Nibble(0x03)};

Block addRoundKey(Block key, Block plainText) {
    return Block(
        Nibble(key.get()[0][0].get() ^ plainText.get()[0][0].get()),
        Nibble(key.get()[0][1].get() ^ plainText.get()[0][1].get()),
        Nibble(key.get()[1][0].get() ^ plainText.get()[1][0].get()),
        Nibble(key.get()[1][1].get() ^ plainText.get()[1][1].get())    
    );
}

Block subNibbles(Block plainText) {
    return Block(
        sbox[plainText.get()[0][0].get()],
        sbox[plainText.get()[0][1].get()],
        sbox[plainText.get()[1][0].get()],
        sbox[plainText.get()[1][1].get()]
    );
}

Block shiftRows(Block plainText) {
    return Block(
        plainText.get()[0][0], plainText.get()[0][1], plainText.get()[1][1], plainText.get()[1][0]
    );
}

Block mixColumns(Block plainText) {
    return Block(
        Nibble(gf16_mutiplication[plainText.get()[0][0].get()][1] ^ gf16_mutiplication[plainText.get()[0][1].get()][4]),
        Nibble(gf16_mutiplication[plainText.get()[0][0].get()][4] ^ gf16_mutiplication[plainText.get()[0][1].get()][1]),
        Nibble(gf16_mutiplication[plainText.get()[1][0].get()][1] ^ gf16_mutiplication[plainText.get()[1][1].get()][4]),
        Nibble(gf16_mutiplication[plainText.get()[1][0].get()][4] ^ gf16_mutiplication[plainText.get()[1][1].get()][1])
    );
}

vector<Block> keyExpansion(Block key) {
    vector<Block> roundKeys;
    // roundKey0 --> chave original
    roundKeys.push_back(key);

    for(int i = 0; i < 2; i++) {
        vector<Nibble> b0 = roundKeys[i].get()[0];
        vector<Nibble> b1 = roundKeys[i].get()[1];
        // g function
        // RotWord
        vector<Nibble> g_b1 = {b1[1], b1[0]};
        // SubWord
        g_b1 = {sbox[b1[0].get()], sbox[b1[1].get()]};    
        // rcon
        g_b1 = {Nibble(b1[0].get() ^ rcon[0].get()), Nibble(b1[1].get() ^ 0x00)};

        vector<Nibble> b2 = {static_cast<uint8_t>(b0[0].get() ^ g_b1[0].get()), static_cast<uint8_t>(b0[1].get() ^ g_b1[1].get())};
        vector<Nibble> b3 = {static_cast<uint8_t>(b2[0].get() ^ b1[0].get()), static_cast<uint8_t>(b2[1].get() ^ b1[1].get())};
        roundKeys.push_back(Block(b2[0], b2[1], b3[0], b3[1]));
    }

    return roundKeys;
}

int hexChar2Numero(char c) {
    if (c >= '0' && c <= '9')
        return c - '0';          // '0' a '9' → 0 a 9
    else if (c >= 'A' && c <= 'F')
        return 10 + (c - 'A');   // 'A' a 'F' → 10 a 15
    else if (c >= 'a' && c <= 'f')
        return 10 + (c - 'a');   // 'a' a 'f' → 10 a 15
    else
        throw std::invalid_argument("Caractere inválido para hexadecimal.");
}

string stringToBase64(const string& s) {
    static const std::string base64_chars =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789+/";

    string output;
    int val = 0, valb = -6;

    for (unsigned char c : s) {
        val = (val << 8) + c;
        valb += 8;

        while (valb >= 0) {
            output.push_back(base64_chars[(val >> valb) & 0x3F]);
            valb -= 6;
        }
    }

    if (valb > -6) {
        output.push_back(base64_chars[((val << 8) >> (valb + 8)) & 0x3F]);
    }

    while (output.size() % 4) {
        output.push_back('=');
    }

    return output;
}