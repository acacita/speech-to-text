import os
from constants import API_KEY, recursive_to_json, RecognitionConfigShort, RecognitionAudioShort, RecognizeRequest, UPLOADS_DIR, CONFIDENT_ENOUGH
import json
import base64
import aiohttp
from aiohttp import web


async def create_request(b64: str):
    request = RecognizeRequest(
        config=RecognitionConfigShort(
            encoding='FLAC',
            languageCode='ru-RU',
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


async def store_mp3_view(request):
    data = await request.post()
    if not data:
        return web.Response(text='please send audio')

    filename = data['flac'].filename

    file_type = str(filename).split('.')[-1]

    filepath = os.path.join(UPLOADS_DIR, filename)

    if file_type != 'flac':
        return web.Response(text='please send flac only')

    input_file = data['flac'].file

    with open(filepath, 'wb') as file:
        content = input_file.read()
        file.write(content)

        data = base64.b64encode(content).decode('ascii')
        r = await create_request(data)

        # with open(filepath, 'w+') as f:
        #     f.write(str(r))

        async with aiohttp.ClientSession() as session:
            async with session.post('https://speech.googleapis.com/v1/speech:recognize?alt=json&key={}'.format(API_KEY),
                                    json=r) as resp:
                all_res = await resp.json()
                print(all_res)
                result = await parse_response(all_res)
                print(result)
                return web.Response(content_type='plain/text', text=str(result))


app = web.Application()
app.add_routes([web.post('/store_mp3', store_mp3_view)])
web.run_app(app)
