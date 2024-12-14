# README GPT GENERATED PLEASE UPDATE IT

## Overview

This project is a Flask-based application that includes functionality for a basic web interface and transcription of videos into text. It uses OpenAI's Whisper model for transcription and OpenAI's API for summarizing the transcribed text.

---

## Features

1. **Flask Web App**:
   - A homepage (`index.html`) is served at `/`.
   - A `/prompt` endpoint accepts POST requests with a prompt message and returns the same message as a JSON response.

2. **Video Transcription**:
   - Extracts audio from a video file using `ffmpeg`.
   - Transcribes the extracted audio into text using OpenAI's Whisper model.
   - Saves the transcription in a text file (`transcription.txt`).

3. **Summarization**:
   - Summarizes the transcribed text using OpenAI's GPT-3 API.
   - The function takes the transcription file as input and returns a concise summary.

---

## Requirements

Install the necessary dependencies:

```bash
pip install flask openai git+https://github.com/openai/whisper.git ffmpeg-python
```

Make sure `ffmpeg` is installed on your system. For Ubuntu, you can install it with:

```bash
apt-get update && apt-get install ffmpeg -y
```

---

## Setup

1. **Environment Variables**:
   - Set your OpenAI API key in an environment variable:
     ```bash
     export OPENAI_API_KEY="your_api_key"
     ```

2. **Run the Flask App**:
   - Start the server:
     ```bash
     python app.py
     ```
   - Access the app at `http://127.0.0.1:5000/`.

3. **Transcription and Summarization**:
   - Call the `transcribe_video(video_path, language, model_name)` function to transcribe a video.
   - Use the `compterendu(filename, api_key)` function to summarize the transcription.

---

## Usage

1. **Transcription**:
   - Provide a video file path to `transcribe_video()`.
   - The audio will be extracted, transcribed, and saved to `transcription.txt`.

2. **Summarization**:
   - Call `compterendu("transcription.txt", api_key)` with the transcription file to get a summary.

---

## Example

```python
# Transcribe a video
transcribe_video("example_video.mp4")

# Summarize the transcription
summary = compterendu("transcription.txt", os.environ.get("OPENAI_API_KEY"))
print(summary)
```

---

## Notes

- **Security**: Avoid hardcoding your OpenAI API key. Use environment variables or secure storage.
- **Customization**: Adjust the `language` and `model_name` parameters in `transcribe_video()` and the `max_tokens` or `temperature` in `compterendu()` as needed.

--- 

## License

This project is licensed under the [MIT License](LICENSE).
