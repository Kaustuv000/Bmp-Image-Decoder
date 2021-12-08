#include <stdint.h>
#include <stdio.h>

typedef struct
{
	uint16_t ftype;        // size 2 bytes
	uint32_t fileSize;     // size 4 bytes
	uint16_t Reserved1;	   // size 2 bytes
	uint16_t Reserved2;	   // size 2 bytes
	uint32_t file_offset_array;  // size 4 bytes	

} BMP_HEADER;

typedef struct
{
	uint32_t header_size;     // size 4 bytes
	int32_t width;			  // size 2 bytes
	int32_t height;			  // size 2 bytes
	uint16_t color_panel;	  // size 2 bytes
	uint16_t bits_per_pixel;  // size 2 bytes
	uint32_t compression;     // size 2 bytes
	
} DIB_HEADER;

typedef struct{
	BMP_HEADER bmp;
	DIB_HEADER dib;
	FILE *stream;
} Image;

void read_bmp_header(Image *imageFile);
void read_dib_header(Image *imageFile);
void read_image(Image *imageFile);
