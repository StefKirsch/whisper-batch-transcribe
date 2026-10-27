# Audio Transcription in Batch

Transcribe recordings locally with Whisper. Each recording gets a `.txt` file beside it. Subfolders are included. Recordings with an existing `.txt` file are treated as already transcribed and are skipped.

## Setup

Download this repository (**Code → Download ZIP**, then extract it), or clone it.

Open a terminal and follow the steps below. On Windows we recommend Windows Powershell that should already be in the list of installed programs on your computer.

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) by pasting the respective code in the terminal and confirming with `Enter`:

   **Windows (PowerShell):**

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   **macOS / Linux:**

   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Close and reopen your terminal after installing uv.

2. Open the repository folder in your terminal (`cd "path/to/repo"`), then run:

   ```sh
   uv sync --locked
   ```

   uv downloads Python 3.13 if needed and installs the locked dependencies in
   `.venv`. No environment activation is needed.

## Transcribe

From the repository folder, run the command below to transcribe all audio files in the folder and its subfolders:

```sh
uv run batch_transcribe.py .
```

The default model is `turbo`. To choose another model:

```sh
uv run batch_transcribe.py --model small .
```

Supported audio extensions: `.aac`, `.ac3`, `.aif`, `.aifc`, `.aiff`, `.amr`,
`.ape`, `.au`, `.caf`, `.flac`, `.m4a`, `.m4b`, `.mka`, `.mp2`, `.mp3`, `.oga`,
`.ogg`, `.opus`, `.wav`, `.wave`, `.weba`, and `.wma`. Uppercase extensions are
also accepted.

FFmpeg is set up automatically using [static-ffmpeg](https://pypi.org/project/static-ffmpeg/),
the same dependency used by [transcribetools](https://github.com/ndegroot/transcribetools).
An existing FFmpeg/FFprobe installation is reused; otherwise, the binaries are
downloaded on the first run with recordings to transcribe and reused on later runs.
No separate FFmpeg installation or administrator access is needed. This works
directly from the GitHub download or clone; this project does not need to be on PyPI.

The first run needs internet to download FFmpeg (if needed) and the model.
Transcription runs locally and can take a while. Run
`uv run batch_transcribe.py --help` for options.
