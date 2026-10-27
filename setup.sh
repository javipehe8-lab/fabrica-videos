#!/usr/bin/env bash
# Descarga los modelos de voz (no se guardan en git). Uso: bash setup.sh
set -e
cd "$(dirname "$0")/tts"
[ -f piper/espeak-ng ] || { curl -sL -o piper.tgz https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz && tar xzf piper.tgz && rm piper.tgz; }
chmod +x piper/espeak-ng piper/piper
[ -f kokoro.onnx ] || curl -sL -o kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -f voices.bin ] || curl -sL -o voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
python3.13 -c "import onnxruntime, numpy, scipy, PIL" && echo "setup OK"
