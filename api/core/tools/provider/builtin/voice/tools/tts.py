import hashlib
import logging
import os
from typing import Any, Union

import requests

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

logger = logging.getLogger(__name__)

default_base_url = 'http://10.252.25.251:9880/tts'
default_sotrage_root = '/nas/dify/audio'


# noinspection PyTypeChecker
class TtsTool(BuiltinTool):

    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) \
            -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:

        base_url = self.runtime.credentials.get('tts_base_url', default_base_url)
        data = {}

        input_text = tool_parameters.get('text', '')
        if not input_text:
            return self.create_text_message('Please input text')
        else:
            data['text'] = input_text

        speech_rate = tool_parameters.get('speech_rate', None)
        if speech_rate:
            data['speech_rate'] = float(speech_rate)

        target_duration = tool_parameters.get('target_duration', None)
        if target_duration:
            data['target_duration'] = float(target_duration)

        response = requests.post(url=base_url, json=data)
        if 200 <= response.status_code < 300:
            content_type = response.headers['Content-Type']
            extension = content_type.split("/")[1]
            raw_bytes = response.content
            hash_str = hashlib.sha1(input_text.encode("utf-8")).hexdigest()
            audio_dir = self.runtime.credentials.get('sotrage_root', default_sotrage_root)
            audio_file = f"{audio_dir}/{hash_str}.{extension}"
            os.makedirs(f"{audio_dir}", exist_ok=True)
            with open(audio_file, "wb") as f:
                f.write(raw_bytes)

            url_prefix = self.runtime.credentials.get('output_url_prefix')
            output_url = f"{url_prefix}/{hash_str}.{extension}"

            return [
                self.create_text_message(text="audio file generated"),
                self.create_json_message({"audio_file": output_url}),
                self.create_blob_message(blob=raw_bytes, meta={"mime_type": content_type}, save_as="audio"),
            ]

        return self.create_text_message(text="Synthesis failed")
