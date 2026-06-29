import sys
import os
import argparse

# Forzar UTF-8 en consola de Windows para mostrar tildes/ñ correctamente
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from faster_whisper import WhisperModel

AUDIO_EXTS = {".ogg", ".mp3", ".m4a", ".wav", ".opus", ".flac", ".aac", ".wma", ".mp4", ".mkv", ".webm"}


def transcribe_file(model, path, model_size, lang, with_timestamps):
    name = os.path.basename(path)
    print("\n" + "=" * 70)
    print(f"Transcribiendo: {name}")
    print("=" * 70, flush=True)

    segments, info = model.transcribe(path, language=lang, beam_size=5, vad_filter=True)
    print(f"[idioma {info.language} · {info.duration:.0f}s · modelo {model_size}]\n", flush=True)

    plain, stamped = [], []
    for seg in segments:
        txt = seg.text.strip()
        print(f"[{seg.start:6.1f} -> {seg.end:6.1f}]  {txt}", flush=True)
        plain.append(txt)
        stamped.append(f"[{seg.start:6.1f} -> {seg.end:6.1f}]  {txt}")

    out = os.path.splitext(path)[0] + ".txt"
    body = "\n".join(stamped) if with_timestamps else " ".join(plain).strip()
    with open(out, "w", encoding="utf-8") as f:
        f.write(body + "\n")
    print(f"\n>> Guardado: {out}", flush=True)


def main():
    p = argparse.ArgumentParser(
        description="Transcribe audios a texto (offline, faster-whisper).",
        epilog="Ejemplos:\n"
               "  py transcribe.py nota.ogg\n"
               "  py transcribe.py nota.ogg --medium\n"
               "  py transcribe.py a.ogg b.mp3 --small\n"
               "  py transcribe.py clase.m4a --large --timestamps\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("archivos", nargs="+", help="Uno o varios archivos de audio")
    # Banderas de modelo (atajos)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--tiny", action="store_const", const="tiny", dest="model", help="Modelo mas rapido, menos preciso")
    g.add_argument("--base", action="store_const", const="base", dest="model")
    g.add_argument("--small", action="store_const", const="small", dest="model", help="Rapido, buena calidad")
    g.add_argument("--medium", action="store_const", const="medium", dest="model", help="Preciso (por defecto)")
    g.add_argument("--large", action="store_const", const="large-v3", dest="model", help="Maxima precision, mas lento")
    g.add_argument("--model", dest="model", help="Nombre de modelo manual")

    p.add_argument("--lang", "--idioma", default="es", help="Idioma (def: es). Usa 'auto' para detectar")
    p.add_argument("--timestamps", "-t", action="store_true", help="Guardar el .txt con marcas de tiempo")
    args = p.parse_args()

    model_size = args.model or "medium"
    lang = None if args.lang == "auto" else args.lang

    archivos = [a for a in args.archivos if os.path.isfile(a) and os.path.splitext(a)[1].lower() in AUDIO_EXTS]
    faltan = [a for a in args.archivos if a not in archivos]
    for a in faltan:
        print(f"!! Ignorado (no existe o formato no soportado): {a}")
    if not archivos:
        print("No hay audios validos. Formatos: " + ", ".join(sorted(AUDIO_EXTS)))
        sys.exit(1)

    print(f"Cargando modelo '{model_size}' (la primera vez se descarga)...", flush=True)
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    for path in archivos:
        try:
            transcribe_file(model, path, model_size, lang, args.timestamps)
        except Exception as e:
            print(f"!! Error con {path}: {e}", flush=True)

    print("\nListo. Cada audio tiene su .txt al lado.")


if __name__ == "__main__":
    main()
