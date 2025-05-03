from bunq import ApiEnvironmentType
from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.model.generated.endpoint import PaymentApiObject, MonetaryAccountBankApiObject
from bunq.sdk.model.generated.object_ import AmountObject, PointerObject
from bunq.sdk.model.generated.endpoint import RequestInquiryApiObject


def make_payment_Email(who,money,receiver_email):
    api_contextSender = ApiContext.restore("fake_users/"+who+".conf")
    BunqContext.load_api_context(api_contextSender)
    try:
        payment_id  = PaymentApiObject.create(
            amount=AmountObject(money, "EUR"),
            counterparty_alias=PointerObject("EMAIL", receiver_email),
            description="Payment for services"
        ).value
        return True
    except Exception as e:
        print(f"❌ Error making payment: {e}")
        return False

def make_payment_Iban(who,money,receiver_iban):
    api_contextSender = ApiContext.restore("fake_users/"+who+".conf")
    BunqContext.load_api_context(api_contextSender)
    try:
        payment = PaymentApiObject.create(
            amount=AmountObject(money, "EUR"),
            counterparty_alias=PointerObject("IBAN", receiver_iban),
            description="Payment for services"
        ).value
        return True
    except Exception as e:
        print(f"❌ Error making payment: {e}")
        return False

def get_all_transactions(who):
    api_contextSender = ApiContext.restore("fake_users/"+str(who)+".conf")
    BunqContext.load_api_context(api_contextSender)
    payments = PaymentApiObject.list().value

    if not payments:
        print("No transactions found.")
        return None
    return payments

def get_all_transactions_from_user_api(user_api):
    api_context = ApiContext.create(
        ApiEnvironmentType.SANDBOX,
        user_api,
        "Temp Session"
    )
    BunqContext.load_api_context(api_context)
    payments = PaymentApiObject.list().value

    if not payments:
        print("No transactions found.")
        return
    return payments

def create_money_request(who, to_email, amount_eur, description="Please pay me"):
    api_contextSender = ApiContext.restore("fake_users/"+who+".conf")
    BunqContext.load_api_context(api_contextSender)

    inquiry = RequestInquiryApiObject.create(
        amount_inquired=AmountObject(str(amount_eur), "EUR"),
        counterparty_alias=PointerObject("EMAIL", to_email),
        description=description,
        allow_bunqme=True  # optional: allows it to be paid via bunq.me link
    )

    print("✅ Money request created!")
    return inquiry.value

def get_user_balance_from_user_api(api_key: str):
    # Dynamically create a new context from sandbox API key
    api_context = ApiContext.create(
        ApiEnvironmentType.SANDBOX,
        api_key,
        "Temp Session"
    )
    BunqContext.load_api_context(api_context)

    account = BunqContext.user_context().primary_monetary_account
    balance = account.balance

    print(f"💰 Balance: {balance.value} {balance.currency}")
    return balance.value, balance.currency
def get_user_balance(who):
    api_contextSender = ApiContext.restore("fake_users/"+who+".conf")
    BunqContext.load_api_context(api_contextSender)

    account = BunqContext.user_context().primary_monetary_account
    balance = account.balance

    print(f"💰 Balance: {balance.value} {balance.currency}")
    return balance.value, balance.currency
# Run the function
#Mihaita -> David   test+0b05e3bc-7efd-4675-b5d4-ca3a8982b0f6@bunq.com
#top_up_user("fake_users/1882147.conf", "test+0b05e3bc-7efd-4675-b5d4-ca3a8982b0f6@bunq.com", amount="500")
#top_up_user("fake_users/1882147.conf", "", amount="5")
#make_payment_email("Mihaita","50","test+0b05e3bc-7efd-4675-b5d4-ca3a8982b0f6@bunq.com")
#print(get_all_transactions("1882147"))
print(get_all_transactions_from_user_api("sandbox_d199e92eb4646fce5b3ced92b2d8fc0c062fa389084c988a0bd7fdb0"))
#make_payment_Email("Mihaita","2","test+0b05e3bc-7efd-4675-b5d4-ca3a8982b0f6@bunq.com")
#create_money_request("Mihaita","sugardaddy@bunq.com","100")

get_user_balance("1882147") #1882147 Mihaita
get_user_balance_from_user_api("sandbox_d199e92eb4646fce5b3ced92b2d8fc0c062fa389084c988a0bd7fdb0") #1880854 David