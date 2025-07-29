from django.urls import path
from .views import InnovationDiagnosisSubmissionView

urlpatterns = [
    path('innovation-diagnosis-submit/', InnovationDiagnosisSubmissionView.as_view({'post': 'create'}), name='innovation-diagnosis-submit'),
    # path('mailing-list-join/', MailingListSignupView.as_view({'post': 'create'}), name='mailing-list-join'),
] 