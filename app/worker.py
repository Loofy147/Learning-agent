from celery import Celery
from .config import settings

celery = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        'process-orders-every-minute': {
            'task': 'app.worker.process_orders',
            'schedule': 60.0,
        },
    },
)

@celery.task
def process_orders():
    from . import database, models, api_client
    db = next(database.get_db())

    current_price = api_client.get_btc_price_usd_sync()
    if current_price is None:
        return

    active_orders = db.query(models.Order).filter(models.Order.is_active == True).all()
    for order in active_orders:
        wallet = db.query(models.Wallet).filter(models.Wallet.id == order.wallet_id).first()
        if order.order_type == "buy" and current_price <= order.price_usd:
            usd_needed = order.btc_amount * order.price_usd
            if wallet.usd_balance >= usd_needed:
                wallet.usd_balance -= usd_needed
                wallet.btc_balance += order.btc_amount
                transaction = models.Transaction(
                    wallet_id=wallet.id,
                    transaction_type="buy",
                    btc_amount=order.btc_amount,
                    usd_amount=usd_needed,
                )
                db.add(transaction)
                order.is_active = False
        elif order.order_type == "sell" and current_price >= order.price_usd:
            if wallet.btc_balance >= order.btc_amount:
                usd_gained = order.btc_amount * order.price_usd
                wallet.btc_balance -= order.btc_amount
                wallet.usd_balance += usd_gained
                transaction = models.Transaction(
                    wallet_id=wallet.id,
                    transaction_type="sell",
                    btc_amount=order.btc_amount,
                    usd_amount=usd_gained,
                )
                db.add(transaction)
                order.is_active = False
    db.commit()
