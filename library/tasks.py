from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from datetime import date 
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)
today = timezone.now().date()

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task(bind=True, max_retries=3)
def check_overdue_loans(self,loan_id):
    member_email = loan.member.user.email
    overdue_loans = Loan.objects.filter(is_returned=False, due_date__lt=today)

    for loan in overdue_loans:
        try:
            send_mail(
            subject='over Due Period reached',
            message=f'Hello {loan.member.user.username},\n\nYou loan period is over due Please return it as soon as possible',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
        except Exception as e:
            #logs the error and retries 3 times with countdown of 60secs
            logger.error(f"the email couldnt be send due to {str(e)} retrying")
            raise self.retry(exc=e, countdown=60)
