from django.urls import path
from .views import InnovationDiagnosisSubmissionView, MailingListSignupView, ContactUsView

urlpatterns = [
    path('innovation-submition/', InnovationDiagnosisSubmissionView.as_view({'post': 'create'}), name='innovation-diagnosis-submit'),
    path('mailing-list-join/', MailingListSignupView.as_view({'post': 'create'}), name='mailing-list-join'),
    path('contact-us/', ContactUsView.as_view({'post' : 'create'}), name='contact-us')
] 