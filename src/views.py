import base64
import json
import os
import aiohttp
import asyncio
from aiohttp import web
from constants import API_KEY, recursive_to_json
from constants import RecognitionConfigShort, RecognitionAudioShort, RecognizeRequest
from constants import SpeechRecognitionService
from constants import UPLOADS_DIR, CONFIDENT_ENOUGH


async def create_request(b64: str):
    request = RecognizeRequest(
        config=RecognitionConfigShort(
            encoding='FLAC',
            languageCode='ru-RU',
            profanityFilter=True
        ),
        audio=RecognitionAudioShort(
            content=str(b64)
        )
    )
    return recursive_to_json(request)


async def parse_response(response: json):
    text = ''
    for i in range(len(response["results"])):
        if response['results'][i]['alternatives'][0]['confidence'] > CONFIDENT_ENOUGH:
            text += response['results'][i]['alternatives'][0]['transcript']
            return text


async def fetch_text(service, request):
    print('Fetching IP from {}'.format(service.name))

    async with aiohttp.ClientSession() as session:
        async with session.post(service.url.format(service.api_key), json=request) as resp:
            result = await resp.json()
            res_text = await parse_response(result)
            return res_text


async def transcribe(request):
    data = await request.post()
    if not data:
        return web.Response(text='The audio field can not be empty', status=400)

    filename = data['flac'].filename

    file_type = str(filename).split('.')[-1]

    filepath = os.path.join(UPLOADS_DIR, filename)

    if file_type != 'flac':
        return web.Response(text='Only FLAC format is acceptable', status=400)

    input_file = data['flac'].file

    with open(filepath, 'wb') as file:
        content = input_file.read()
        file.write(content)

        data = base64.b64encode(content).decode('ascii')
        r = await create_request(data)

        services = (
            SpeechRecognitionService(name='google-cloud-speech-to-text',
                                     url='https://speech.googleapis.com/v1/speech:recognize?alt=json&key={}',
                                     api_key=API_KEY),
        )

        futures = [fetch_text(service, r) for service in services]

        done, _ = await asyncio.wait(futures)
        for f in done:
            result = f.result()
            return web.Response(content_type='plain/text', text=result)


app = web.Application()
app.add_routes([web.post('/transcribe', transcribe)])
web.run_app(app)
