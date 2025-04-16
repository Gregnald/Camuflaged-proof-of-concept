document.getElementById("backCam").addEventListener("click", function () {
    startCamera("environment"); // Back camera
});

let videoElement = document.getElementById("webcam");
let zoomLevel = 1.0; // Default zoom level

async function startCamera(facingMode) {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: facingMode,
                zoom: zoomLevel // Initial zoom level
            }
        });

        videoElement.srcObject = stream;
    } catch (err) {
        alert("Camera access denied or not available.");
        console.error("Error accessing webcam:", err);
    }
}

document.getElementById("capture").addEventListener("click", async function () {
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");

    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append("image", blob, "qr_capture.jpg");

        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                console.log("Image saved successfully.");
            } else {
                console.error("Failed to save image.");
            }
        } catch (error) {
            console.error("Error:", error);
        }
    }, "image/jpeg");
});

// Zoom in and zoom out functionality
document.getElementById("zoomIn").addEventListener("click", function () {
    changeZoom(0.1);
});

document.getElementById("zoomOut").addEventListener("click", function () {
    changeZoom(-0.1);
});

function changeZoom(delta) {
    let track = videoElement.srcObject.getVideoTracks()[0];
    let capabilities = track.getCapabilities();
    
    if ('zoom' in capabilities) {
        zoomLevel = Math.min(Math.max(zoomLevel + delta, capabilities.zoom.min), capabilities.zoom.max);
        track.applyConstraints({ advanced: [{ zoom: zoomLevel }] });
    }
}
