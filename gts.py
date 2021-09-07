import os
import hashlib
from google.cloud import texttospeech_v1beta1 as texttospeech

#jsonファイルへのpath
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "google-credentials.json"
DEFAULT_LANGUAGE_CODE = "ja-JP"

class GoogleCloudSpeak:
    """GoogleText-to-Speechを使用するためのクラス。

    使用法：
        cloudttsからGoogleCloudSpeakをインポートします
        GoogleCloudSpeak.speak（text、language_code = "ja-JP"）
    """

    @classmethod
    def __synthesize(cls, input_text, language_code, name):
        client = texttospeech.TextToSpeechClient()
        # 音声の名前はclient.list_voices（）で取得できます。
        voice = texttospeech.types.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL,
            name=name,
        )

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16
        )

        return client.synthesize_speech(
            input_=input_text, voice=voice, audio_config=audio_config
        )

    @classmethod
    def synthesize_text(cls, text, language_code=DEFAULT_LANGUAGE_CODE, name=None):
        """テキストの入力文字列から音声を合成します。"""
        input_text = texttospeech.types.SynthesisInput(text=text)
        response = cls.__synthesize(input_text, language_code, name)

        return response.audio_content


    # @classmethod
    # def speak(cls, text, language_code=DEFAULT_LANGUAGE_CODE, name=None):
    #     """テキストメッセージを話します。"""
    #     audio_content = cls.synthesize_text(text, language_code, name)
    #     SoundPlayer.play_from_buffer(audio_content, stop=True)

class CachedSpeak:
    """音声キャッシュモジュール。

    GoogleText-to-Speechから取得した音声データを保存および再生するクラス。
    音声データを./audio_cache/にキャッシュして再利用してます。
    """

    @classmethod
    def synthesize(cls, text, language_code=DEFAULT_LANGUAGE_CODE, name=None):
        """SSML check and Synctesize."""
        if text.startswith("<speak>") and text.endswith("</speak>"):
            return GoogleCloudSpeak.synthesize_ssml(
                text, language_code=language_code, name=name
            )
        return GoogleCloudSpeak.synthesize_text(
            text, language_code=language_code, name=name
        )

    @classmethod
    def speak(cls,
        text,
        wait=True,
        stop=True,
        language_code=DEFAULT_LANGUAGE_CODE,
        name=None,
        replace=False,
    ):
        """Cache speak."""
        dir_path = "./audio_cache/"
        text_hash = hashlib.sha224(text.encode("utf-8")).hexdigest()
        file_name = dir_path + text_hash + ".wav"
        list_name = dir_path + "cached.txt"

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if not os.path.exists(file_name) or replace:
            with open(file_name, mode="wb") as f_p:
                audio = cls.synthesize(text, language_code=language_code, name=name)
                f_p.write(audio)
                with open(list_name, mode="a") as log_f_p:
                    log_f_p.write("\n{}, {}".format(text, text_hash + ".wav"))
        return file_name