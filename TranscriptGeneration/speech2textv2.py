from google.cloud import speech_v1p1beta1
import io


def speech2text(local_file_path):
    """
    Convert speech to text and identifies different speakers
    ________________________________
    Args: local_file_path Path to local audio file, e.g. /path/audio.wav
    Returns: dictionary of words and speaker
    """

    client = speech_v1p1beta1.SpeechClient()

    # If enabled, each word in the first alternative of each result will be
    # tagged with a speaker tag to identify the speaker.
    enable_speaker_diarization = True

    # Optional. Specifies the estimated number of speakers in the conversation.
    diarization_speaker_count = 2

    # The language of the supplied audio
    language_code = "en-US"
    config = {
        "enable_speaker_diarization": enable_speaker_diarization,
        "diarization_speaker_count": diarization_speaker_count,
        "language_code": language_code,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}
    print("prank")
    operation = client.long_running_recognize(config, audio)
    response = operation.result()

    script = []

    for (idx, result) in enumerate(response.results):
        # Skipping first epoch
        if idx == 0:
            continue
        # First alternative has words tagged with speakers
        # print(result)
        alternative = result.alternatives[0]
        # print(u"Transcript: {}".format(alternative.transcript))
        # Print the speaker_tag of each word
        for word in alternative.words:
            print(u"Word: {}".format(word.word))
            print(u"Speaker tag: {}".format(word.speaker_tag))
            script.append([word.word, word.speaker_tag])

    return script
