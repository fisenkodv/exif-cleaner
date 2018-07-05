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
            tags = self.get_tags(file_path)
        return

    def get_tags(self, file_path):
        tags = exifread.process_file(open(file_path, 'rb'))
        xmpfile = XMPFiles(file_path=file_path, open_forupdate=False)
        # for tag in tags.keys():
        #     print("Key: %s, value %s" % (tag, tags[tag]))
        return tags

    def get_files(self, target_dir, extension = ['*']):
        item_list = os.listdir(target_dir)

        file_list = list()
        for item in item_list:
            item_dir = os.path.join(target_dir, item)
            if os.path.isdir(item_dir):
                file_list += self.get_files(item_dir, extension)
            else:
                if '*' in extension or self.get_file_extension(item_dir) in extension:
                    file_list.append(item_dir)
        return file_list

    def get_file_extension(self, path):
        return os.path.splitext(path)[1][1:].strip()


if __name__ == '__main__':
    source_photos_path = 'D://Temp//exif//'#input('Source path: ') or 'D://documents//'
    if source_photos_path:
        cataloguer = GeotagKeywordsCleaner(source_photos_path)
        cataloguer.cleanup()
    else:
        pass
