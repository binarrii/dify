from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.comfyui.tools.comfyapi import ComfyApiTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class ComfyUIProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict) -> None:
        try:
            ComfyApiTool().fork_tool_runtime(
                runtime={
                    "credentials": credentials,
                }
            ).invoke(
                user_id='',
                tool_parameters={
                    "query": "binarii",
                },
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
