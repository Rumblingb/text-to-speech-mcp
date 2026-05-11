# Text-to-Speech MCP Server

![Status](https://img.shields.io/badge/status-active-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

A Model Context Protocol (MCP) server that provides text-to-speech capabilities using [edge-tts](https://github.com/rany2/edge-tts) — Microsoft Edge's free TTS engine. No API key required, no usage limits.

## Features

- **No API key needed** — leverages Microsoft Edge's free TTS
- **50+ voices** across multiple languages and accents
- **Adjustable speed** — slow down or speed up speech
- **Two output modes** — base64 audio for in-chat use, or direct file save
- **MP3 output** — universally compatible audio format

## Tools

### 1. `text_to_speech`

Convert text to speech and return base64-encoded MP3 audio.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | Yes | — | Text to convert to speech |
| `voice` | string | No | `en-US-JennyNeural` | Voice to use (see `list_voices`) |
| `speed` | number | No | `1.0` | Speaking speed multiplier (0.5–2.0) |

**Returns:** Base64-encoded MP3 audio data.

### 2. `list_voices`

List all available TTS voices.

**Parameters:** None

**Returns:** Formatted list of all available voices.

### 3. `text_to_speech_file`

Convert text to speech and save the MP3 file to disk.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | Yes | — | Text to convert to speech |
| `output_path` | string | Yes | — | Absolute path to save the MP3 file |
| `voice` | string | No | `en-US-JennyNeural` | Voice to use (see `list_voices`) |

**Returns:** File path confirmation with byte size.

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd text-to-speech-mcp

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
python server.py
```

### MCP Client Configuration

For Claude Desktop or any MCP-compatible client, add to your MCP configuration:

```json
{
  "mcpServers": {
    "text-to-speech": {
      "command": "python",
      "args": ["/path/to/text-to-speech-mcp/server.py"]
    }
  }
}
```

## Available Voices

The server includes 50+ voices across multiple languages and regional variants:

**English (US):** JennyNeural, GuyNeural, AriaNeural, DavisNeural, JaneNeural, JasonNeural, NancyNeural, SaraNeural, TonyNeural

**English (UK):** SoniaNeural, RyanNeural, LibbyNeural, MaisieNeural

**English (AU):** NatashaNeural, WilliamNeural

**English (CA):** ClaraNeural, LiamNeural

**English (IN):** NeerjaNeural, PrabhatNeural

**Other Languages:** Chinese, French, German, Japanese, Korean, Portuguese, Spanish (ES & MX), and more.

Use `list_voices` in your MCP client to see the full list.

## Example Usage (with MCP client)

```
User: Say "Hello, world!" in a British voice

Assistant: [calls text_to_speech(text="Hello, world!", voice="en-GB-SoniaNeural")]
Returns: [base64 MP3 audio]

User: List the available voices

Assistant: [calls list_voices()]
Returns: Formatted list of 50+ voices

User: Save "This is a test" to /tmp/test.mp3

Assistant: [calls text_to_speech_file(text="This is a test", output_path="/tmp/test.mp3")]
Returns: Audio saved to /tmp/test.mp3 (14230 bytes, MP3)
```

## Deployment

### Smithery

This server is configured for deployment on [Smithery](https://smithery.ai/). See `smithery.yaml` for configuration.

### Pricing

**$19/month** for hosted deployment via Smithery.

[Subscribe here](https://buy.stripe.com/dRm6oJ4Hd2Jugek0wz1oI0m)

## License

MIT
