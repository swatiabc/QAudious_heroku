from __future__ import absolute_import, unicode_literals
from uuid import uuid4
from punctuator import Punctuator
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from django.utils import timezone
import os
from . import models

def process_uploaded_file(audio_data_id):
    """
    Call all other processing methods from this method
    """
    print("555555555555555")
    # Get Audio data model
    audio_data = None
    audio_data = models.AudioDataModel.objects.get(id=audio_data_id)
    print("66666666666666")
    # Convert uploaded file into WAV format
    convert_into_wave(audio_data)
    print("77777777777777777777")
    # Extract the Transcript from WAV file
    # transcribe_audio(audio_data)
    get_large_audio_transcription(audio_data)


def convert_into_wave(audio_data):
    """
    Converts the uploaded file into WAV, suitable for Speech Recognition
    """

    uploaded_file_name = audio_data.uploaded_file.name
    file_extension = uploaded_file_name.split('.')[-1].lower()
    exported_file_name = audio = None

    # Convert into WAV format
    if file_extension != 'wav':
        print("-----------------------", uploaded_file_name, file_extension)
        audio = AudioSegment.from_mp3(uploaded_file_name)
        print("mp3--------------------------------")
        # Generate a unique name and then export as WAV
        exported_file_name = f'{str(uuid4())}.wav'
        audio.export(exported_file_name, format='wav')

    # Already a WAV file
    else:
        exported_file_name = uploaded_file_name

    # Now save the exported file name
    audio_data.exported_file_name = exported_file_name
    audio_data.save()

    return


def transcribe_audio(audio_data):
    """
    Extract transcript from WAV file
    """
    print(audio_data,"--------------",type(audio_data) )
    exported_file_name = audio_data.exported_file_name
    audio = transcript = None

    recognizer = sr.Recognizer()

    with sr.AudioFile(exported_file_name) as ef:
        audio = recognizer.record(ef)
        transcript = recognizer.recognize_google(audio)

    # Save the transcript in the database
    audio_data.transcript = transcript
    audio_data.status = 'COM'
    audio_data.time_taken = timezone.now() - audio_data.created_at
    print(timezone.now() - audio_data.created_at)
    audio_data.save()

    return

def get_large_audio_transcription(audio_data):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    print("8888888888888888888")
    print(audio_data,"------------------",type(audio_data))
    r = sr.Recognizer()
    exported_file_name = audio_data.exported_file_name
    # open the audio file using pydub
    sound = AudioSegment.from_wav(exported_file_name)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    print("999999999999999999999")
    chunks = split_on_silence(sound,
                              # experiment with this value for your target audio file
                              min_silence_len=1000,
                              # adjust this per requirement
                              silence_thresh=sound.dBFS - 16,
                              # keep the silence for 1 second, adjustable as well
                              # keep_silence=500,
                              )
    print("aaaaaaaaaaaaaaaa")
    target_length = 60*1000
    output_chunks = [chunks[0]]
    for chunk in chunks[1:]:
        if len(output_chunks[-1]) < target_length:
            output_chunks[-1] += chunk
        else:
            # if the last output chunk is longer than the target length,
            # we can start a new one
            output_chunks.append(chunk)
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(output_chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected

    p = Punctuator('Demo-Europarl-EN.pcl')
    text = p.punctuate(whole_text)
    print(text)

    # Save the transcript in the database
    audio_data.transcript = text
    audio_data.status = 'COM'
    audio_data.time_taken = timezone.now() - audio_data.created_at
    print(timezone.now() - audio_data.created_at)
    audio_data.save()
    return whole_text
