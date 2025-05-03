from bunq.sdk.context.api_context import ApiContext
from bunq import ApiEnvironmentType


def generate_conf(api_key,name):
    api_context = ApiContext.create(
        ApiEnvironmentType.SANDBOX,
        api_key,
        name
    )
    api_context.save(name+"_bunq.conf")
    print("✅ saved")

generate_conf("sandbox_d199e92eb4646fce5b3ced92b2d8fc0c062fa389084c988a0bd7fdb0","David")