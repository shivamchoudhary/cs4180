#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <openssl/evp.h>
#include <string>
#include <fstream>
#include <iostream>
#include <streambuf>
#include <sstream>
using namespace std;
void handleErrors(void){
        ERR_print_errors_fp(stderr);
        abort();
}
int encrypt(unsigned char *key, unsigned char *iv,unsigned char *ciphertext){
        EVP_CIPHER_CTX *ctx;
        int len;
        int ciphertext_len;
        printf("Encrypting with key %s\n",key);
        /* Create and initialise the context */
        if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();
        /* Initialise the encryption operation. IMPORTANT - ensure you use a key
        * and IV size appropriate for your cipher
        * In this example we are using 256 bit AES (i.e. a 256 bit key). The
        * IV size for *most* modes is the same as the block size. For AES this
        * is 128 bits */
        if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv))
        handleErrors();
        /* Provide the message to be encrypted, and obtain the encrypted output.
        * EVP_EncryptUpdate can be called multiple times if necessary
        */
        ifstream filestream;
        filestream.open("test.txt",ios::in);
        std::ifstream in("test.txt");
        std::string contents((std::istreambuf_iterator<char>(in)), 
        std::istreambuf_iterator<char>());
        
        /* Finalise the encryption. Further ciphertext bytes may be written at
        * this stage.
        */
        unsigned char *plaintext = (unsigned char *) contents.c_str();
        if (1!=EVP_EncryptUpdate(ctx,ciphertext,&len,plaintext,
                                strlen((char *)plaintext))) 
                handleErrors();
        ciphertext_len = len;
        if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)) 
        handleErrors();
        ciphertext_len += len;
        /* Clean up */
        EVP_CIPHER_CTX_free(ctx);
        return ciphertext_len;
}
int decrypt(unsigned char *ciphertext, int ciphertext_len, unsigned char *key,
                unsigned char *iv,unsigned char *plaintext){
        EVP_CIPHER_CTX *ctx;
        int len;
        int plaintext_len;
        /* Create and initialise the context */
        if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();
        /* Initialise the decryption operation. IMPORTANT - ensure you use a key
        * and IV size appropriate for your cipher
        * In this example we are using 256 bit AES (i.e. a 256 bit key). The
        * IV size for *most* modes is the same as the block size. For AES this
        * is 128 bits */
        if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv))
        handleErrors();
        /* Provide the message to be decrypted, and obtain the plaintext output.
        * EVP_DecryptUpdate can be called multiple times if necessary
        */
        if(1 != EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, 
                                ciphertext_len))
        handleErrors();
        plaintext_len = len;
        /* Finalise the decryption. Further plaintext bytes may be written at
        * this stage.
        */
        if(1 != EVP_DecryptFinal_ex(ctx, plaintext + len, &len)) handleErrors();
        plaintext_len += len;
        /* Clean up */
        EVP_CIPHER_CTX_free(ctx);
        return plaintext_len;
}

int start(unsigned char *inputkey){
        //unsigned char *key = (unsigned char *)"01234567890123456789012345678901";
        /* A 128 bit IV */
        unsigned char *key = (unsigned char *)inputkey;
        unsigned char *iv = (unsigned char *)"01234567890123456";

        /* Message to be encrypted */
        /* Buffer for ciphertext. Ensure the buffer is long enough for the
        * ciphertext which may be longer than the plaintext, dependant on the
        * algorithm and mode
        */
        unsigned char ciphertext[1000000];
        //unsigned char *plaintext =
                //(unsigned char *)"The quick brown fox jumps over the lazy dog";
        /* Buffer for the decrypted text */
        unsigned char decryptedtext[10000000];

        int decryptedtext_len;
        int ciphertext_len;
        /* Initialise the library */
        ERR_load_crypto_strings();
        OpenSSL_add_all_algorithms();
        OPENSSL_config(NULL);
        /* Encrypt the plaintext */
        ciphertext_len = encrypt (key, iv, ciphertext);
        /* Do something useful with the ciphertext here */
        printf("Ciphertext is:\n");
        BIO_dump_fp (stdout, (const char *)ciphertext, ciphertext_len);

        /* Decrypt the ciphertext */
        decryptedtext_len = decrypt(ciphertext, ciphertext_len, key, iv,
                        decryptedtext);

        /* Add a NULL terminator. We are expecting printable text */
        decryptedtext[decryptedtext_len] = '\0';

        /* Show the decrypted text */
        printf("Decrypted text is:\n");
        printf("%s\n", decryptedtext);

        /* Clean up */
        EVP_cleanup();
        ERR_free_strings();

        return 0;
}
 
