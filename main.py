#!/usr/bin/python
from __future__ import print_function
import os
import os.path
import exifread
from libxmp import XMPFiles, consts


class GeotagKeywordsCleaner(object):
    def __init__(self, source_photos_path):
        self.source_photos_path = source_photos_path

    def cleanup(self):
        files = self.get_files(self.source_photos_path, ['jpg', 'jpeg'])
        for file_path in files:
            print('Reading %s' % file_path)
            self.get_tags_from_xmp(file_path)
        return

    def get_tags_from_xmp(self, file_path):
        xmpfile = XMPFiles(file_path=file_path, open_forupdate=True)
        xmp = xmpfile.get_xmp()
        property_was_removed = False
        for index in range(5, 0, -1):
            property_was_removed |= self.remove_geo_xmp_property(
                xmp, consts.XMP_NS_DC, 'subject[%s]' % (index))
        if property_was_removed:
            print('Updating %s' % file_path)
            xmpfile.put_xmp(xmp)
        xmpfile.close_file()
        return

    def remove_geo_xmp_property(self, xmp, ns, property_name):
        if xmp is not None and xmp.does_property_exist(ns, property_name):
            property = xmp.get_property(ns, property_name)
            if isinstance(property, basestring) and property.find('geo') != -1:
                xmp.delete_property(ns, property_name)
                return True
        return False

    def get_files(self, target_dir, extension=['*']):
        item_list = os.listdir(target_dir)

        file_list = list()
        for item in item_list:
            item_dir = os.path.join(target_dir, item)
            if os.path.isdir(item_dir):
                file_list += self.get_files(item_dir, extension)
            else:
                if '*' in extension or self.get_file_extension(item_dir) in extension and self.is_ascii(item_dir):
                    file_list.append(item_dir)
        return file_list

    def get_file_extension(self, path):
        return os.path.splitext(path)[1][1:].strip()

    def is_ascii(self, s):
        return all(ord(c) < 128 for c in s)


if __name__ == '__main__':
    source_photos_path = input('Source path: ')
    if source_photos_path:
        cataloguer = GeotagKeywordsCleaner(source_photos_path)
        cataloguer.cleanup()
    else:
        pass
