# Transcriptor de Audio 🎙️

Transcribe audios a texto **100% en local** (offline) usando [faster-whisper](https://github.com/SYSTRAN/faster-whisper).
Pensado para notas de voz de WhatsApp, clases, reuniones, etc. Tu audio nunca sale de tu PC.

## Características

- 🔒 **Privado y offline** — todo se procesa en tu máquina.
- 🗣️ Optimizado para **español** (configurable a cualquier idioma o autodetección).
- 📦 Soporta `ogg, mp3, m4a, wav, opus, flac, aac, wma, mp4, mkv, webm`.
- ⚡ Varios tamaños de modelo (`tiny` → `large-v3`) según velocidad/precisión.
- 📝 Genera un `.txt` junto a cada audio (texto corrido o con marcas de tiempo).
- 🎯 Procesa **varios audios** en una sola ejecución.

## Requisitos

- Python 3.9+ (probado en 3.14)
- `pip install faster-whisper`

No necesitas instalar `ffmpeg` por separado: `faster-whisper` trae su propio decodificador de audio (PyAV).

## Instalación

```bash
git clone https://github.com/<tu-usuario>/transcriptor-audio.git
cd transcriptor-audio
pip install -r requirements.txt
```

## Uso

```bash
# Básico (modelo medium por defecto)
python transcribe.py "nota.ogg"

# Elegir modelo
python transcribe.py "nota.ogg" --small      # rápido
python transcribe.py "nota.ogg" --medium     # preciso (defecto)
python transcribe.py "clase.m4a" --large     # máxima precisión

# Varios audios a la vez
python transcribe.py "a.ogg" "b.mp3" --medium

# Con marcas de tiempo en el .txt
python transcribe.py "audio.ogg" --timestamps

# Detectar idioma automáticamente
python transcribe.py "audio.ogg" --lang auto

# Ayuda
python transcribe.py --help
```

> En Windows, con el lanzador `Transcribir.bat` también puedes **arrastrar y soltar** los audios encima.

## Modelos disponibles

| Modelo | Descarga | Velocidad (CPU) | Precisión |
|---|---|---|---|
| `tiny`     | ~75 MB  | muy rápida | baja |
| `base`     | ~145 MB | rápida     | media |
| `small`    | ~480 MB | media      | buena |
| `medium`   | ~1.5 GB | lenta      | muy buena |
| `large-v3` | ~3 GB   | muy lenta  | máxima |

Los modelos se descargan una sola vez y quedan cacheados para uso offline.

## Notas

- En CPU, el tiempo de proceso ronda **1–1.5×** la duración del audio con `medium`.
- Con audios ruidosos o términos muy técnicos puede haber errores; subir de modelo ayuda.

## Licencia

MIT
