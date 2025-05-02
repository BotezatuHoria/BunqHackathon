from bunq.sdk.context.api_context import ApiContext
from bunq import ApiEnvironmentType

api_context = ApiContext.create(
    ApiEnvironmentType.SANDBOX,
    "sandbox_d199e92eb4646fce5b3ced92b2d8fc0c062fa389084c988a0bd7fdb0",
    "My Python Device"
)
api_context.save("bunq.conf")
print("✅ API context saved")