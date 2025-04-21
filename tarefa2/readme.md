# UNIVERSIDADE DE BRASÍLIA (UNB)

## DEPARTAMENTO DE CIÊNCIA DA COMPUTAÇÃO

**TÓPICOS ESPECIAIS EM COMPUTADORES**

---

**TAREFA 2**

---

**GUSTAVO MELLO TONNERA**  
211055272

---

**Brasília - DF**  
**2025**

---

## Resumo

O presente relatório possui os resultados obtidos pelo estudantes Gustavo M Tonnera no desenvolvimento da Tarefa 2 da disciplina de Tópicos Especiais em Computadores ministrada pela professora Lorena de Souza Bezerra Borges. A tarefa consiste no desenvolvimento do algoritmo criptográfico S-AES, a fim de fixar os conceitos sobre criptografia apresentados durante as aulas.

**Palavras-chave:** tarefa; resultados; S-AES.

---

## 1. Introdução

A criptografia evoluiu significativamente ao longo da história, acompanhando o avanço das tecnologias e a crescente complexidade das ameaças à segurança da informação. Desde os métodos clássicos como a cifra de César, utilizada na Roma Antiga, até os complexos algoritmos modernos como RSA e AES, a criptografia passou de técnicas manuais e simbólicas para sistemas matemáticos robustos baseados em teoria dos números e computação. Com o surgimento da internet e a digitalização massiva de dados, a criptografia se tornou indispensável, sendo aplicada em diversas áreas, como comunicações seguras, transações financeiras, armazenamento em nuvem e autenticação de usuários. Hoje, com o avanço da computação quântica, novas abordagens como a criptografia pós-quântica estão sendo desenvolvidas, mostrando que a criptografia continua em constante evolução para atender às demandas de um mundo digital em transformação.

Com o objetivo de fixar os conceitos vistos em sala de aula, a Tarefa 2 foi proposta. A primeira parte da atividade consiste no desenvolvimento do algoritmo criptográfico S-AES. O S-AES (Simplified Advanced Encryption Standard) é uma versão simplificada do algoritmo AES, desenvolvida com fins educacionais para facilitar o entendimento dos princípios fundamentais da criptografia simétrica. Ele opera com blocos de 16 bits e chaves de 16 bits, utilizando operações semelhantes às do AES real, como substituição de bytes (SubBytes), permutação (ShiftRows), mistura de colunas (MixColumns) e adição de chave (AddRoundKey).

A segunda parte da tarefa caracteriza-se pelo desenvolvimento do modo de operação ECB para o algoritmo desenvolvido anteriormente. O modo de operação ECB (Electronic Codebook) é uma das formas mais simples de aplicar o algoritmo AES na criptografia de blocos de dados. Nesse modo, cada bloco de texto puro é criptografado de forma independente, utilizando a mesma chave para todos os blocos. Embora seja fácil de implementar, o ECB apresenta sérias vulnerabilidades de segurança, pois blocos idênticos de entrada geram blocos idênticos de saída, permitindo padrões visuais que podem ser explorados por atacantes.

Por fim, a última etapa envolve a implementação do algoritmo AES com o auxílio de uma biblioteca e na comparação dos seguintes modos de operação: ECB, CBC, CFB, OFB e CTR. Os resultados obtidos estão expostos na próximas seções do relatório.

---

## 2. Parte 1 - Implementação do S-AES

O S-AES (Simplified Advanced Encryption Standard) é uma versão didática do algoritmo AES original, projetada para facilitar o entendimento dos principais conceitos e operações envolvidas em criptografia simétrica por blocos. Ele mantém a estrutura geral do AES, mas opera com blocos e chaves de tamanho reduzido: enquanto o AES utiliza blocos de 128 bits e chaves de 128, 192 ou 256 bits, o S-AES trabalha com blocos e chaves de apenas 16 bits, tornando-o ideal para uso educacional. O processo de criptografia envolve uma etapa de expanção da chave, uma etapa de adição da chave de rodada e duas rodadas de operações principais, totalizando assim 4 etapas.

A etapa de expansão da chave (keyExpasion) é responsável por gerar três chaves de rodadas, a primeira consiste na chave original e é usada na operação de adição da chave antes das rodadas e as duas outras chaves são calculadas por meio de operações de rotação, substituição e XOR com constantes de rodada e são usadas uma em cada rodada para criptografar o blobo de texto.

```cpp

vector<Nibble> sbox = {
    Nibble(0x09), Nibble(0x04), Nibble(0x0A), Nibble(0x0B),
    Nibble(0x0D), Nibble(0x01), Nibble(0x08), Nibble(0x05),
    Nibble(0x06), Nibble(0x02), Nibble(0x00), Nibble(0x03),
    Nibble(0x0C), Nibble(0x0E), Nibble(0x0F), Nibble(0x07)
};

vector<Nibble> rcon = {Nibble(0x08), Nibble(0x03)};

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
};

```

A operação de adição da chave é feita uma vez antes das duas rodadas e uma vez em cada rodada. Essa operação consiste em um XOR entre o bloco e chave da rodada.

```cpp
Block addRoundKey(Block key, Block plainText) {
    return Block(
        Nibble(key.get()[0][0].get() ^ plainText.get()[0][0].get()),
        Nibble(key.get()[0][1].get() ^ plainText.get()[0][1].get()),
        Nibble(key.get()[1][0].get() ^ plainText.get()[1][0].get()),
        Nibble(key.get()[1][1].get() ^ plainText.get()[1][1].get())
    );
}
```

Durante as rodadas, operações de rotação e substituição são realizadas. Na primeira rodada, a primeira operação feita é uma operação de substituição (SubNibbles), a qual consiste na substituição dos Nibbles do bloco. Em seguida, é realizada uma operação de permutação entre os 2 últimos Nibbles do bloco. Em sequência, é realizada uma operação de mistura de colunas (MixColumns), na qual cada coluna da matriz 2x2 é transformada através de uma multiplicação em um campo finito (GF(2⁴)), utilizando uma matriz fixa. Essa operação mistura os dados de forma a aumentar ainda mais a difusão, espalhando os bits dos nibbles por toda a estrutura. Foi utilzada uma tabela de multiplicação para calcular as mutiplicações de maneira mais eficiente. Por fim, uma nova operação de adição de chave é feita, porém a segunda chave de rodada.

```cpp

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

```

Utilizando as funções expostas, desenvolveu-se a seguinte função:

```cpp
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

```

As seguintes Structs foram desenvolvidas para auxiliar no desenvolvimento do algoritmo:

```cpp

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

```

Elas foram úteis para lidar com dados com apenas 4 bits, tipo de dados que o C++ não possui. A Struct Nibble simula a implementação de um número de 4 bits e a Struct Block simula a implementação de uma matrix 2x2 de nibbles.

### 2.1 Diferença entre AES e S-AES

O S-AES e o AES apresentam diferenças estruturais e operacionais importantes. O S-AES utiliza blocos e chaves de 16 bits, enquanto o AES trabalha com blocos de 128 bits e chaves de 128, 192 ou 256 bits. O número de rodadas também varia: o S-AES realiza 2 rodadas, enquanto o AES realiza entre 10 e 14 rodadas, dependendo do tamanho da chave. Além disso, embora ambos os algoritmos compartilhem operações como SubBytes, ShiftRows e AddRoundKey, o AES inclui uma operação adicional, a Mistura de Colunas (MixColumns), que promove uma maior difusão e torna o processo de criptografia mais complexo. O S-AES, por sua vez, simplifica ou omite essa operação, tornando o algoritmo mais vulnerável a ataques. A combinação dessas diferenças resulta em um nível de segurança significativamente maior no AES.

Em termos de aplicação e segurança, o S-AES foi projetado para fins educacionais, não sendo seguro para uso prático. Ele permite entender os conceitos básicos de criptografia por blocos, mas não oferece a resistência necessária para proteger dados sensíveis. Já o AES é amplamente utilizado em contextos de alta segurança, como em transações financeiras, comunicação segura e armazenamento de dados. O AES é considerado um dos algoritmos mais seguros, adotado globalmente em sistemas críticos para proteção de informações confidenciais.

---

## 3. Parte 2 – Implementação do Modo de Operação ECB com o S-AES

---

## 4. Parte 3 – Simulação com AES Real usando Bibliotecas Criptográficas

---

## Referências

Liste todas as obras consultadas, em ordem alfabética, conforme a ABNT (NBR 6023:2018). Exemplos:

- SILVA, João. _Introdução à Programação_. 2. ed. São Paulo: Editora Técnica, 2020.
- SOUZA, Maria. _Aprendizado de Máquina Aplicado_. Rio de Janeiro: Ciência Moderna, 2021.

---
