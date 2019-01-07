# cosMeta2es
使用Serverless云函数把COS对象存储的元信息存储到ES中,同步的元信息字段有：

* Key
* Content-Type
* Content-Length
* ETag
* Last-Modified

## 使用方式
1. clone该源码，在源码目录下执行
```
pip install Elasticsearch -t ./
```
2. 修改cos2es.py源码文件中的账户信息、cos信息、es信息

```
appid = 1  # 请替换为您的 APPID
secret_id = u'x'  # 请替换为您的 SecretId
secret_key = u'y'  # 请替换为您的 SecretKey
region = u'ap-guangzhou'  # 请替换为您bucket 所在的地域
token = ''

esEndPoint = '1.1.1.1' # 请替换为您的ES地址
```
3. 打包源码目录为zip格式，使用腾讯云无服务器云函数(SCF)部署
```
zip cosMeta2es.zip * -r
```
