import os
import tempfile
import datetime

import numpy
from pydicom.dataset import  FileDataset, FileMetaDataset


FILENAME_PATH = tempfile.NamedTemporaryFile(suffix='.dcm').name


def create_default_ds():
    ds = create_ds()
    save_ds_file_as_dicom(ds)
    return ds


def create_ds():
    # Populate required values for file meta information
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
    file_meta.MediaStorageSOPInstanceUID = "1.2.3"
    file_meta.ImplementationClassUID = "1.2.3.4"

    # Create the FileDataset instance (initially no data elements, but file_meta
    # supplied)
    ds = FileDataset(FILENAME_PATH, {},
                     file_meta=file_meta, preamble=b"\0" * 128)

    # Add the data elements -- not trying to set all required here. Check DICOM
    # standard
    ds.PatientName = "Test^Firstname"
    ds.PatientID = "123456"

    # Set the transfer syntax
    ds.is_little_endian = True
    ds.is_implicit_VR = True

    # Set image position patient and image orientation patient
    ds.PixelSpacing = ['3.0', '3.0']
    slice_data = numpy.zeros((50, 50)).astype(numpy.uint16)
    ds.ImagePositionPatient = ['-74.87273061275482', '-147.24999237060547', '-147.1303328871727']
    ds.ImageOrientationPatient = ['0.9995653468771569', '0.027916281967051135', '-0.00947620828628687',
                                       '-0.02835352390030065', '0.9983635539946439', '-0.04966177340388578']

    # set the settings for this slice
    ds.Rows = slice_data.shape[1]
    ds.Columns = slice_data.shape[0]

    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = 'MONOCHROME2'
    ds.PlanarConfiguration = 0
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 1
    ds.WindowCenter = 0
    ds.WindowWidth = 100

    # Set creation date/time
    dt = datetime.datetime.now()
    ds.ContentDate = dt.strftime('%Y%m%d')
    timeStr = dt.strftime('%H%M%S.%f')  # long format with micro seconds
    ds.ContentTime = timeStr

    return ds


def save_ds_file_as_dicom(ds):
    ds.save_as(FILENAME_PATH)


def remove_temporary_ds_file():
    if os.path.exists(FILENAME_PATH):
        os.remove(FILENAME_PATH)

