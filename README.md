![WSU Vancouver](WSUV.png)

# WAHbitmap
## CS482 - Assignment 2 - WSU Vancouver
### WAH Bitmap Indexes
### About
This  assignment  primarily  dealt  with  Bitmap  Indexes  from  a  table  whose  fields  consists  of  an  **Animal  Type,
Animal  Age**  and  **Animal  Adopted.**   The  Type  and  Adopted  field  was  converted  to  a  grey  code,  while  the  Age
field  was  converted  in  groups  of  10  via  binning.
The data output was not binary,  instead our assignment required us to output as the character one and zero
*(ie.  ‘1’ and ‘0’ respectively)* aiding in debugging visually.  With minor changes to the bitmap code, it can be a true
bitmap.  Our bitmap data was aligned to optimize compression along the table’s columns.  In the case of our schema,
the uncompressed bitmap was comprised of 16 lines of text with the column width of the file equal to the number of
entries in the table.

### Requirements
Python 3

### Executing
*animals.txt and animals_test.txt are the datafiles that can be processed*
```sh
    ./bitmap.py animals.txt
```
or
```sh
    python3 bitmap.py animals_test.txt
```
### Notes
*Code Cleanup, added documents, and added files* - June 13, 2018
