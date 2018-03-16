#!/usr/bin/python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: GCS.py
# Author: Carson Wang
# mail: carson.wnag@droi.com
# Created Time: 2018-03-16 15:00:10
#########################################################################

from google.cloud import storage
import os
import os.path
import magic
import argparse

class Storage:
    def __init__(self, project_name, key_file):
        if not (project_name or key_file):
            raise ValueError('Empty key file or project name not allowed.')
        os.environ['GCLOUD_PROJECT'] = project_name
        self.storage_client = storage.Client().from_service_account_json(key_file)

    def uploadFile(self, file_path, dir_name=None, file_name=None, TTL_time=None, MIME=None):
        if not os.path.isfile(file_path) or not file_name:
            return False
        MIME = magic.Magic(mime=True).from_file(file_path) if not MIME else MIME
        cache_control = 'max-age={0}'.format(TTL_time) if TTL_time else 'no-cache'
        self.dir_name = None if file_name.find('index.html') > -1 else dir_name
        self.file_name = file_name
        try:
            self.bucket = self.storage_client.get_bucket('www.ts082.xyz')
            blob_location = dir_name + '/' + file_name
            self.blob = self.bucket.blob(blob_location)
            self.blob.cache_control = 'public, ' + cache_control
            self.blob.upload_from_filename(file_path, content_type=MIME, )
            self.blob.make_public()
        except Exception as e:
            print(e)
            return False
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='python GCS.py', description='Upload file to www.ts082.xyz buckets on google storage.')
    parser.add_argument('-p', '--project', help='what project name on google storage', required=True)
    parser.add_argument('-k', '--key', help='where key file to be placed')
    parser.add_argument('-f', '--file', help='what file to be uploaded', required=True)
    parser.add_argument('-d', '--dir', help='where file to be placed on google storage', required=True)
    parser.add_argument('-n', '--name', help='what file name on google storage', required=True)
    parser.add_argument('-c', '--cache', type=int, help='seconds CDN cache will expire')
    parser.add_argument('-m', '--mime', help='MIME of the file')
    args = parser.parse_args()

    project_name = args.project
    key_file_path = args.key
    file_path = args.file
    dir_name = args.dir
    file_name = args.name
    cache_expire = args.cache
    mime = args.mime

    storage = Storage(project_name, key_file_path)
    print(storage.uploadFile(file_path, dir_name, file_name, cache_expire, mime))
