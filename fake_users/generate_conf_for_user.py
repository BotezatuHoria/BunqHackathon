from bunq.sdk.context.api_context import ApiContext
from bunq import ApiEnvironmentType


def generate_conf(api_key,name):
    api_context = ApiContext.create(
        ApiEnvironmentType.SANDBOX,
        api_key,
        name
    )
    api_context.save(name+".conf")
    print("✅ saved")

generate_conf("sandbox_0e43e831578732ca1624aeb2c57e2e1c8ad7c3526ebf5ba0aa44189d","1883393")