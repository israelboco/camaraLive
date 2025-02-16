import time
from flask import Flask, Response, request, redirect, render_template, send_from_directory, url_for
import cv2
import os
import signal
import webbrowser
from threading import Thread
from studio.controller.CamController import CamController
from kivymd.utils import asynckivy


class ConnectLiveController:
    app = Flask(__name__, template_folder='templates', static_folder='templates/static')
    CHUNK = 1024
    client_ip = None
    flask_thread = None
    file_path = "index.html"

    def __init__(self, camController: CamController, **kwargs):
        super().__init__(**kwargs)
        self.camController = camController

        @self.app.route('/camlive')
        def home():
            script_path = url_for('static', filename='client.js')
            return render_template(self.file_path, client_ip=request.remote_addr, script_path=script_path)

        @self.app.route('/camlive/audio_feed')
        def audio_feed():
            return Response(self.generate_audio(),
                            mimetype='audio/x-wav')
        
        @self.app.route('/camlive/video_feed')
        def video_feed():
            return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.app.route('/camlive/old-api')
        def old_api():
            return redirect("https://new-domain.com/new-api", code=302)
        
        @self.app.route('/camlive/shutdown', methods=['POST'])
        def shutdown(self):
            self.stop()
            return 'Server shutting down...'

    def serve_static_client_js(self):
        return send_from_directory(os.path.join(self.app.root_path, 'static'), 'client.js')

    def generate_audio(self):
        while self.camController.audioCamera:
            data = self.camController.audioCamera.read(self.CHUNK)
            yield data

    def generate_frames(self):
        max_erreurs = 10
        erreurs = 0

        while True:
            if self.camController.videoCamera is None or not self.camController.videoCamera.isOpened():
                print("📸 Caméra déconnectée, tentative de reconnexion...")
                try:
                    if self.camController.videoCamera is None or not self.camController.videoCamera.isOpened():
                        print("🚨 Impossible de reconnecter la caméra.")
                        return
                except Exception as e:
                    print(f"🚨 Erreur lors de la réouverture de la caméra : {e}")
                    return
            
            success, frame = self.camController.videoCamera.read()
            if not success or frame is None:
                erreurs += 1
                print(f"⚠️ Échec de lecture de la frame ({erreurs}/{max_erreurs}), tentative suivante...")

                if erreurs >= max_erreurs:
                    print("🔄 Trop d'erreurs, tentative de reconnexion...")
                    break  # Arrêter la boucle

                asynckivy.sleep(0.1)
                continue

            # Encodage de l'image en JPEG
            try:
                erreurs = 0  # Réinitialiser le compteur d'erreurs
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    print("⚠️ Erreur d'encodage de l'image.")
                    continue

                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            except Exception as e:
                print(f"🚨 Erreur lors du traitement de l'image : {e}")
                continue


    def local_template(self):
        file_path = self.file_path
        webbrowser.open_new_tab(file_path)

    def start(self):
        try:
            self.flask_thread = Thread(target=self.on_demare)
            self.flask_thread.start()
            # flask_thread.join()
        except Exception as e:
            print(e)
    
    def stop(self):
        try:
            os.kill(os.getpid(), signal.SIGINT)
            self.flask_thread = None
        except Exception as e:
            # self.app = None
            print(e)

    def on_demare(self):
        # if not self.app:
        #     self.app = Flask(__name__, template_folder='templates', static_folder='templates/static')
        self.app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
        self.client_ip = request.remote_addr

# , debug=True