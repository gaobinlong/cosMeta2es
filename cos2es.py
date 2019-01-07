# -*- coding: utf8 -*-
#SCF配置COS触发，从COS获取文件上传信息，并同步meta信息到es中
from qcloud_cos_v5 import CosConfig
from qcloud_cos_v5 import CosS3Client
from qcloud_cos_v5 import CosServiceError
from qcloud_cos_v5 import CosClientError
from elasticsearch import Elasticsearch
import sys
import time
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

appid = 1  # 请替换为您的 APPID
secret_id = u'x'  # 请替换为您的 SecretId
secret_key = u'y'  # 请替换为您的 SecretKey
region = u'ap-guangzhou'  # 请替换为您bucket 所在的地域
token = ''

esEndPoint = '1.1.1.1' # 请替换为您的ES地址

config = CosConfig(Secret_id=secret_id, Secret_key=secret_key, Region=region, Token=token)
client = CosS3Client(config)
logger = logging.getLogger()

def connectES(esEndPoint):
 print ('Connecting to the ES Endpoint {0}'.format(esEndPoint))
 try:
  esClient = Elasticsearch(
   hosts=[{'host': esEndPoint, 'port': 9200}])
  return esClient
 except Exception as E:
  print("Unable to connect to {0}".format(esEndPoint))
  print(E)
  exit(3)

def trans_format(time_string, from_format, to_format='%Y-%m-%d %H:%M:%S'):
    time_struct = time.strptime(time_string, from_format)
    times = time.strftime(to_format, time_struct)
    return times

def indexDocElement(esClient, key, response):
  try:
   objectCreatedDate = response['Last-Modified']
   # 转换时间格式
   objectCreatedDate = trans_format(objectCreatedDate, '%a, %d %b %Y %H:%M:%S GMT')
   objectContentLength = response['Content-Length']
   objectContentType = response['Content-Type']
   etag = response['ETag']
   objectEtag = etag[1:len(etag)-1]
   retval = esClient.index(index='cos-metadata', doc_type='metadata', body={
     'createdDate': objectCreatedDate,
     'objectKey': key,
     'contentType': objectContentType,
     'contentLength': objectContentLength,
     'eTag': objectEtag
   })
  except Exception as E:
    print("Doc not indexed")
    print("Error: ",E)
    exit(5)

def main_handler(event, context):
    logger.info("start main handler")
    esClient = connectES(esEndPoint)
    for record in event['Records']:
        try:
            bucket = record['cos']['cosBucket']['name'] + '-' + str(appid)
            key = record['cos']['cosObject']['key']
            key = key.replace('/' + str(appid) + '/' + record['cos']['cosBucket']['name'] + '/', '', 1)
            logger.info("Bucket: "+bucket+",Key: " + key)

            try:
                response = client.head_object(Bucket=bucket, Key=key,)
                print(response)
                print("key: " + key)
                print("Content-Type: " + response['Content-Type'])
                print("Content-Length: " + response['Content-Length'])
                print("ETag: " + response['ETag'])
                print("Last-Modified: " + response['Last-Modified'])
                indexDocElement(esClient,key,response)
                return "Success"
            except CosServiceError as e:
                print(e.get_error_code())
                print(e.get_error_msg())
                print(e.get_resource_location())
                return "Fail"
            logger.info("Index cos metadata of key [%s] Success" % key)

        except Exception as e:
            print(e)
            print('Error getting object {} from bucket {}. '.format(key, bucket))
            raise e
            return "Fail"

    return "Success"
