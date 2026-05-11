"""
Text-to-Speech MCP Server
Uses edge-tts (Microsoft Edge's free TTS, no API key required).

Tools:
  - text_to_speech(text, voice?, speed?) -> base64 MP3 audio
  - list_voices() -> available voices
  - text_to_speech_file(text, output_path, voice?) -> save to file
"""

import asyncio
import base64
import os

import edge_tts
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
)

DEFAULT_VOICE = "en-US-JennyNeural"
AVAILABLE_VOICES = [
    "en-US-JennyNeural",
    "en-US-GuyNeural",
    "en-US-AriaNeural",
    "en-US-DavisNeural",
    "en-US-JaneNeural",
    "en-US-JasonNeural",
    "en-US-NancyNeural",
    "en-US-SaraNeural",
    "en-US-TonyNeural",
    "en-GB-SoniaNeural",
    "en-GB-RyanNeural",
    "en-GB-LibbyNeural",
    "en-GB-MaisieNeural",
    "en-AU-NatashaNeural",
    "en-AU-WilliamNeural",
    "en-CA-ClaraNeural",
    "en-CA-LiamNeural",
    "en-IN-NeerjaNeural",
    "en-IN-PrabhatNeural",
    "en-IE-EmilyNeural",
    "en-IE-ConnorNeural",
    "en-SG-LunaNeural",
    "en-SG-WayneNeural",
    "en-ZA-LukeNeural",
    "en-ZA-SamNeural",
    "en-KE-AsiliaNeural",
    "en-KE-ChilembaNeural",
    "en-NG-EzinneNeural",
    "en-NG-AbeoNeural",
    "en-TZ-ImaniNeural",
    "en-TZ-ElimuNeural",
    "en-PH-RosaNeural",
    "en-PH-JamesNeural",
    "zh-CN-XiaoxiaoNeural",
    "zh-CN-YunxiNeural",
    "zh-CN-YunjianNeural",
    "zh-CN-XiaoyiNeural",
    "zh-CN-YunyangNeural",
    "fr-FR-DeniseNeural",
    "fr-FR-HenriNeural",
    "fr-FR-EloiseNeural",
    "de-DE-KatjaNeural",
    "de-DE-ConradNeural",
    "de-DE-AmalaNeural",
    "de-DE-BerndNeural",
    "ja-JP-NanamiNeural",
    "ja-JP-KeitaNeural",
    "ko-KR-SunHiNeural",
    "ko-KR-InJoonNeural",
    "pt-BR-FranciscaNeural",
    "pt-BR-AntonioNeural",
    "es-ES-AlvaroNeural",
    "es-ES-ElviraNeural",
    "es-MX-JorgeNeural",
    "es-MX-DaliaNeural",
]


async def _synthesize(text: str, voice: str, speed: float) -> bytes:
    """Run edge-tts and return raw MP3 bytes."""
    rate_str = f"+{int((speed - 1.0) * 100)}%" if speed >= 1.0 else f"-{int((1.0 - speed) * 100)}%"
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate_str)
    audio_chunks = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])
    return b"".join(audio_chunks)


app = Server("text-to-speech")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="text_to_speech",
            description="Convert text to speech and return base64-encoded MP3 audio. Use 'list_voices' first to see available voices.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to convert to speech",
                    },
                    "voice": {
                        "type": "string",
                        "description": "Voice to use (e.g., en-US-JennyNeural, en-GB-SoniaNeural). Default: en-US-JennyNeural",
                        "default": DEFAULT_VOICE,
                    },
                    "speed": {
                        "type": "number",
                        "description": "Speaking speed multiplier. 1.0 = normal, 0.5 = half speed, 2.0 = double speed",
                        "default": 1.0,
                    },
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="list_voices",
            description="List all available TTS voices.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="text_to_speech_file",
            description="Convert text to speech and save the MP3 file to disk. Returns the file path.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to convert to speech",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Absolute path where the MP3 file should be saved (e.g., /tmp/output.mp3)",
                    },
                    "voice": {
                        "type": "string",
                        "description": "Voice to use (e.g., en-US-JennyNeural, en-GB-SoniaNeural). Default: en-US-JennyNeural",
                        "default": DEFAULT_VOICE,
                    },
                },
                "required": ["text", "output_path"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "list_voices":
        voices_info = "\n".join(
            f"  {i+1}. {v}" for i, v in enumerate(AVAILABLE_VOICES)
        )
        return [
            TextContent(
                type="text",
                text=f"Available voices ({len(AVAILABLE_VOICES)}):\n{voices_info}\n\nTip: Use a voice like 'en-US-JennyNeural' with text_to_speech or text_to_speech_file.",
            )
        ]

    if name == "text_to_speech":
        text = arguments["text"]
        voice = arguments.get("voice", DEFAULT_VOICE)
        speed = arguments.get("speed", 1.0)

        audio_bytes = await _synthesize(text, voice, speed)
        b64 = base64.b64encode(audio_bytes).decode("utf-8")

        return [
            TextContent(
                type="text",
                text=f"Audio generated ({len(audio_bytes)} bytes, MP3).\nBase64:\n{b64}",
            )
        ]

    if name == "text_to_speech_file":
        text = arguments["text"]
        output_path = arguments["output_path"]
        voice = arguments.get("voice", DEFAULT_VOICE)

        audio_bytes = await _synthesize(text, voice, 1.0)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

        return [
            TextContent(
                type="text",
                text=f"Audio saved to {os.path.abspath(output_path)} ({len(audio_bytes)} bytes, MP3).",
            )
        ]

    raise ValueError(f"Unknown tool: {name}")


async def main() -> None:
    from mcp import stdio_server

    async with stdio_server() as (read, write):
        await app.run(
            read,
            write,
            InitializationOptions(
                server_name="text-to-speech",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
