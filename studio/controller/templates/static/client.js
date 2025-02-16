// const videoElement = document.getElementById('videoElement');
// const audioElement = document.getElementById('audioElement');
// const client_ip = document.getElementById('client_ip');

// // URL des flux audio et vidéo
// const videoStreamUrl = `http://${client_ip.innerHTML}:5000/camlive/video_feed`;
// const audioStreamUrl = `http://${client_ip.innerHTML}:5000/camlive/audio_feed`;

// // Fonction pour démarrer le flux vidéo
// function startVideoStream() {
//     videoElement.src = videoStreamUrl;
//     videoElement.play().catch(error => {
//         console.error('Erreur lors de la lecture de la vidéo :', error);
//         alert('Erreur lors de la lecture de la vidéo. Veuillez réessayer.');
//     });
// }

// // Fonction pour démarrer le flux audio
// function startAudioStream() {
//     audioElement.src = audioStreamUrl;
//     audioElement.play().catch(error => {
//         console.error('Erreur lors de la lecture de l\'audio :', error);
//         alert('Erreur lors de la lecture de l\'audio. Veuillez réessayer.');
//     });
// }

// // Démarrer les flux vidéo et audio
// startVideoStream();
// startAudioStream();

// // Gestion des erreurs
// videoElement.onerror = (error) => {
//     console.error('Erreur lors du chargement de la vidéo :', error);
//     alert('Erreur lors du chargement de la vidéo. Veuillez réessayer.');
// };

// audioElement.onerror = (error) => {
//     console.error('Erreur lors du chargement de l\'audio :', error);
//     alert('Erreur lors du chargement de l\'audio. Veuillez réessayer.');
// };

document.addEventListener("DOMContentLoaded", function () {
    const client_ip = document.getElementById("client_ip").textContent.trim();

    const videoElement = document.getElementById("videoElement");
    const audioElement = document.getElementById("audioElement");

    // Vérifier si la vidéo et l'audio se chargent bien
    videoElement.onerror = () => {
        console.error("❌ Erreur chargement vidéo.");
        alert("⚠️ Impossible de charger la vidéo.");
    };

    audioElement.onerror = () => {
        console.error("❌ Erreur chargement audio.");
        alert("⚠️ Impossible de charger l'audio.");
    };

    console.log("📡 Flux vidéo lancé sur :", videoElement.src);
    console.log("🎵 Flux audio lancé sur :", audioElement.src);
});