#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/aes.h>
 
/* AES key for Encryption and Decryption */
const static unsigned char aes_key[]={0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xAA,0xBB,0xCC,0xDD,0xEE,0xFF};
 
/* Print Encrypted and Decrypted data packets */
void print_data(const char *tittle, const void* data, int len);
 
int main( )
{
	/* Input data to encrypt */
	unsigned char aes_input[]={0x0,0x1,0x2,0x3,0x4,0x5};
	
	/* Init vector */
	unsigned char iv[AES_BLOCK_SIZE];
	memset(iv, 0x00, AES_BLOCK_SIZE);
	
	/* Buffers for Encryption and Decryption */
	unsigned char enc_out[sizeof(aes_input)];
	unsigned char dec_out[sizeof(aes_input)];
	
	/* AES-128 bit CBC Encryption */
	AES_KEY enc_key, dec_key;
	AES_set_encrypt_key(aes_key, sizeof(aes_key)*8, &enc_key);
	AES_cbc_encrypt(aes_input, enc_out, sizeof(aes_input), &enc_key, iv, AES_ENCRYPT);
	/* AES-128 bit CBC Decryption */
	memset(iv, 0x00, AES_BLOCK_SIZE); // don't forget to set iv vector again, else you can't decrypt data properly
	AES_set_decrypt_key(aes_key, sizeof(aes_key)*8, &dec_key); // Size of key is in bits
	AES_cbc_encrypt(enc_out, dec_out, sizeof(aes_input), &dec_key, iv, AES_DECRYPT);
	
	/* Printing and Verifying */
	print_data("\n Original ",aes_input, sizeof(aes_input)); // you can not print data as a string, because after Encryption its not ASCII
	
	print_data("\n Encrypted",enc_out, sizeof(enc_out));
	
	print_data("\n Decrypted",dec_out, sizeof(dec_out));
	
	return 0;
}
 
void print_data(const char *tittle, const void* data, int len)
{
	printf("%s : ",tittle);
	const unsigned char * p = (const unsigned char*)data;
	int i = 0;
	
	for (; i<len; ++i)
		printf("%02X ", *p++);
	
	printf("\n");
}

/*#include<iostream>*/
//#include<openssl/aes.h>


//using namespace std;
//static const unsigned char key[] = {
    //0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
    //0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff,
    //0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
    //0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f
//};

//int main()
//{
    //unsigned char text[]="hello world!";
    //unsigned char iv[AES_BLOCK_SIZE];
    //memset (iv,0X00,AES_BLOCK_SIZE);
    //unsigned char enc_out[sizeof(text)];
    //unsigned char dec_out[sizeof(text)];
    //AES_KEY enc_key, dec_key;
    //AES_set_encrypt_key(key, sizeof(key)*8, &enc_key);
    //AES_cbc_encrypt(text, enc_out, sizeof(text),&enc_key,iv,AES_ENCRYPT);      
    //memset (iv,0X00,AES_BLOCK_SIZE);
    //AES_set_decrypt_key(key,sizeof(key)*8,&dec_key);
    //AES_cbc_encrypt(enc_out, dec_out, sizeof(text),&dec_key,iv,AES_DECRYPT);

    //int i;

    //cout<<"original:\t";
    //for(i=0;*(text+i)!=0x00;i++)
        //cout<<*(text+i);
    //cout<<"\nencrypted:\t";
    //for(i=0;*(enc_out+i)!=0x00;i++)
        //cout<<*(enc_out+i);
    //printf("\ndecrypted:\t");
    //for(i=0;*(dec_out+i)!=0x00;i++)
        //cout<<*(dec_out+i);
    //[>printf("\n");<]

    //return 0;
/*}*/ 
