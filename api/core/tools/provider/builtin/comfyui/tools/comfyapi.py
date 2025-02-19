import logging
import time
from typing import Any, Union

import requests
from requests import RequestException

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool

logger = logging.getLogger(__name__)

default_base_url = 'http://10.252.25.251:8080'


class ComfyApiTool(BuiltinTool):

    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) \
            -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:

        base_url = self.runtime.credentials.get('api_base_url', default_base_url)
        params = {}

        workflow = tool_parameters.get('workflow', '')
        if not workflow:
            return self.create_text_message('Please input workflow name')
        else:
            params['workflow'] = workflow

        prompt = tool_parameters.get('prompt', None)
        if prompt:
            params['prompt'] = prompt

        expand = tool_parameters.get('expand', '')
        if expand:
            params['expand'] = self._str_to_bool(expand)

        image_path = tool_parameters.get('imagePath', None)
        if image_path:
            params['imagePath'] = image_path

        user_gender = tool_parameters.get('userGender', None)
        if user_gender:
            params['userGender'] = user_gender

        batch_size = tool_parameters.get('batchSize', '')
        if batch_size:
            params['batchSize'] = int(batch_size)

        lora = tool_parameters.get('lora', None)
        if lora:
            params['lora'] = lora

        lora_weight = tool_parameters.get('loraWeight', None)
        if lora_weight:
            params['loraWeight'] = lora_weight

        seed = tool_parameters.get('seed', '')
        if seed:
            params['seed'] = int(seed)

        scale_by = tool_parameters.get('scaleBy', None)
        if scale_by:
            params['scaleBy'] = scale_by

        trigger_word = tool_parameters.get('triggerWord', None)
        if trigger_word:
            params['triggerWord'] = trigger_word

        negtive_prompt = tool_parameters.get('negtivePrompt', None)
        if negtive_prompt:
            params['negtivePrompt'] = negtive_prompt

        positive_prompt = tool_parameters.get('positivePicturePrompt', None)
        if positive_prompt:
            params['positivePicturePrompt'] = positive_prompt

        single_face_fix_prompt = tool_parameters.get('singleFaceFixPrompt', None)
        if single_face_fix_prompt:
            params['singleFaceFixPrompt'] = single_face_fix_prompt

        character_num = tool_parameters.get('characterNum', '')
        if character_num:
            params['characterNum'] = int(character_num)

        image = tool_parameters.get('image', '')
        url = f"{base_url}/generate"
        if not image:
            response = requests.post(url=url, json=params)
        else:
            image_bytes = open(image, 'rb')
            image_file = {'image': image_bytes}
            response = requests.post(url=url, data=params, files=image_file)

        if 200 <= response.status_code < 300:
            response_json = response.json()
            task_id = response_json.get('taskId', None)
            while task_id:
                try:
                    response = requests.get(f"{base_url}/status?taskId={task_id}")
                    if 200 <= response.status_code < 300:
                        response_json = response.json()
                        status = response_json.get('status', '')
                        if status == 'error':
                            break
                        if status == 'done':
                            return [
                                self.create_text_message(text="images generated"),
                                self.create_json_message(response_json),
                            ]
                except RequestException:
                    pass
                time.sleep(3)

        return self.create_text_message(text="Image generation failed")

    @staticmethod
    def _str_to_bool(s: str) -> bool:
        return s.lower() in ("yes", "y", "true", "t", "1")
