from celery import shared_task
from django.core.mail import EmailMessage


@shared_task(ignore_result=True, bind=True, max_retries=3, default_retry_delay=5, acks_late=True, reject_on_worker_lost=True,)
def send_welcome_email(self,subject,message,sender,receiver):
    try:
        email = EmailMessage(
            subject,
            message,
            sender,
            [receiver]
        )

        email.content_subtype = "html"
        email.send(fail_silently=True)
        pass
    except Exception as exc:
        raise self.retry(exc=exc)
    




@shared_task(ignore_result=True, bind=True, max_retries=3, default_retry_delay=5, acks_late=True, reject_on_worker_lost=True,)
def check_rate_limit(self,api,limit):
    try:
        import asyncio
        import aiohttp

        async def fetch(session, url):
            async with session.get(url) as response:
                return response.status

        async def main():
            async with aiohttp.ClientSession() as session:
                tasks = [
                    fetch(session, api)
                    for _ in range(limit)
                ]

                results = await asyncio.gather(*tasks)
                print(results)

        asyncio.run(main())
        pass
    except Exception as exc:
        raise self.retry(exc=exc)
    