import os
import threading
import time
import subprocess
import shutil
from datetime import datetime
from studio.view.AudioRecorder import AudioRecorder
from studio.view.VideoRecorder import VideoRecorder


class Camera:

    def __int__(self, lien=None):
        self.lien = lien
        self.video_thread = None
        self.filename = None
        self.filename_video = None
        self.filename_audio = None
        self.filename_video_2 = None
        self.filename_video_final = None

    def afficheCamara(self, lien):
        print(lien)
        if len(lien) == 1:
            self.lien = int(lien)
            lien = int(lien)
        else:
            self.lien = lien
            lien = lien + "/video"
        self.filename = datetime.now().strftime("%A_%d_%B_%Y_%I_%M_%S")
        self.filename_video = "{}.mp4".format(self.filename)
        self.filename_audio = "{}".format(self.filename)
        return self.start_AVrecording(lien, self.filename_video)

    def start_AVrecording(self, lien, filename):
        global video_thread
        global audio_thread
        self.filename = filename
        video_thread = VideoRecorder(lien, filename)
        try:
            int(self.lien)
            audio_thread = AudioRecorder(self.filename_audio, self.lien)
        except:
            audio_thread = AudioRecorder(self.filename_audio)
        return video_thread.demarage(lien, filename)

    def record_demarage(self, frames_to_record):
        if video_thread is not None:
            print("record_demarage True")
            video_thread.record_demarage(frames_to_record)
            audio_thread.start()

    def enregistrer(self, frames_to_record):
        if video_thread is not None:
            print("video_thread stop")
            video_frame = video_thread.stop_record(frames_to_record)
            self.stop()
            return video_frame

    def update_enregistrer(self, frames_to_record):
        if video_thread is not None:
            print("video_thread update")
            return video_thread.update_record(frames_to_record)

    def stop(self):
        video_thread.stop()
        audio_thread.stop()
        # self.stop_enregistrement()

    def stop_enregistrement(self):
        local_path = os.getcwd()
        audio_thread.stop()
        frame_counts = video_thread.frame_counts
        elapsed_time = time.time() - video_thread.start_time
        recorded_fps = frame_counts / elapsed_time
        print("total frames " + str(frame_counts))
        print("elapsed time " + str(elapsed_time))
        print("recorded fps " + str(recorded_fps))
        video_thread.stop()
        try:
            self.filename_video_final = str(local_path) + "/enregistrement/final_" + self.filename_video
            self.filename_audio = str(local_path) + "/enregistrement/output_{}.wav".format(self.filename_audio)
            out_audio = shutil.copy(self.filename_audio, str(os.getcwd()) + "/temp_audio.wav")
            print(out_audio)
            out_video = shutil.copy(str(local_path) + "/enregistrement/" + self.filename_video, str(os.getcwd()) + "/temp_video.mp4")
            print(out_video)

            # Makes sure the threads have finished
            while threading.active_count() > 1:
                time.sleep(1)

            #    Merging audio and video signal
            print(str(abs(recorded_fps - 6)))
            if abs(recorded_fps - 6) >= 0.01:  # If the fps rate was higher/lower than expected, re-encode it to the expected

                print("Re-encoding")
                cmd = "ffmpeg -r " + str(recorded_fps) + " -i temp_video.mp4 -pix_fmt yuv420p -r 6 temp_video2.mp4"
                subprocess.call(cmd, shell=True)

                print("Muxing")
                cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video2.mp4 -pix_fmt yuv420p filename.mp4"
                subprocess.call(cmd, shell=True)

            else:

                print("Normal recording\nMuxing")
                cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video.mp4 -pix_fmt yuv420p filename.mp4"
                subprocess.call(cmd, shell=True)

                print("..")

            self.file_manager(self.filename)

        except Exception as e:
            print(str(e))

    # Required and wanted processing of final files
    def file_manager(self, filename):

        local_path = os.getcwd()

        if os.path.exists(str(local_path) + "/temp_audio.wav"):
            os.remove(str(local_path) + "/temp_audio.wav")

        if os.path.exists(str(local_path) + "/temp_video.mp4"):
            os.remove(str(local_path) + "/temp_video.mp4")

        if os.path.exists(str(local_path) + "/temp_video2.mp4"):
            os.remove(str(local_path) + "/temp_video2.mp4")

        if os.path.exists(str(local_path) + "/filename.mp4"):
            out_video = shutil.copy(str(os.getcwd()) + "/filename.mp4", self.filename_video_final)
            print(out_video)
            os.remove(str(local_path) + "/filename.mp4")
