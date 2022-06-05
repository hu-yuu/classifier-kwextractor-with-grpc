from urllib import response
import grpc
from requests import request
import classify_and_extract_pb2, classify_and_extract_pb2_grpc


channel = grpc.insecure_channel('localhost:9998')

stub = classify_and_extract_pb2_grpc.ExtractorAndClassifierStub(channel)

request = classify_and_extract_pb2.Request(text="İdare mahkemesinde açmış olduğumuz hukuki el atma nedeniyle kamulaştırmasız el atma davasında bilirkişi raporu düzenlendi. Rapora itiraz etmeyeceğiz , dava konusu miktarı ıslah edeceğiz ancak dosyanın yeniden bilirkişiye gidip gitmeyeceğini konusunda emin olamıyoruz. Islahı ne zaman yapmalıyım , bu konu da yardımcı olursanız sevinirim.")

response = stub.Classify(request)
print(response)

#response is:
#label: "labelkamu"
