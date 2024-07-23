from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.voice.tools.tts import TtsTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class VoiceProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict) -> None:
        try:
            TtsTool().fork_tool_runtime(
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
