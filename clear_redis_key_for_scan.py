#coding:utf-8
import redis
import time
import sys
import os
from threading import Thread, current_thread

# CQC,PRE 
# PRE:2001

# 开启进程数
t = 4
# 连接密码
Password='PASSWORD'
# redis 主机
Host='127.0.0.1'
# 默认端口6379
Port=6379
# 默认DB 0
DB=0

r = redis.Redis(host=Host,password=Password,port=Port,db=DB)
# 获取运行中服务器key列表,通过ansible获取运行中的服务器id（后面清key要排除）
def RunKeys():
    try:
        run_key = os.popen("ansible projects -m shell -a 'cd /data/infra/scripts;./project status'|grep project_|awk '{print $3}'")
        keys = run_key.read().split('\n')
        print("Running Games keys:",keys)
        return keys
    except:
        print("Some servers were closing...,Don't accept clear redis keys!!!!!")
        return 0
    finally:
        run_key.close()

def RedisScan(key_prx,host='127.0.0.1',port=6379,db=0,password=None):
    begin_pos,counts,var,delete_key = 0,0,0,0
    key_prxs = key_prx + ':*'
    #redis_cache = redis.Redis(host=host,port=port,db=db,password=password,decode_responses=True)    # decode_responses参数会导致报 UnicodeDecodeError:'utf8' codec can't decode 错误
    redis_cache = redis.Redis(host=host,port=port,db=db,password=password)
    while True:
        begin_pos,list_keys = redis_cache.scan(begin_pos,key_prxs,5000)
        counts += len(list_keys)
        for key in list_keys:
            num = redis_cache.ttl(key)
            if num == -1:
                redis_cache.delete(key)
                delete_key = delete_key + 1
            else:
                var = var + 1
        if begin_pos == 0:
            break

    print("total key is:", counts)
    print("delete key is", delete_key)
    print("no delete kye is", var)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        sys.exit("Error!!!!, Like this 'python %s 111111'" % sys.argv[0])
    else:
        keys = RunKeys()
        if  keys == 0 or 'stopped' in keys:
            sys.exit("Error!!!!,现在有部分服处��关机维护状态,不允许执行清数据!!!!!!!")
        arg = sys.argv[1]
        if arg in keys:
            sys.exit("Error!!!!,禁止输入的key是正在运行中的服务器数据库!!!!!!!")
        else:
            print("Clear keys is %s:*" % arg)

    try:
        r.ping()
    except:
        print("Redis connect failed.No password?")
    else:
        RedisScan(arg,host=Host,port=Port,password=Password,db=DB)
