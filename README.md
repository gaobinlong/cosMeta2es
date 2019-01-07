# cosMeta2es
使用Serverless云函数把COS对象存储的元信息存储到ES中

## 使用方式
1. clone该源码，在源码目录下执行
pip install Elasticsearch -t ./
2. 打包源码目录为zip格式，使用腾讯云无服务器云函数(SCF)部署
zip cosMeta2es.zip * -r
