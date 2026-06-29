<div align="center">

# Transcriptor de Audio

**Transcripción de voz a texto, 100 % local y privada.**

Convierte notas de voz, clases o reuniones en texto sin que tu audio salga nunca de tu computadora.

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![faster-whisper](https://img.shields.io/badge/engine-faster--whisper-FF6F00)](https://github.com/SYSTRAN/faster-whisper)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-blue)]()

</div>

---

## Contenido

- [¿Por qué?](#por-qué)
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Modelos](#modelos)
- [Cómo funciona](#cómo-funciona)
- [Rendimiento](#rendimiento)
- [Solución de problemas](#solución-de-problemas)
- [Créditos](#créditos)
- [Licencia](#licencia)

---

## ¿Por qué?

La mayoría de servicios de transcripción suben tu audio a la nube. Esta herramienta hace
todo **en tu propia máquina** con el modelo [Whisper](https://github.com/openai/whisper)
de OpenAI, a través de la implementación optimizada
[faster-whisper](https://github.com/SYSTRAN/faster-whisper):

- No hay servidores, ni cuentas, ni límites de uso.
- Tu audio y tus transcripciones **nunca salen de tu equipo**.
- Funciona sin conexión una vez descargado el modelo.

---

## Características

| | |
|---|---|
| **Privado** | Procesamiento 100 % local y offline. |
| **Multi-idioma** | Optimizado para español; admite cualquier idioma o autodetección. |
| **Multi-formato** | `ogg`, `mp3`, `m4a`, `wav`, `opus`, `flac`, `aac`, `wma`, `mp4`, `mkv`, `webm`. |
| **Modelos a elegir** | Desde `tiny` (veloz) hasta `large-v3` (máxima precisión). |
| **Salida flexible** | Texto corrido o con marcas de tiempo, guardado junto al audio. |
| **Por lotes** | Transcribe varios audios en una sola ejecución. |
| **Sin dependencias externas** | No requiere instalar `ffmpeg` (incluye su propio decodificador). |

---

## Instalación

```bash
git clone https://github.com/OtazuGIT/TranscriptorAudio.git
cd TranscriptorAudio
pip install -r requirements.txt
```

> **Requisitos:** Python 3.9 o superior (probado en 3.14).

---

## Uso

```bash
python transcribe.py "nota.ogg"
```

Esto genera `nota.txt` junto al audio. Algunos ejemplos más:

```bash
# Elegir el modelo
python transcribe.py "nota.ogg" --small        # rápido
python transcribe.py "nota.ogg" --medium       # preciso (por defecto)
python transcribe.py "clase.m4a" --large       # máxima precisión

# Transcribir varios audios de una vez
python transcribe.py "a.ogg" "b.mp3" "c.m4a" --medium

# Incluir marcas de tiempo en el archivo de salida
python transcribe.py "reunion.ogg" --timestamps

# Detectar el idioma automáticamente
python transcribe.py "audio.ogg" --lang auto
```

### Opciones

| Bandera | Descripción |
|---|---|
| `--tiny` / `--base` / `--small` / `--medium` / `--large` | Tamaño del modelo (por defecto `--medium`). |
| `--model NOMBRE` | Especifica un modelo manualmente. |
| `--lang CÓDIGO` | Idioma (`es` por defecto; usa `auto` para detectar). |
| `--timestamps`, `-t` | Guarda la transcripción con marcas de tiempo. |
| `--help` | Muestra la ayuda completa. |

**Sugerencia:** en lugar de escribir la ruta del audio, arrástralo a la ventana de la terminal
y la ruta se pega sola.

---

## Modelos

| Modelo | Descarga | Velocidad (CPU) | Precisión | Recomendado para |
|---|---|---|---|---|
| `tiny`     | ~75 MB  | Muy alta | Baja | Pruebas rápidas |
| `base`     | ~145 MB | Alta | Media | Borradores |
| `small`    | ~480 MB | Media | Buena | Audios largos |
| `medium`   | ~1.5 GB | Baja | Muy buena | **Notas de voz (por defecto)** |
| `large-v3` | ~3 GB   | Muy baja | Máxima | Términos técnicos / nombres difíciles |

Los modelos se descargan **una sola vez** y quedan cacheados para uso sin conexión.

---

## Cómo funciona

```
Audio --> Espectrograma Mel --> Encoder --> Decoder --> Texto
            (representación        (resume      (genera el
             del sonido)           el audio)    texto palabra
                                                a palabra)
```

1. El audio se decodifica y se remuestrea a 16 kHz.
2. Se convierte en un **espectrograma Mel** (una representación visual del sonido).
3. Un detector de actividad de voz (**VAD**) descarta los silencios.
4. El **encoder** resume el audio y el **decoder** genera el texto, prediciendo
   cada palabra según el audio y el contexto previo.

---

## Rendimiento

Tiempo de procesamiento aproximado en **CPU** con el modelo `medium`:

| Duración del audio | Tiempo estimado |
|---|---|
| 1 minuto  | ~1 min |
| 10 minutos | ~10-15 min |
| 1 hora    | ~1-1.5 h |

Para audios largos, usar `--small` reduce el tiempo a la mitad o menos.
Con una GPU NVIDIA (CUDA) el proceso es varias veces más rápido.

---

## Solución de problemas

<details>
<summary><b>La transcripción tiene errores en nombres propios o términos técnicos</b></summary>

Sube de modelo (`--large`) o revisa manualmente. Whisper "interpreta" el audio,
así que con vocabulario muy específico puede equivocarse.
</details>

<details>
<summary><b>Aparece texto inventado en silencios o música</b></summary>

El filtro VAD ya está activado para mitigarlo. Si persiste, prueba con audio de mejor calidad.
Las canciones con música de fondo son un caso difícil para el modelo.
</details>

<details>
<summary><b>La primera ejecución tarda mucho</b></summary>

La primera vez se **descarga el modelo** (hasta ~3 GB en `large`). Las siguientes
ejecuciones ya no descargan nada.
</details>

---

## Créditos

- Modelo: [Whisper](https://github.com/openai/whisper) (OpenAI)
- Motor: [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (SYSTRAN)
- Código generado con [Claude Code](https://claude.com/claude-code) (Anthropic)

---

## Licencia

MIT — ver [LICENSE](LICENSE).
