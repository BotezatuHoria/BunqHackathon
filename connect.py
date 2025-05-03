from bunq.sdk.context.api_context import ApiContext
from bunq import ApiEnvironmentType

api_context = ApiContext.create(
    ApiEnvironmentType.SANDBOX,
    "sandbox_8dc8c6f8016266a027acf022ff568aadc4c1dc307148493406f8af54",
    "My Python Device"
)
#api_context.save("bunq.conf")
print("✅ API context saved")