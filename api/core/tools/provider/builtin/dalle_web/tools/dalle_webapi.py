import logging
from typing import Any, Union

import requests

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

logger = logging.getLogger(__name__)

default_base_url = 'http://10.252.25.214:8000/v1'


class DalleWebApiTool(BuiltinTool):

    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) \
            -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:

        base_url = self.runtime.credentials.get('api_base_url', default_base_url)
        params = {}

        prompt = tool_parameters.get('prompt', '')
        if not prompt:
            return self.create_text_message('Please input prompt')
        else:
            params['prompt'] = prompt

        style = tool_parameters.get('style', None)
        if style:
            params['style'] = style

        size = tool_parameters.get('size', None)
        if size:
            params['size'] = size

        n = tool_parameters.get('n', '')
        if n:
            params['n'] = int(n)

        is_async = tool_parameters.get('async', '')
        if is_async:
            params['async'] = self._str_to_bool(is_async)

        notify_url = tool_parameters.get('notifyUrl', None)
        if notify_url:
            params['notifyUrl'] = notify_url

        image = tool_parameters.get('image', '')
        if not image:
            url = f"{base_url}/images/generations"
            response = requests.post(url=url, json=params)
        else:
            url = f"{base_url}/images/variations"
            image_bytes = open(image, 'rb')
            image_file = {'image': image_bytes}
            response = requests.post(url=url, data=params, files=image_file)

        if 200 <= response.status_code < 300:
            response_json = response.json()
            return [
                self.create_text_message(text="images generated"),
                self.create_json_message(response_json),
            ]

        return self.create_text_message(text="Image generation failed")

    @staticmethod
    def _str_to_bool(s: str) -> bool:
        return s.lower() in ("yes", "y", "true", "t", "1")
