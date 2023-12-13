import streamlit as st
from audio_recorder_streamlit import audio_recorder

from google.cloud import speech
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from google.api_core.client_options import ClientOptions

region = 'asia-southeast1'
model = 'chirp'
# model = 'default'
project_id = 'mitochondrion-project-344303'

st.title('Konnyaku Penerjemah')

language_list = ['id-ID', 'en-US', 'zh-CN', 'ja-JP', 'ar-EG', ]
origin_language = st.sidebar.selectbox('Select Origin Language', language_list)
destination_language = st.sidebar.selectbox('Select Destination Language', language_list)


def stt_v1(content, language):
    """Transcribe the given audio file."""
    client = speech.SpeechClient()

    # with open(speech_file, "rb") as audio_file:
    #     content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        # encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=16000,
        language_code=language,
        audio_channel_count = 2,
    )

    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response


def transcribe_chirp(
    audio_file,
    language
):
    """Transcribe an audio file using Chirp."""
    # Instantiates a client
    client = SpeechClient(
        client_options=ClientOptions(
            api_endpoint=f"{region}-speech.googleapis.com",
        )
    )

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[language],
        model=model
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/{region}/recognizers/_",
        config=config,
        content=audio_file,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return response

from vertexai.preview.language_models import TextGenerationModel

llm = TextGenerationModel.from_pretrained('text-bison')

audio_bytes = audio_recorder(pause_threshold=2.0, sample_rate=41_000)
if audio_bytes:

    st.write('Running transcription')

    # response = transcribe_chirp(audio_bytes, origin_language)
    response = stt_v1(audio_bytes, origin_language)
    text = response.results[0].alternatives[0].transcript

    st.text_area('Transcription Result', text)

    prompt = """
    Translate this sentence from {} to {} as accurate as possible while maintaining the tone and style

    Input: {}
    Output:
    """.format(origin_language, destination_language, text)

    resp = llm.predict(prompt, temperature=0)

    st.text_area('Translation Result', resp.text)
