from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.dalle_web.tools.dalle_webapi import DalleWebApiTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class DalleWebProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict) -> None:
        try:
            DalleWebApiTool().fork_tool_runtime(
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
        