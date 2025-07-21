from django.urls import path
from .views import InnovationDiagnosisSubmissionView, MailingListSignupView

urlpatterns = [
    path('innovation-diagnosis-submit/', InnovationDiagnosisSubmissionView.as_view({'post': 'create'}), name='innovation-diagnosis-submit'),
    path('mailing-list-join/', MailingListSignupView.as_view({'post': 'create'}), name='mailing-list-join'),
] 