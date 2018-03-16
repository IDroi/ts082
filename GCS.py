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

class Storage:
    def __init__(self, project_name, key_file):
        if not (project_name or key_file):
            raise ValueError('Empty key file or project name not allowed.')
        os.environ['GCLOUD_PROJECT'] = project_name
        self.storage_client = storage.Client().from_service_account_json(key_file)

    def getBlobs(self, bucket_name, prefix=None):
        try:
            self.bucket = self.storage_client.get_bucket(bucket_name)
        except Exception as e:
            print(e)
            return None
        return self.bucket.list_blobs(prefix=prefix)

    def uploadFile(self, file_path, dir_name=None, file_name=None, TTL_time=None, MIME=None):
        if not os.path.isfile(file_path) or not file_name:
            return False
        MIME = magic.Magic(mime=True).from_file(file_path) if not MIME else MIME
        cache_control = 'max-age={0}'.format(TTL_time) if TTL_time else 'no-cache'
        self.dir_name = None if file_name.find('index.html') > -1 else dir_name
        self.file_name = file_name
        try:
            self.bucket = self.storage_client.get_bucket('infohub')
            blob_location = file_name if file_name.find('index.html') > -1 else dir_name + '/' + file_name
            self.blob = self.bucket.blob(blob_location)
            self.blob.cache_control = 'public, ' + cache_control
            self.blob.upload_from_filename(file_path, content_type=MIME, )
            self.blob.make_public()
        except Exception as e:
            print(e)
            return False
        return True

    def getUrl(self):
        try:
            return '/'.join(filter(None.__ne__, ['http://www.infohubapp.com', self.dir_name, self.file_name]))
        except:
            return None
