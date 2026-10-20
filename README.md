# Transcribe interviews

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

2. Install [FFmpeg](https://ffmpeg.org/download.html) by pasting the respective code below in your terminal:

   - Windows:

      ```powershell
      winget install --id Gyan.FFmpeg --exact`
      ```

   - macOS (with [Homebrew](https://brew.sh)):

      ```sh
      brew install ffmpeg
      ```

   *Reopen* your terminal, then check that `ffmpeg -version` works.

3. Open the repository folder in your terminal (`cd "path/to/repo"`), then run:

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

The first run downloads the model and needs internet. Transcription runs locally and can take a while. Run `uv run batch_transcribe.py --help` for options.
