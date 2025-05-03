from bunq import ApiEnvironmentType
from bunq.sdk.context.api_context import ApiContext
from bunq.sdk.context.bunq_context import BunqContext
from bunq.sdk.model.generated.endpoint import PaymentApiObject, MonetaryAccountBankApiObject
from bunq.sdk.model.generated.object_ import AmountObject, PointerObject
from bunq.sdk.model.generated.endpoint import RequestInquiryApiObject
from bunq.sdk.model.generated.endpoint import MonetaryAccountBankApiObject


def make_payment_Email(who,money,receiver_email,description):
    api_contextSender = ApiContext.restore("fake_users/"+who+".conf")
    BunqContext.load_api_context(api_contextSender)
    try:
        payment_id  = PaymentApiObject.create(
            amount=AmountObject(money, "EUR"),
            counterparty_alias=PointerObject("EMAIL", receiver_email),
            description=description
        ).value
        return True
    except Exception as e:
        print(f"❌ Error making payment: {e}")
        return False

def make_payment_Iban(who,money,receiver_iban,description):
    api_contextSender = ApiContext.restore("fake_users/"+who+".conf")
    BunqContext.load_api_context(api_contextSender)
    try:
        payment = PaymentApiObject.create(
            amount=AmountObject(money, "EUR"),
            counterparty_alias=PointerObject("IBAN", receiver_iban),
            description=description
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

#it returns all transactions from all accounts of a user
def get_all_transactions_from_user_api(user_api):
    api_context = ApiContext.create(
        ApiEnvironmentType.SANDBOX,
        user_api,
        "Temp Session"
    )
    BunqContext.load_api_context(api_context)

    accounts = MonetaryAccountBankApiObject.list().value
    transactions = []

    for account in accounts:
        account_id = account.id_
        payments = PaymentApiObject.list().value
        transactions.extend(payments)
    return transactions


def create_money_request_from_user_api(user_api, to_email, amount_eur, description="Please pay me"):
    api_contextSender = ApiContext.create(
        ApiEnvironmentType.SANDBOX,
        user_api,
        "Temp Session"
    )
    BunqContext.load_api_context(api_contextSender)

    user_id = BunqContext.user_context().user_id
    account = BunqContext.user_context().primary_monetary_account
    monetary_account_id = account.id_

    # Create the request
    request_id = RequestInquiryApiObject.create(
        amount_inquired=AmountObject(str(amount_eur), "EUR"),
        counterparty_alias=PointerObject("EMAIL", "sugardaddy@bunq.com", "Sugar Daddy"),
        description="You're the best!",
        allow_bunqme=True,
        monetary_account_id=monetary_account_id,
        # user_id is inferred automatically from context
    ).value

    print("✅ Money request created!")
    return True

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

def get_user_details(who):
    # Load API context
    api_context = ApiContext.restore(f"fake_users/{who}.conf")
    BunqContext.load_api_context(api_context)

    user_context = BunqContext.user_context()
    user_id = user_context.user_id
    account = user_context.primary_monetary_account
    balance = account.balance
    currency = balance.currency
    account_id = account.id_
    aliases = account.alias

    # Extract alias info (email/IBAN)
    alias_info = [(alias.type_, alias.value) for alias in aliases]

    # Get address_main
    address_main = None
    if user_context.user_person:
        name = user_context.user_person.display_name
        address_main = user_context.user_person.address_main
    elif user_context.user_company:
        name = user_context.user_company.name
        address_main = user_context.user_company.address_main
    else:
        name = "Unknown"

    # print(f"👤 User: {name} (User ID: {user_id})")
    # print(f"💰 Balance: {balance.value} {currency}")
    # print(f"🏦 Account ID: {account_id}")
    # print(f"🔗 Aliases: {alias_info}")
    # print(f"📍 Address Main: {address_main}")

    return {
        "user_id": user_id,
        "name": name,
        "account_id": account_id,
        "balance_value": balance.value,
        "balance_currency": currency,
        "aliases": alias_info,
        "address_main": {
            "street": address_main.street,
            "house_number": address_main.house_number,
            "postal_code": address_main.postal_code,
            "city": address_main.city,
            "country": address_main.country,
            "is_user_address_updated": address_main.is_user_address_updated
        } if address_main else None
    }
# Run the function
#Mihaita -> David   test+0b05e3bc-7efd-4675-b5d4-ca3a8982b0f6@bunq.com
#top_up_user("fake_users/1882147.conf", "test+0b05e3bc-7efd-4675-b5d4-ca3a8982b0f6@bunq.com", amount="500")
#top_up_user("fake_users/1882147.conf", "", amount="5")
#make_payment_email("Mihaita","50","test+0b05e3bc-7efd-4675-b5d4-ca3a8982b0f6@bunq.com")
#print(get_all_transactions_from_user_api("sandbox_d199e92eb4646fce5b3ced92b2d8fc0c062fa389084c988a0bd7fdb0"))
#print(get_all_transactions_from_user_api("sandbox_d199e92eb4646fce5b3ced92b2d8fc0c062fa389084c988a0bd7fdb0"))
#make_payment_Email("Mihaita","2","test+0b05e3bc-7efd-4675-b5d4-ca3a8982b0f6@bunq.com")

#create_money_request_from_user_api("sandbox_d199e92eb4646fce5b3ced92b2d8fc0c062fa389084c988a0bd7fdb0","sugardaddy@bunq.com","5")

# create_money_request_from_user_api("sandbox_8dc8c6f8016266a027acf022ff568aadc4c1dc307148493406f8af54","sugardaddy@bunq.com","2")
#create_money_request("1880854","sugardaddy@bunq.com","2")
# create_money_request("1880854","sugardaddy@bunq.com","2")


#make_payment_Email("1880854","20","test+c4eb6b86-8652-4049-a2ec-eb7e741f5ae1@bunq.com","Wine, Rotterdam")
#make_payment_Email("1880854","45","test+c4eb6b86-8652-4049-a2ec-eb7e741f5ae1@bunq.com","12 Beers at Constanta, Romania")
#make_payment_Email("1880854","12","test+c4eb6b86-8652-4049-a2ec-eb7e741f5ae1@bunq.com","Sun glassses at Costinesti Romania")
#make_payment_Email("1880854","100","test+c4eb6b86-8652-4049-a2ec-eb7e741f5ae1@bunq.com","Aperol at Vama Veche, Romania")
# make_payment_Email("1880854","50","test+c4eb6b86-8652-4049-a2ec-eb7e741f5ae1@bunq.com","Femei")
make_payment_Email("1880854","10","test+c4eb6b86-8652-4049-a2ec-eb7e741f5ae1@bunq.com","Spritz (wine+water) at Mangalia, Romania")
# make_payment_Email("1880854","10","test+c4eb6b86-8652-4049-a2ec-eb7e741f5ae1@bunq.com","Coffee at Sofia, Bulgaria")

#get_user_details("1880854")
get_user_balance("1882147") #1882147 Mihaita
get_user_balance("1880854") #1880854 David
#get_user_balance_from_user_api("sandbox_d199e92eb4646fce5b3ced92b2d8fc0c062fa389084c988a0bd7fdb0") #1880854 David