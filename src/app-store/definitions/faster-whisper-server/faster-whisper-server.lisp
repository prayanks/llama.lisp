(define-app
    (version ,(choose-version "faster-whisper-server" "0.5.0-cuda"))
    (ports 8000)
    (url "https://github.com/fedirz/faster-whisper-server")
    (containers
        (container
            (name "server")
            (image ,(format "docker.io/fedirz/faster-whisper-server:{}" ,(choose-version "faster-whisper-server" "0.5.0-cuda")))
            (volumes
                ("models" "/root/.cache/huggingface"))
            (additional-flags "--device nvidia.com/gpu=all"))))
