#!/usr/bin/env python3

import sys
from PyPDF2 import PdfFileReader
from PIL import Image


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} pdf_file'.format(sys.argv[0]))
        sys.exit()

    pdf = open(sys.argv[1], 'rb')
    reader = PdfFileReader(pdf)
    n = reader.getNumPages()

    for i in range(n):
        page = reader.getPage(i)
        try:
            objs = page['/Resources']['/XObject']
        except KeyError:
            continue

        for key in objs:
            obj = objs[key]
            if obj['/Subtype'] != '/Image':
                continue

            name = 'P{}-{}'.format(i, key[1:])
            data = obj.getData()

            if '/Filter' in obj:
                ext = '.png'
                if obj['/Filter'] == '/DCTDecode':
                    ext = '.jpg'
                elif obj['/Filter'] == '/JPXDecode':
                    ext = '.jp2'
                elif obj['/Filter'] == '/CCITTFaxDecode':
                    ext = '.tif'
                name += ext
                if ext != '.png':
                    with open(name) as im:
                        im.write(data)
                    print('Save image ' + name)
                    continue

            size = (obj['/Width'], obj['/Height'])

            if obj['/ColorSpace'] == '/DeviceRGB':
                mode = 'RGB'
            else:
                mode = 'P'

            im = Image.frombytes(mode, size, data)
            im.save(name)
            print('Save image ' + name)

    pdf.close()
