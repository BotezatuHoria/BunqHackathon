from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.model.generated.endpoint import PaymentApiObject
from bunq.sdk.model.generated.object_ import AmountObject, PointerObject

# api_context = ApiContext.restore("bunq.conf")
# BunqContext.load_api_context(api_context)
#
# # Access the user context
# user_context = BunqContext.user_context()
#
# # Get the user ID
# user_id = user_context.user_id
#
# # Get the primary monetary account
# primary_account = user_context.primary_monetary_account
#
# print(primary_account)

api_context = ApiContext.restore("bunq.conf")
BunqContext.load_api_context(api_context)

def make_payment_email(who,money,receiver_email):
    api_contextSender = ApiContext.restore("fake_users/"+who+"_bunq.conf")
    BunqContext.load_api_context(api_contextSender)
    payment = PaymentApiObject.create(
        amount=AmountObject(money, "EUR"),
        counterparty_alias=PointerObject("EMAIL", receiver_email),
        description="Payment for services"
    ).value

    return {
        "id": payment.id_,
        "amount": payment.amount.value,
        "currency": payment.amount.currency,
        "description": payment.description,
        "created": payment.created
    }
def make_payment_Iban(who,money,receiver_iban):
    api_contextSender = ApiContext.restore("fake_users/"+who+"_bunq.conf")
    BunqContext.load_api_context(api_contextSender)
    payment = PaymentApiObject.create(
        amount=AmountObject(money, "EUR"),
        counterparty_alias=PointerObject("IBAN", receiver_iban),
        description="Payment for services"
    ).value

    return {
        "id": payment.id_,
        "amount": payment.amount.value,
        "currency": payment.amount.currency,
        "description": payment.description,
        "created": payment.created
    }


def get_all_transactions():
    payments = PaymentApiObject.list().value

    if not payments:
        print("No transactions found.")
        return

    for payment in payments:
        print(f"💸 ID: {payment.id_}")
        print(f"   Amount: {payment.amount.value} {payment.amount.currency}")
        print(f"   Description: {payment.description}")
        print(f"   Date: {payment.created}")
        print("---")

# Run the function
#print(make_payment())
print(get_all_transactions())
# aliases = BunqContext.user_context().primary_monetary_account.alias
# for alias in aliases:
#     print(f"{alias.type_}: {alias.value}")