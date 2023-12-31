import requests
import base64
import json
import time
from pydub import AudioSegment

subscriptionKey = "eaa8a25a9d104972a4d873832b931932" # replace this with your subscription key
# subscriptionKey = 'ca0e5b14-5d77-41f6-9194-594cf0719f19'
region = "eastus" # replace this with the region corresponding to your subscription key, e.g. westus, eastasia

# a common wave header, with zero audio length
# since stream data doesn't contain header, but the API requires header to fetch format information, so you need post this header as first chunk for each query
WaveHeader16K16BitMono = bytes([ 82, 73, 70, 70, 78, 128, 0, 0, 87, 65, 86, 69, 102, 109, 116, 32, 18, 0, 0, 0, 1, 0, 1, 0, 128, 62, 0, 0, 0, 125, 0, 0, 2, 0, 16, 0, 0, 0, 100, 97, 116, 97, 0, 0, 0, 0 ])

# a generator which reads audio data chunk by chunk
# the audio_source can be any audio input stream which provides read() method, e.g. audio file, microphone, memory stream, etc.
def get_chunk(audio_source, chunk_size=1024):
  yield WaveHeader16K16BitMono
  while True:
    time.sleep(chunk_size / 32000) # to simulate human speaking rate
    chunk = audio_source.read(chunk_size)
    if not chunk:
      global uploadFinishTime
      uploadFinishTime = time.time()
      break
    yield chunk


def get_final_answer(referenceText, audioData):
    # build pronunciation assessment parameters
    pronAssessmentParamsJson = "{\"ReferenceText\":\"%s\",\"GradingSystem\":\"HundredMark\",\"Dimension\":\"Comprehensive\"}" % referenceText
    pronAssessmentParamsBase64 = base64.b64encode(bytes(pronAssessmentParamsJson, 'utf-8'))
    pronAssessmentParams = str(pronAssessmentParamsBase64, "utf-8")

    # build request
    url = "https://%s.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-us" % region
    headers = { 'Accept': 'application/json;text/xml',
                'Connection': 'Keep-Alive',
                'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
                'Ocp-Apim-Subscription-Key': subscriptionKey,
                'Pronunciation-Assessment': pronAssessmentParams,
                'Transfer-Encoding': 'chunked',
                'Expect': '100-continue' }

    # audioFile = open('check.m4a', 'rb')
    x = AudioSegment.from_file(audioData)
    x.export("check.wav", format='wav')    # maybe use original resolution to make smaller

    # send request with chunked data
    response = requests.post(url=url, data=get_chunk(open("check.wav","rb")), headers=headers)
    # getResponseTime = time.time()
    # audioFile.close()

    resultJson = json.loads(response.text)
    return resultJson
# print(json.dumps(resultJson, indent=4))

# latency = getResponseTime - uploadFinishTime
# print("Latency = %sms" % int(latency * 1000))