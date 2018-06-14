#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
The MIT License

Copyright (c) 2016 Ronald Cotton

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import sys
import os
import array   # for the multidimentional array of the bitmap


def convertcsv2bitmaporiginal(l,outputFile,ext):
  '''
  converts the comma delimited table into a bitmap.
  this only works with the following database schema:
    first element: cat, dog, turtle, bird
    second element: 1-100
    third element: True, False
  :param l: data to be processed
  :param outputFile: returns file
  :param ext: file extension
  :return:
  '''

  i = 0             # start with 0 -> 15
  size = len(l)			# table rows
  str = ""					# showing str needs to start empty
  output = [[[] for y in range(size) ] for y in range(16) ]

  for each in l:
    Animal, Age, Adopted = each.split(',')	# place the tuple into string variables

    for x in range(0,16):
      output[x][i]='0'					# clear first element in array
    if Animal == 'cat':					# Animal Type
      output[0][i]='1'
    if Animal == 'dog':
      output[1][i]='1'
    if Animal == 'turtle':
      output[2][i]='1'
    if Animal == 'bird':
      output[3][i]='1'
    if 1 <= int(Age) <= 10:     # Animal Age
      output[4][i] = '1'					# binning in groups of 10
    if 11 <= int(Age) <= 20:
      output[5][i] = '1'
    if 21 <= int(Age) <= 30:
      output[6][i] = '1'
    if 31 <= int(Age) <= 40:
      output[7][i] = '1'
    if 41 <= int(Age) <= 50:
      output[8][i] = '1'
    if 51 <= int(Age) <= 60:
      output[9][i] = '1'
    if 61 <= int(Age) <= 70:
      output[10][i] = '1'
    if 71 <= int(Age) <= 80:
      output[11][i] = '1'
    if 81 <= int(Age) <= 90:
      output[12][i] = '1'
    if 91 <= int(Age) <= 100:
      output[13][i] = '1'
    if Adopted == 'True\n':			# Animal Adopted
      output[14][i] = '1'					# 10 - true
      output[15][i] = '0'
    if Adopted == 'False\n':
      output[14][i] = '0'					# 01 - false
      output[15][i] = '1'
    i+=1
  for x in range(0,16):					# convert array to str
    str += ''.join(output[x])
    str += "\n"
  outputFile += ext
  outFile = open(outputFile,"w")
  outFile.write(str)
  outFile.close()
# end convertcsv2bitmaporiginal()


def compresslinewah(line,bits):
  '''
  compress bitmap index using WAH
  :param line: Lined of the bitmap index (uncompressed)
  :param bits: Number of bits - 1
  :return: Compressed String
  '''
  input_str_len = len(line)-1
  return_str = ""
  form_str = "{0:0"+str(bits-1)+"b}"                # used to create compressed str
  compressing = -1
  num_of_bits = 0

  for i in range(0,input_str_len,bits):            # for (i=0;i<input_str_len;i+=bits)
    if ( bits > (input_str_len-i)):                 # tail of line
      if (compressing != -1):
        return_str += "1" + str(compressing) + form_str.format(num_of_bits)
      return_str += "0" + line[i:input_str_len]
      return return_str
    if (line[i:i+bits] == "".rjust(bits,str(0))):   # compressible 0
      if (compressing == -1):
        compressing = 0
        num_of_bits = 1
        continue
      if (compressing == 0):
        num_of_bits += 1
        if (num_of_bits > (pow(2,bits)-1)):
          return_str += "10" + "".rjust(bits,str(1))
          num_of_bits = 1
        continue
      if (compressing != 0):
        return_str += "1" + str(compressing) + form_str.format(num_of_bits)
        compressing = 0
        num_of_bits = 1
        continue
    if (line[i:i+bits] == "".rjust(bits,str(1))):   # compressible 1
      if (compressing == -1):
        compressing = 1
        num_of_bits = 1
        continue
      if (compressing == 1):
        num_of_bits += 1
        if (num_of_bits > (pow(2,bits)-1)):
          return_str += "11" + "".rjust(bits,str(1))
          num_of_bits = 1
        continue
      if (compressing != 1):
        return_str += "1" + str(compressing) + form_str.format(num_of_bits)
        compressing = 1
        num_of_bits = 1
        continue
    if (compressing != -1):                         # compressing & not end of line
      return_str += "1" + str(compressing) + form_str.format(num_of_bits)
    return_str += "0" + line[i:i+bits]
    compressing = -1
    num_of_bits = 0

  return return_str																	# reaches this if the number of entries = mod bits


def convertbm2bitmapcompress(basefn, in_ext, out_ext, bits):
  '''
  converts bitmap index into a compressed bitmap

  :param basefn: base filename
  :param in_ext: input extension
  :param out_ext: output extension
  :param bits: number of bits that are being compressed
  :return: Nothing
  '''
  compressBits = bits - 1;					# elements compressed
  compressed = [None]*16						# empty array
  bmlines = openFileReturnLines(basefn+in_ext)
  for x in range(0,16):						# compress 1 line - loop
    compressed[x] = compresslinewah(bmlines[x],compressBits)
  outFile = open(basefn+out_ext,"w")
  for line in compressed:
    outFile.write("%s\n" % line);
  outFile.close()


def openFileReturnLines(filename):
  '''
  open filename and return an array of lines - used by main() and convertbm2bitmapcompress()
  :param filename:
  :return: returns all lines from file
  '''
  with open(filename) as f:
    lines = f.readlines()
  return lines


def main(argv):
  '''
  takes in an argument and processes the file by executing:
  openFileReturnLines() -- to open first argument file
  convertcsv2bitmaporiginal()
  convertbm2bitmapcompress()
  then exits when complete...
  :param argv: requires one argument for the datafile name
  :return: Nothing, assumes program will run first time
  '''
  if (len(sys.argv)!=2):
    print("USAGE: bitmap <datafilename>\n")
    exit()

  lines = openFileReturnLines(argv[1])
  convertcsv2bitmaporiginal(lines,argv[1],".orig.unsorted")
  convertbm2bitmapcompress(argv[1],".orig.unsorted",".unsorted.wah32",32)
  convertbm2bitmapcompress(argv[1],".orig.unsorted",".unsorted.wah64",64)
  lines.sort()
  convertcsv2bitmaporiginal(lines,argv[1],".orig.sorted")
  convertbm2bitmapcompress(argv[1],".orig.sorted",".sorted.wah32",32)
  convertbm2bitmapcompress(argv[1],".orig.sorted",".sorted.wah64",64)
# end main()

if __name__ == "__main__":
  main(sys.argv)