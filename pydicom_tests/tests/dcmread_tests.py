import json
import os
import unittest
from pathlib import Path

import matplotlib.pyplot as plt
from pydicom import dcmread, FileDataset
from pydicom.data import get_testdata_file
from pydicom.errors import InvalidDicomError
from pydicom.tag import Tag

from pydicom_tests.utils import ds_creation_util, util
from pydicom_tests.utils.ds_creation_util import FILENAME_PATH


class DcmReadTest(unittest.TestCase):

    def tearDown(self):
        ds_creation_util.remove_temporary_ds_file()

    def test_read_own_dicom_file_validate_default_attributes(self):
        """
            - Writes dicom file from scratch
            - Check attributes
        """
        original_ds = ds_creation_util.create_default_ds()
        ds = dcmread(ds_creation_util.FILENAME_PATH)
        self.assertEqual(original_ds.PatientName, ds.PatientName)
        self.assertEqual(original_ds.PatientID, ds.PatientID)
        self.assertEqual(original_ds.is_little_endian, ds.is_little_endian)
        self.assertEqual(original_ds.is_implicit_VR, ds.is_implicit_VR)
        self.assertEqual(original_ds.ContentDate, ds.ContentDate)
        self.assertEqual(original_ds.ContentTime, ds.ContentTime)
        self.assertEqual(FileDataset, type(ds))

    def test_read_custom_dicom_file_validate_all_attributes(self):
        """
            - Read dicom file downloaded from the web
            - Read dicom file to_json downloaded from the web
            - Check values of the are still being the same
        """
        ttfm_dicom = util.read_file('ttfm.dcm')
        ttfm_json = util.read_json('ttfm.json')
        ds = dcmread(ttfm_dicom)
        ds_json = json.loads(ds.to_json())
        self.assertEqual(FileDataset, type(ds))
        for key in ttfm_json.keys():
            if ds_json[key] is not None:
                self.assertEqual(ttfm_json[key], ds_json[key])

    def test_read_pydicom_data_file_is_FileDataset(self):
        """
            - Read dicom file from pydicom test data files
            - Check is a FileDataSet
        """
        mr_name = get_testdata_file("MR_small.dcm")
        ds = dcmread(mr_name)
        self.assertEqual(FileDataset, type(ds))

    def test_pathlib_path_filename(self):
        """
            - Writes dicom file from scratch
            - Check attributes
            - Check that file can be read using pathlib.Path
        """
        original_ds = ds_creation_util.create_default_ds()
        ds = dcmread(Path(FILENAME_PATH))
        self.assertEqual(original_ds.PatientName, ds.PatientName)
        self.assertEqual(original_ds.PatientID, ds.PatientID)
        self.assertEqual(original_ds.is_little_endian, ds.is_little_endian)
        self.assertEqual(original_ds.is_implicit_VR, ds.is_implicit_VR)
        self.assertEqual(original_ds.ContentDate, ds.ContentDate)
        self.assertEqual(original_ds.ContentTime, ds.ContentTime)
        self.assertEqual(FileDataset, type(ds))

    def test_read_pydicom_data_file_can_be_plot(self):
        """
            - Read dicom file from pydicom test data files
            - Check can be plotted
        """
        mr_name = get_testdata_file("MR_small.dcm")
        ds = dcmread(mr_name)
        try:
            plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
        except:
            self.fail()

    def test_read_own_dicom_file_with_none_attributes(self):
        # FIXME: This test fails, it's correct ds PatientID and PatientName values? Just an empty string instead of None value?
        """
            - Writes dicom file from scratch, with None attributes
            - Check attributes
        """
        original_ds = ds_creation_util.create_ds()
        original_ds.PatientName = None
        original_ds.PatientID = None
        original_ds.ContentDate = '12321312'
        ds_creation_util.save_ds_file_as_dicom(original_ds)
        ds = dcmread(FILENAME_PATH)
        self.assertEqual(original_ds.PatientName, ds.PatientName)
        self.assertEqual(original_ds.PatientID, ds.PatientID)
        self.assertEqual(original_ds.ContentDate, ds.ContentDate)
        self.assertEqual(FileDataset, type(ds))

    def test_read_file_exceptions(self):
        """
            - Try to read, without sending required argument(path to file)
            - Check TypeError Exception is raised
            - Try to read, without sending None as required argument
            - Check AttributeError Exception is raised
            - Try to read, a path that doesn't exists
            - Check FileNotFoundError Exception is raised
        """
        try:
            dcmread()
            self.fail()
        except TypeError:
            pass
        else:
            self.fail()
        try:
            dcmread(None)
            self.fail()
        except AttributeError:
            pass
        else:
            self.fail()
        try:
            dcmread(os.path.abspath('/not_a_file'))
            self.fail()
        except FileNotFoundError:
            pass
        else:
            self.fail()

    def test_defer_size_correct_values(self):
        """
            - Read dicom file from pydicom test data files
            - read with different differ sizes
        """
        try:
            mr_name = get_testdata_file("MR_small.dcm")
            dcmread(mr_name, defer_size='0 KB')
            dcmread(mr_name, defer_size='0.001 KB')
            dcmread(mr_name, defer_size='0.001 GB')
            dcmread(mr_name, defer_size=0)
            dcmread(mr_name, defer_size=12312321321321321321321421342132142132141232132130)
            dcmread(mr_name, defer_size=12312)
            dcmread(mr_name, defer_size=None)
            dcmread(mr_name, defer_size=1516.15615)
        except:
            self.fail()

    def test_defer_size_incorrect_values(self):
        """
            - Read dicom file from pydicom test data files
            - read with different differ sizes
            - Check exceptions are raised
        """
        mr_name = get_testdata_file("MR_small.dcm")
        try:
            dcmread(mr_name, defer_size='asdsadsa$#!@#')
            self.fail()
        except ValueError:
            pass
        except:
            self.fail()
        try:
            dcmread(mr_name, defer_size={})
            self.fail()
        except TypeError:
            pass
        except:
            self.fail()

    def test_stop_before_pixels(self):
        """
            - Read dicom file from pydicom test data files
            - read with stop_before_pixels True and False
            - Check ds with stop True is smaller than ds with stop False
        """
        mr_name = get_testdata_file("MR_small.dcm")
        ds_stop_true = dcmread(mr_name, stop_before_pixels=True)
        ds_stop_false = dcmread(mr_name, stop_before_pixels=False)
        self.assertTrue(len(ds_stop_true) < len(ds_stop_false))

    def test_stop_before_pixels_default_false_value(self):
        """
            - Read dicom file from pydicom test data files
            - read with stop_before_pixels True and default False
            - Check ds with stop True is smaller than ds with stop default False
        """
        mr_name = get_testdata_file("MR_small.dcm")
        ds_stop_true = dcmread(mr_name, stop_before_pixels=True)
        ds_stop_default_false = dcmread(mr_name)
        self.assertTrue(len(ds_stop_true) < len(ds_stop_default_false))

    def test_force_is_false_raise_exception(self):
        """
            - Writes dicom file from scratch without File Meta Information Header
            - read with force = False
            - Check it raises InvalidDicomError Exception
        """
        original_ds = FileDataset(FILENAME_PATH, {}, file_meta=None)
        ds_creation_util.save_ds_file_as_dicom(original_ds)
        try:
            dcmread(FILENAME_PATH, force=False)
            self.fail()
        except InvalidDicomError:
            pass
        except:
            self.fail()

    def test_force_is_default_false_raise_exception(self):
        """
            - Writes dicom file from scratch without File Meta Information Header
            - read with force = False
            - Check it raises InvalidDicomError Exception
        """
        original_ds = FileDataset(FILENAME_PATH, {})
        ds_creation_util.save_ds_file_as_dicom(original_ds)
        try:
            dcmread(FILENAME_PATH)
            self.fail()
        except InvalidDicomError:
            pass
        except:
            self.fail()

    def test_force_is_true(self):
        """
            - Writes dicom file from scratch without File Meta Information Header
            - read with force = True
            - Check it doesn't raise InvalidDicomError Exception
            - Check file_meta has length 0
        """
        original_ds = FileDataset(FILENAME_PATH, {}, file_meta=None)
        ds_creation_util.save_ds_file_as_dicom(original_ds)
        ds = dcmread(FILENAME_PATH, force=True)
        self.assertTrue(len(ds.file_meta) == 0)

    def test_specific_tags(self):
        """
           - Writes dicom file from scratch
           - Read with specific tags
           - Check specific tags are part of ds
           - Check other tags from original are not part from ds
           - Check len(ds) is 3
        """
        ds_creation_util.create_default_ds()
        tags_present = [Tag(0x10, 0x10), Tag(0x20, 0x37), Tag(0x28, 0x06)]
        tags_not_present = [Tag(0x28, 0x11), Tag(0x28, 0x11), Tag(0x28, 0x04)]
        ds = dcmread(ds_creation_util.FILENAME_PATH, specific_tags=tags_present)
        for tag_present in tags_present:
            self.assertIsNotNone(ds[tag_present].value)
        for tag_not_present in tags_not_present:
            self.assertFalse(tag_not_present in ds.keys())
        self.assertEqual(3, len(ds))

    def test_specific_tags_is_empty_cs_tag_is_present(self):
        """
           - Writes dicom file from scratch with tag (0x08, 0x05)
           - Read with specific tags empty list
           - Check tag (0x08, 0x05)
           - Check len(ds) is 1
        """
        original_ds = ds_creation_util.create_ds()
        original_ds.add_new(Tag(0x08, 0x05), 'CS', 'utf8')
        ds_creation_util.save_ds_file_as_dicom(original_ds)
        tags_present = []
        ds = dcmread(ds_creation_util.FILENAME_PATH, specific_tags=tags_present)
        self.assertIsNotNone(ds[0x08, 0x05].value)
        self.assertEqual(1, len(ds))

    def test_read_sending_all_params(self):
        """
           - Writes dicom file from scratch with tag (0x08, 0x05)
           - Read with specific tags empty list
           - Check tag (0x08, 0x05)
           - Check len(ds) is 1
        """
        mr_name = get_testdata_file("MR_small.dcm")
        tags = [Tag(0x08, 0x16), Tag(0x08, 0x30), Tag(0x18, 0x22)]
        ds = dcmread(mr_name, defer_size='2 KB', stop_before_pixels=True, force=True, specific_tags=tags)
        self.assertEqual(FileDataset, type(ds))


if __name__ == '__main__':
    unittest.main()
