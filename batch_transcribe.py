
import argparse
import os
import shutil
import sys
from pathlib import Path
from unittest.mock import patch

import static_ffmpeg
import tqdm
import whisper


AUDIO_EXTENSIONS = {
    ".aac", ".ac3", ".aif", ".aifc", ".aiff", ".amr", ".ape", ".au",
    ".caf", ".flac", ".m4a", ".m4b", ".mka", ".mp2", ".mp3", ".oga",
    ".ogg", ".opus", ".wav", ".wave", ".weba", ".wma",
}


class ProgressBar(tqdm.tqdm):
    """Keep terminal updates on one line and captured output readable."""

    def __init__(self, *args, **kwargs):
        stream = kwargs.setdefault("file", sys.stdout)
        kwargs.update(ascii=True, dynamic_ncols=False)
        kwargs.setdefault("mininterval", 0.5 if stream.isatty() else 5.0)
        kwargs.setdefault("miniters", 1)
        super().__init__(*args, **kwargs)

    @property
    def format_dict(self):
        fields = super().format_dict
        fields["ncols"] = self.line_width(self.fp)
        return fields

    @staticmethod
    def line_width(stream):
        try:
            columns = os.get_terminal_size(stream.fileno()).columns
        except (OSError, ValueError, AttributeError):
            columns = shutil.get_terminal_size(fallback=(80, 24)).columns
        # Leave a column free to prevent automatic wrapping at the right edge.
        return max(1, columns - 1)

    @staticmethod
    def status_printer(stream):
        if stream.isatty():
            last_width = 0

            def redraw(message):
                nonlocal last_width
                message = str(message)
                padding = max(0, min(last_width, ProgressBar.line_width(stream)) - len(message))
                stream.write("\r" + message + " " * padding)
                stream.flush()
                last_width = len(message)

            return redraw

        def write_line(message):
            stream.write(str(message) + "\n")
            stream.flush()

        return write_line


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    parser.add_argument("--model", default="turbo")
    args = parser.parse_args(argv)

    files = sorted(
        p for p in args.folder.rglob("*")
        if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS
    )
    pending = [p for p in files if not p.with_suffix(".txt").exists()]

    print(f"Found {len(files)} recordings, {len(pending)} to transcribe.", flush=True)

    # Whisper imports tqdm separately for downloads and transcription.
    with patch.object(whisper, "tqdm", ProgressBar), patch.object(tqdm, "tqdm", ProgressBar):
        if pending:
            print("Preparing FFmpeg (downloading if needed)...", flush=True)
            try:
                static_ffmpeg.add_paths(weak=True)
            except Exception as e:
                parser.exit(1, f"ERROR: Could not prepare FFmpeg: {e}\n")

            print(f"Loading model {args.model} (downloading if needed)...", flush=True)
            model = whisper.load_model(args.model)

            for i, audio in enumerate(pending, 1):
                print(f"[{i}/{len(pending)}] {audio}", flush=True)

                try:
                    result = model.transcribe(str(audio), verbose=False)
                    audio.with_suffix(".txt").write_text(
                        result["text"].strip(), encoding="utf-8"
                    )
                except Exception as e:
                    print(f"ERROR: {audio}: {e}", flush=True)

    print("Done.", flush=True)


if __name__ == "__main__":
    main()
