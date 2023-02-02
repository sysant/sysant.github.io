#!/bin/python
#coding:utf-8
# by san at 20220910

import redis
import time
import threadpool
import sys

HOST=127.0.0.1
PASSWD="123456"

r = redis.Redis(host=HOST,password=PASSWD,port=6379,db=0)
def ClearRedisKey(key):
    start_time = time.time()
    if key.isdigit():
        ky = str(key) + ':*'
        print("int key:", ky)
    else:
        ky = key + ':*'
        print("string key:", ky)

    keys = r.keys('%s' % ky)
    pool = threadpool.ThreadPool(20)
    requests = threadpool.makeRequests(r.delete, keys)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    print('%d second'% (time.time()-start_time))
    time.sleep(1)

if __name__ == "__main__":
   if len(sys.argv) <= 1:
       print("exec error!!!!, Like this 'python %s 111111'" % sys.argv[0])
       print("or python %s zk_sssssss" % sys.argv[0])
   else:
       arg = sys.argv[1]
       print("Clear keys is %s" % arg)
       ClearRedisKey(arg)
~                                   
