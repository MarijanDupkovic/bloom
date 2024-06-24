import asyncio
import subprocess
from channels.generic.websocket import AsyncWebsocketConsumer

class FileStreamConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ffmpeg_process = subprocess.Popen(
            ['ffmpeg', '-i', '-', '-f', 'mp4', 'output.mp4'],
            stdin=subprocess.PIPE
        )

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        self.ffmpeg_process.stdin.close()
        self.ffmpeg_process.wait()

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            self.ffmpeg_process.stdin.write(bytes_data)