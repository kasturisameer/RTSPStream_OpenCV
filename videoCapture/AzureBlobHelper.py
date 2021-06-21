import os, uuid, sys
from io import BytesIO
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from azure.identity import ClientSecretCredential
import logging

class AzureBlobHelper:
    def __init__(self):
        self.account_name = ""
        self.tenant_id = ""
        self.client_id = ""
        self.client_secret = ""
        credential = ClientSecretCredential(self.tenant_id, self.client_id, self.client_secret)
        self.service_client = DataLakeServiceClient.from_connection_string("")
        #  DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format("https", self.account_name), credential=credential)

    def _getFileUriParts(self, path):
        secondSlashPosition = path.find('/', 1)
        return path[1: secondSlashPosition], path[secondSlashPosition: len(path)]


    def read_file(self, path: str):
        file_system, file_path = self._getFileUriParts(path)
        file_client = self.service_client.get_file_client(file_system, file_path)
        file = file_client.download_file()
        stream = BytesIO()
        length = file.readinto(stream)
        return stream

    def upload_file(self, path:str, stream):
        file_system, file_path = self._getFileUriParts(path)
        file_client = self.service_client.get_file_client(file_system, file_path)
        if file_client.exists():
            file_client.delete_file()
        file_client.create_file()
        if str == type(stream):
            file_client.upload_data(data=stream, length=stream.getbuffer().nbytes, overwrite=True)
            return
        stream.seek(0)
        file_client.upload_data(data=stream.read(), length=stream.getbuffer().nbytes, overwrite=True)
    
    def get_file_properties(self, path):
        file_system, file_path = self._getFileUriParts(path)
        file_client = self.service_client.get_file_client(file_system, file_path)
        return file_client.get_file_properties()
    
    def move_file(self, source, target):
        file_system, file_path = self._getFileUriParts(source)
        file_client = self.service_client.get_file_client(file_system, file_path)
        file_client.rename(target)