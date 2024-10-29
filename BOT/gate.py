import httpx
import asyncio
import logging
from asyncio import Semaphore

# Configure logging
logging.basicConfig(level=logging.INFO)

# Stripe API keys
sk = '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'
pk = 'pk_live_51Oe5itKiK7vykOc70DH5o1EEnTVkFm1ssGU5SL3EJnYf7r3AYqjvkX09r0GVlPMG5856TkrZXJwSSTtEOkjS6dGb00OzbxBNrp'

# Directly update sk and pk without persisting
def update_keys(new_sk, new_pk):
    global sk, pk
    sk = new_sk
    pk = new_pk

# Define the semaphore with a reasonable default (adjust as needed)
CONCURRENT_REQUESTS = 200
semaphore = Semaphore(CONCURRENT_REQUESTS)  # Limit concurrent requests

async def create_payment_method(cc, mes, ano, cvv, session):
    data = {
        'type': 'card',
        'card[number]': cc,
        'card[exp_month]': mes,
        'card[exp_year]': ano,
        'card[cvc]': cvv
    }
    async with semaphore:
        response = await session.post(
            'https://api.stripe.com/v1/payment_methods',
            data=data,
            auth=(sk, '')
        )
    return response.text

async def create_payment_intent(payment_method, amount, session):
    data = {
        'amount': amount * 100,  # Amount in cents, which is equal to 1 USD.
        'currency': 'usd',
        'payment_method': payment_method,
        'confirmation_method': 'automatic',
        'confirm': 'true',
        'off_session': 'true'
    }
    async with semaphore:
        response = await session.post(
            'https://api.stripe.com/v1/payment_intents',
            data=data,
            auth=(sk, '')
        )
    return response.text

async def main_svv(i):
    async with httpx.AsyncClient() as session:
        print(i)
        cc, mes, ano, cvv = i.split('|')
        resp = await create_payment_method(cc, mes, ano, cvv, session)
        getres_result = await create_payment_intent(resp, 1, session)
        return getres_result
