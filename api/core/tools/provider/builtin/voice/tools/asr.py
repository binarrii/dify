import logging
from typing import Any, Union

import requests

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

logger = logging.getLogger(__name__)

default_base_url = 'http://10.252.25.251:9880/stt'


class AsrTool(BuiltinTool):

    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) \
            -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:

        base_url = self.runtime.credentials.get('asr_base_url', default_base_url)
        wav_file = tool_parameters.get('wav_file', '')
        if not wav_file:
            return self.create_text_message('Please provide audio file')

        audio_bytes = open(wav_file, 'rb')
        files = {'wav_file': audio_bytes}
        response = requests.post(url=base_url, files=files)
        if 200 <= response.status_code < 300:
            resp_json = response.json()
            return [
                self.create_text_message(text="speech recognized"),
                self.create_json_message(resp_json),
            ]

        return self.create_text_message(text="recognition failed")
