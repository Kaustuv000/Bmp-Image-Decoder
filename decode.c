#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include"bmpdecode.h"

int main()
{
	Image imageFile;

	imageFile.stream = fopen("sample.bmp","rb");

	read_bmp_header(&imageFile);

	
	read_dib_header(&imageFile);
	fclose(imageFile.stream);
	read_image(&imageFile);

	// FILE *fptr;
	// fptr = fopen("sample.bin","rb");
	
	return 0;
}