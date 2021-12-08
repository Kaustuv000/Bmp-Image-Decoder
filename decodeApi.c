#include <stdio.h>
#include <stdlib.h>
#include "bmpdecode.h"

void read_bmp_header(Image *imageFile)
{
	fread(&imageFile->bmp.ftype,sizeof(imageFile->bmp.ftype),1,imageFile->stream);
	fread(&imageFile->bmp.fileSize,sizeof(imageFile->bmp.fileSize),1,imageFile->stream);
	fread(&imageFile->bmp.Reserved1,sizeof(imageFile->bmp.Reserved1),1,imageFile->stream);
	fread(&imageFile->bmp.Reserved2,sizeof(imageFile->bmp.Reserved2),1,imageFile->stream);
	fread(&imageFile->bmp.file_offset_array,sizeof(imageFile->bmp.file_offset_array),1,imageFile->stream);
}

void read_dib_header(Image *imageFile)
{
	fread(&imageFile->dib.header_size,sizeof(imageFile->dib.header_size),1,imageFile->stream);
	fread(&imageFile->dib.width,sizeof(imageFile->dib.width),1,imageFile->stream);
	fread(&imageFile->dib.height,sizeof(imageFile->dib.height),1,imageFile->stream);
	fread(&imageFile->dib.color_panel,sizeof(imageFile->dib.color_panel),1,imageFile->stream);
	fread(&imageFile->dib.bits_per_pixel,sizeof(imageFile->dib.bits_per_pixel),1,imageFile->stream);
	fread(&imageFile->dib.compression,sizeof(imageFile->dib.compression),1,imageFile->stream);
}

void read_image(Image *imageFile)
{
	imageFile->stream = fopen("sample.bmp","rb");
	fseek(imageFile->stream,imageFile->bmp.file_offset_array,SEEK_CUR);
	FILE *image;
	image = fopen("sample.txt","w");

	int size = imageFile->dib.height*imageFile->dib.width;
	unsigned char imageArray[size];

	for(int i=1;i<size+1;i++)
	{
		fwrite(&imageArray[i],1,1,image);
		if(i%imageFile->dib.width==0)
		{
			fwrite("\n",1,1,image);
		}
	}
	fclose(image);
	fclose(imageFile->stream);
}