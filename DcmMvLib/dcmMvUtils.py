# -*- coding: utf-8 -*-

#  Copyright (c) 2021 Francesco Santini <francesco.santini@gmail.com>

import os
import re
import shutil
import pydicom
from pathvalidate import sanitize_filepath

UNKNOWN_TAG = 'UNKNOWN'
DEBUG = False
DRY_RUN = False

def safe_int(s):
    try:
        return int(s)
    except ValueError:
        return 0

def get_dicom_attribute(dataset, attribute):
    try:
        return str(getattr(dataset, attribute))
    except:
        return UNKNOWN_TAG

def pattern_translate(dataset, attribute):
    if attribute == 'SeriesID':
        return get_dicom_attribute(dataset, 'SeriesInstanceUID')
    if attribute == 'SeriesName':
        return get_dicom_attribute(dataset, 'SeriesDescription')
    if attribute == 'PatientName':
        res = get_dicom_attribute(dataset, 'PatientName')
        if res == UNKNOWN_TAG:
            return get_dicom_attribute(dataset, 'PatientsName')
    if attribute == 'InstanceNumber':
        return safe_int(get_dicom_attribute(dataset, 'InstanceNumber'))
    if attribute == 'CoilInfo':
        try:
            return str(dataset[0x0051, 0x100F]) # Siemens private field
        except:
            return UNKNOWN_TAG
    if attribute == 'SeriesNumber':
        return get_dicom_attribute(dataset, attribute).rjust(2,'0')
    return get_dicom_attribute(dataset, attribute)


def move_dicom_image(filename_in, destination_base_dir, pattern, copy=False):
    try:
        dataset = pydicom.dcmread(filename_in)
    except:
        if DEBUG:
            print(f'Not a dicom file: {filename_in}')
        return
    while m := re.search(r'%([A-Za-z]+)%', pattern):
        found_key = m.group(1)
        replacement = pattern_translate(dataset, m.group(1))
        pattern = pattern.replace(f'%{found_key}%', replacement)

    dest_directory = sanitize_filepath(os.path.join(destination_base_dir, pattern), platform='auto')

    if not DRY_RUN:
        os.makedirs(dest_directory, exist_ok=True)

    instance_number = pattern_translate(dataset, 'InstanceNumber')
    coil_info = pattern_translate(dataset, 'CoilInfo')

    extra_file_part = ''
    if len(coil_info) == 3: # only one coil, with a 3-letter ID: this is probably part of a "save uncombined dataset"
        extra_file_part = f'_{coil_info}'

    dest_name = f'image{instance_number:04d}{extra_file_part}.dcm'

    dest_path = sanitize_filepath(os.path.join(destination_base_dir, pattern, dest_name), platform='auto')

    if DEBUG:
        print(f'{filename_in} -> {dest_path}')

    if not DRY_RUN:
        if copy:
            shutil.copy2(filename_in, dest_path)
        else:
            shutil.move(filename_in, dest_path)


def move_directory(dir_in, destination_base_dir, pattern, copy=False, callback_function=None):
    file_list = []
    for root, dirs, files in os.walk(dir_in):
        file_list.extend([os.path.join(root, f) for f in files])
    n_files = len(file_list)
    for index, file in enumerate(file_list):
        move_dicom_image(file, destination_base_dir, pattern, copy)
        try:
            callback_function(index+1, n_files)
        except:
            pass
