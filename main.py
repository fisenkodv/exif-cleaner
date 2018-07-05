#!/usr/bin/python
from __future__ import print_function
import os
import exifread


class GeotagKeywordsCleaner(object):
    def __init__(self, source_photos_path):
        self.source_photos_path = source_photos_path

    def cleanup(self):
        return


if __name__ == '__main__':
    source_photos_path = input('Source path: ') or ''
    if source_photos_path:
        cataloguer = GeotagKeywordsCleaner(source_photos_path)
        cataloguer.cleanup()
    else:
        pass
