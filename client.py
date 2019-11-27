import grpc

import test_pb2
import test_pb2_grpc

# открываем канал и создаем клиент
channel = grpc.insecure_channel('localhost:6066')
stub = test_pb2_grpc.DataStub(channel)

# запрос за md5
# data = input()
to_ = test_pb2.data(adr="dsf", params={"asfa": "asfaf", "ghrh": "dfhdh"})
res = stub.gen(to_)
print(res.data, res.res)
channel.close()
#print(res.res)
