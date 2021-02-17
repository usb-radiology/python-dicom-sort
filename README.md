# python-dicom-sort
Script to sort DICOM files according to their tags. With a CLI and a GUI.

## Installation

Install it using pip:

`pip install -e .`

If you want to ensure the availability of the GUI, this will also install the optional PySide2 dependency:

`pip install -e .[GUI]`

##  Usage

Call `dicom_sort` (or `python dicom_sort`) without arguments to open the GUI (if PySide2 is available).

Otherwise you can use it as a command line tool with the following syntax:
```
usage: dicom_sort [-h] [--copy] src dest pattern

Move DICOM files into a directory structure

positional arguments:
  src         Origin directory with unsorted files
  dest        Destination directory with sorted files
  pattern     Directory pattern (example: %PatientName%/%StudyDate%/%SeriesNumber%_%SeriesName%)

optional arguments:
  -h, --help  show this help message and exit
  --copy, -c  Copy files instead of moving
```

The program will move (or copy) the dicom files from the `src` folder to the `dest` folder, creating an appropriate directory structure as specified by `pattern`. The dicom files themselves will be renamed into `imageXXXX.dcm` where `XXXX` is replaced by the instance number.

## License

This program is copyrighted by Francesco Santini (2021) and released under the MIT license. See the LICENSE file for details.