import os
import logging
from gtts import gTTS
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip
from backend.config.settings import VIDEO_OUTPUT_PATH, REVIEW_FOLDER

class TTSVideoGenerator:
    def __init__(self, video_output_path=None, review_folder=None):
        self.video_output_path = video_output_path or VIDEO_OUTPUT_PATH
        self.review_folder = review_folder or REVIEW_FOLDER
        os.makedirs(self.video_output_path, exist_ok=True)
        os.makedirs(self.review_folder, exist_ok=True)
        self.logger = logging.getLogger("microtours.tts")

    def script_to_audio(self, script, spot_name):
        try:
            tts = gTTS(text=script, lang='ar')
            audio_path = os.path.join(self.review_folder, f"{spot_name.replace(' ', '_')}.mp3")
            tts.save(audio_path)
            return audio_path
        except Exception as e:
            self.logger.exception("TTS audio generation failed")
            return None

    def images_to_video(self, image_paths, audio_path, spot_name):
        try:
            clips = [ImageClip(img).set_duration(2) for img in image_paths]
            video = concatenate_videoclips(clips, method="compose")
            audio = AudioFileClip(audio_path)
            video = video.set_audio(audio)
            video = video.set_duration(audio.duration)
            output_path = os.path.join(self.video_output_path, f"{spot_name.replace(' ', '_')}.mp4")
            video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
            return output_path
        except Exception as e:
            self.logger.exception("Video generation failed")
            return None

    def generate(self, script, image_paths, spot_name):
        audio_path = self.script_to_audio(script, spot_name)
        if not audio_path:
            return None
        video_path = self.images_to_video(image_paths, audio_path, spot_name)
        return video_path
