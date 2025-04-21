#include <bits/stdc++.h>
#include <fstream>
#include <iostream>

#include "functions.h"



using namespace std;


Block encrypt(Block plainText, vector<Block> roundKeys) {
    // add round key
    Block cipherText = addRoundKey(roundKeys[0], plainText);
    cout << "- Matrix 2x2 (AddRoundKey):" << endl;
    cipherText.print();

    // first round
    cout << "\n>>> Rodada 1:" << endl;
    
    cipherText = subNibbles(cipherText);
    cout << "- Matrix 2x2 (SubNibbles):" << endl;
    cipherText.print();

    cipherText = shiftRows(cipherText);
    cout << "- Matrix 2x2 (ShiftRows):" << endl;
    cipherText.print();

    cipherText = mixColumns(cipherText);
    cout << "- Matrix 2x2 (MixColumns):" << endl;
    cipherText.print();
    
    cipherText = addRoundKey(roundKeys[1], cipherText);
    cout << "- Matrix 2x2 (AddRoundKey):" << endl;
    cipherText.print();

    // second round
    cout << "\n>>> Rodada 2:" << endl;

    cipherText = subNibbles(cipherText);
    cout << "- Matrix 2x2 (SubNibbles):" << endl;
    cipherText.print();

    cipherText = shiftRows(cipherText);
    cout << "- Matrix 2x2 (ShiftRows):" << endl;
    cipherText.print();
    
    cipherText = addRoundKey(roundKeys[2], cipherText);
    cout << "- Matrix 2x2 (AddRoundKey):" << endl;
    cipherText.print();

    return cipherText;
}

int main() {
    string key;
    string plainText;
    
    // adquirir a mensagem
    cout << "Digite a mensagem: "; 
    cin >> plainText;
    // adquirir a chave
    cout << "Digite a chave: "; 
    cin >> key;
    
    // expansao de chave
    vector<Block> roundKeys = keyExpansion(
                                Block(
                                    Nibble(hexChar2Numero(key[0])), 
                                    Nibble(hexChar2Numero(key[1])),
                                    Nibble(hexChar2Numero(key[2])),
                                    Nibble(hexChar2Numero(key[3]))
                                )
                            );
    
    Block plainTextBlock, encryptedBlock;
    string textBlock;
    string encryptedText = "";

    for(int i = 0; i < plainText.size(); i+=2) {
        cout << "##############################" << endl;
        cout << "\t Bloco " << i/2 << endl;
        cout << "##############################" << endl;
        
        cout << ">>> Texto: " <<plainText.substr(i, 2) << endl;
        
        // padding caso necessário
        textBlock = plainText.substr(i, 2);
        if (textBlock.size() < 2) {
            textBlock += " ";
        }

        // formatando a string no formato de bloco 2x2 Nibble
        plainTextBlock = Block(textBlock);
        cout << ">>> Matrix 2x2 inicial:" << endl;
        plainTextBlock.print();

        // cifrando o bloco
        encryptedBlock = encrypt(plainTextBlock, roundKeys);
        // colocando no buffer
        
        cout << ">>> Matrix 2x2 criptograda: " << endl;
        encryptedBlock.print();
        encryptedText += encryptedBlock.toString();
        cout << endl;
    }

    cout << "Mensagem criptografada (base64): " << stringToBase64(encryptedText) << endl;

    return 0;
}
