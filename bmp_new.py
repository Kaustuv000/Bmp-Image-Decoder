import math
import matplotlib.pyplot as plt
import numpy as np

dib_header_offset = 14

class BMP_header:

    def __init__(self):
        self.ftype = None
        self.File_size = None
        self.Reserved1 = None
        self.Reserved2 = None
        self.File_offset_to_pixel = None


class DIB_header:
    def __init__(self):
        self.header_size = None
        self.width = None
        self.height = None
        self.color_panel = None
        self.BitPerPixel = None
        self.compression = None
        self.image_size = None
        self.horizontal_resolution = None
        self.vertical_resolution = None
        self.num_color_palletes = None
        self.imp_colors = None

class BMPDecoder:

    def __init__(self, path):
        self.BMP_header = BMP_header()
        self.DIB_header = DIB_header()
        self.file = path

    def read_BMP_header(self):
        fd = open(self.file, 'rb')
        self.BMP_header.ftype = fd.read(2)
        self.BMP_header.File_size = int(readLE(fd.read(4)), 16)
        self.BMP_header.Reserved1 = int(readLE(fd.read(2)), 16)
        self.BMP_header.Reserved2 = int(readLE(fd.read(2)), 16)
        self.BMP_header.File_offset_to_pixel = int(readLE(fd.read(4)), 16)
        fd.close()
        return self.BMP_header

    def read_DIB_header(self):
        fd = open(self.file, 'rb')
        fd.seek(dib_header_offset)
        self.DIB_header.header_size = int(readLE(fd.read(4)), 16)
        self.DIB_header.width = int(readLE(fd.read(4)), 16)
        self.DIB_header.height = int(readLE(fd.read(4)), 16)
        self.DIB_header.color_panel = int(readLE(fd.read(2)), 16)
        self.DIB_header.BitPerPixel = int(readLE(fd.read(2)), 16)
        self.DIB_header.compression = int(readLE(fd.read(4)), 16)
        self.DIB_header.image_size = int(readLE(fd.read(4)), 16)
        self.DIB_header.horizontal_resolution = int(readLE(fd.read(4)), 16)
        self.DIB_header.vertical_resolution = int(readLE(fd.read(4)), 16)
        self.DIB_header.num_color_palletes = int(readLE(fd.read(4)), 16)
        self.DIB_header.imp_colors = int(readLE(fd.read(4)), 16)
        fd.close()
        return self.DIB_header

    def decode(self):
        if self.DIB_header.compression == 1:
            return self.rle_decode()
        else:    
            data = open(self.file, 'rb')
            rowsize = math.ceil(
                (self.DIB_header.BitPerPixel*self.DIB_header.width)/32)*4
            data.seek(self.BMP_header.File_offset_to_pixel)
            arr = []
            for rows in range(self.DIB_header.height):
                temp = list(data.read(rowsize))
                lines = np.array(temp, dtype=np.float32)
                arr.append(lines)
            data.close()
            return arr

    def rle_decode(self):
        image = [[255.0 for i in range(self.DIB_header.width)]
                 for j in range(self.DIB_header.height)]
        rowsize = math.ceil(
            (self.DIB_header.BitPerPixel*self.DIB_header.width)/32)*4

        data = open(self.file, 'rb')
        data.seek(self.BMP_header.File_offset_to_pixel)

        r, c = 0, 0
        count = 0
        if self.DIB_header.compression:
            while r < self.DIB_header.width:
                temp = list(data.read(2))

                #absolute mode
                if temp[0] == 0 and temp[1] == 0:
                    r += 1
                    c = 0

                elif (temp[0] == 0 and temp[1] == 1):
                    continue

                elif temp[0] == 0 and temp[1] == 2:
                    pos = list(data.read(2))

                    r_c = (c + pos[0])//self.DIB_header.width
                    r_cs = (c + pos[0]) % self.DIB_header.width
                    r += pos[1]

                    if r_c:
                        r += r_c
                        c = r_cs
                    else:
                        c += pos[0]

                else:
                    if temp[0] == 0:
                        for i in list(data.read(temp[1])):
                            if c >= self.DIB_header.width:
                                r += 1
                                c = 0
                            image[r][c] = float(i)
                            c += 1
                        data.read(16 - (temp[1]%16))

                    # encoded stream
                    else:
                        for j in [temp[1]]*temp[0]:
                            if c >= self.DIB_header.width:
                                r += 1
                                c = 0
                            image[r][c] = float(j)
                            c += 1
            return image                


def readLE(string):
    string = string.hex()
    reverse_string = ''
    length = len(string)
    while length:
        reverse_string += string[length-2:length]
        length -= 2
    return reverse_string

def fix_array(arr):
    new_arr = []
    final_img = []
    for i in range(len(arr)):
        final_img.append(arr[-i])
    return final_img

if __name__ == '__main__':

    bmp = BMPDecoder('sample.bmp')
    bmp_h = bmp.read_BMP_header()
    dib_h = bmp.read_DIB_header()
    print(bmp_h.__dict__)
    print(dib_h.__dict__)
    img = bmp.decode()
    plt.imshow(fix_array(img))
    plt.show()