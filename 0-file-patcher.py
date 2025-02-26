"""
TSTO 0-file-Patcher.
WARNING: absolutly no warranties. Use this script at own risk.
"""

__author__ = 'info@damarist.de'

import os
import shutil
import binascii
import glob
import zlib
import forcecrc32
import lxml.etree as ET

header1 = '4247726d0302'
header3 = '008f0042312f20204372656174656420616e64205061636b6564206279204a6541664b6527532020302066696c652047656e657261746f722026205061636b657220202f31000001000802310001'
header2 = '008f00642f626c6120626c6120626c61205649502d4841434b2064616d61723173745c2773205453544f20476f6420444c432047656e657261746f72202d204d6573732077697468207468652062657374202d20646965206c696b652074686520726573742f31000001000802310001'
spacer1 = '0004'
spacer2 = '00010000'
zeSi = '00010203'
duCrc = '33333333'


def create():
    print("Removing temp files")
    for file in ["temp/build1", "temp/build2", "temp/build3", "output/0", "output/1"]:
        if os.path.exists(file):
            os.remove(file)

    print("Converting hex to ASCII")
    shutil.make_archive('1', format="zip", root_dir='modded-1-files')
    os.rename('1.zip', 'output/1')

    with open('output/1', 'rb') as f:
        filedata = f.read()

    crc = binascii.crc32(filedata) & 0xFFFFFFFF
    crcHex = format(crc, '08x')
    crcAsc = binascii.unhexlify(crcHex)
    print("CRC2:", crcAsc)

    directory = 'modded-1-files'
    count = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
    countHex = format(count, '04x')
    countAsc = binascii.unhexlify(countHex)

    header1Asc = binascii.unhexlify(header1)
    header2Asc = binascii.unhexlify(header2)
    ducrcAsc = binascii.unhexlify(duCrc)

    print("Creating 1 file")
    for file in glob.glob("modded-1-files/*.*"):
        files = os.path.basename(file)
        sfile = files.split(".")
        fsize = os.path.getsize(file)

        leng = len(files) + 1
        fileHex = format(leng, '02x')
        fileAsc = binascii.unhexlify(fileHex)

        file2Hex = format(leng, '04x')
        file2Asc = binascii.unhexlify(file2Hex)

        att = len(sfile[1]) + 1
        attHex = format(att, '04x')
        attAsc = binascii.unhexlify(attHex)

        sizeHex = format(fsize, '010x')
        sizeAsc = binascii.unhexlify(sizeHex)
        spacer2Asc = binascii.unhexlify(spacer2)
        zeSiAsc = binascii.unhexlify(zeSi)

        build = fileAsc + files.encode() + attAsc + sfile[1].encode() + files.encode() + sizeAsc + spacer2Asc
        buildlen = len(build) + 2
        buildHex = format(buildlen, '04x')
        buildAsc = binascii.unhexlify(buildHex)
        build1 = buildAsc + fileAsc + files.encode() + attAsc + sfile[
            1].encode() + file2Asc + files.encode() + sizeAsc + spacer2Asc

        with open('temp/build1', 'ab') as f:
            f.write(build1)

    with open('temp/build1', 'rb') as f:
        red = f.read()

    build2 = header1Asc + zeSiAsc + header2Asc + crcAsc + countAsc + red + ducrcAsc
    with open('temp/build2', 'wb') as f:
        f.write(build2)

    print("Creating 0 file")
    bsize = os.path.getsize('temp/build2')
    bsizeHex = format(bsize, '08x')
    bsizeAsc = binascii.unhexlify(bsizeHex)

    build3 = header1Asc + bsizeAsc + header2Asc + crcAsc + countAsc + red
    with open('temp/build3', 'wb') as f:
        f.write(build3)

    with open('temp/build3', 'rb') as f:
        filedata2 = f.read()

    crc2 = binascii.crc32(filedata2) & 0xFFFFFFFF
    crc2Hex = format(crc2, '08x')
    crc2Asc = binascii.unhexlify(crc2Hex)

    with open('output/0', 'wb') as f:
        f.write(filedata2 + crc2Asc)



def crc():
    with open("original-0-file/0", 'rb') as f:
        file_content = f.read()

    crc32 = zlib.crc32(file_content) & 0xFFFFFFFF
    crcHex = format(crc32, '08x')
    print("CRC32:", crcHex)

    # Anstatt os.system zu nutzen, rufen wir die Funktion direkt auf
    forcecrc32.update_crc("output/0", 18,
                          crcHex)  # Beispielhafte Funktion, anpassen je nach Implementierung in forcecrc32.py


def main():
    ascii_art = """
                         _             _   _            
  ___  _ __  ___   __ _ | |_  ___   __| | | |__   _   _ 
 / __|| '__|/ _ \ / _` || __|/ _ \ / _` | | '_ \ | | | |
| (__ | |  |  __/| (_| || |_|  __/| (_| | | |_) || |_| |
 \___||_|   \___| \__,_| \__|\___| \__,_| |_.__/  \__, |
     _                                 _       _  |___/ 
  __| |  __ _  _ __ ___    __ _  _ __ / | ___ | |_      
 / _` | / _` || '_ ` _ \  / _` || '__|| |/ __|| __|     
| (_| || (_| || | | | | || (_| || |   | |\__ \| |_      
 \__,_| \__,_||_| |_| |_| \__,_||_|   |_||___/ \__|     

    """
    print(ascii_art)

    while True:
        print("\nMenu:")
        print("1. Patch Files")
        print("2. Patch Signature")
        print("3. Exit")

        choice = input("Wähle eine Option (1-3): ")

        if choice == '1':
            create()
        elif choice == '2':
            crc()
        elif choice == '3':
            print("exiting...")
            break
        else:
            print("WTF ???")


if __name__ == "__main__":
    main()
