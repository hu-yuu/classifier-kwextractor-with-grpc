from concurrent import futures
import grpc
import classify_and_extract_pb2, classify_and_extract_pb2_grpc
import tfidfextractor, classifier, preprocessing


class ExtractorNClassifier(classify_and_extract_pb2_grpc.ExtractorAndClassifierServicer):

    def __init__(self):
        self.preprocessor = preprocessing.Preprocessor()
        self.kwExtractor = tfidfextractor.TfIdfExtractor()
        self.txtClassify = classifier.Classifier()

    def Extract(self, request, context):
        text = request.text
        try:
            outboundVars = self._extract(text)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
            return classify_and_extract_pb2.ExtractResponse()

        return classify_and_extract_pb2.ExtractResponse(gramOneKeywords=outboundVars[0], gramTwoKeywords=outboundVars[1])

    def Classify(self, request, context):
        text = request.text
        try:
            outboundVars = self._classify(text)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNKNOWN)
            return classify_and_extract_pb2.ClassifyResponse()         

        return classify_and_extract_pb2.ClassifyResponse(label=outboundVars)

    def _classify(self, text):
            
        if (len(text.split()) < 10):
            raise ValueError("Input text must be longer than 10 words")

        try:
            text = self.preprocessor.process(text)
        except:
            raise Exception("error processing text") 

        try:
            X = self.txtClassify.vectorize(text)
        except:
            raise Exception("error vectorizing text")
                
        try:
            label = self.txtClassify.classify(X)
            return label[0]
                
        except:
            raise Exception("error classifying text")
                
    
        
        
    def _extract(self, text):

        text = self.preprocessor.process(text)

        if (len(text.split()) < 10):
            raise Exception("Input text must be longer than 10 words")
  
        try:
            ngram1 = self.kwExtractor.extract(text, 10, 1)
            ngram2 = self.kwExtractor.extract(text, 10, 2)
            return  ngram1, ngram2
            

        except:
            raise Exception( "error extracting keywords")


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    classify_and_extract_pb2_grpc.add_ExtractorAndClassifierServicer_to_server(ExtractorNClassifier(), server)

    server.add_insecure_port('[::]:9998')
    server.start()
    print('Starting server. Listening on port 9998.')
    server.wait_for_termination()

