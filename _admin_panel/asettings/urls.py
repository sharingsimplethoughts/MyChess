from django.urls import *
from .views import *

app_name='ap_settings'

urlpatterns=[
    path('list',SettingsManagementListView.as_view(),name="ap_set_list"),
    # path('settings_list/',SettingsManagementListView.as_view(),name='apsetm_set_list'),

    #Edit related
    path('edit/<str:id>',SettingsManagementEditView.as_view(),name='apsetm_edit'),
    path('faq/edit/',SettingsManagementFaqEditView.as_view(),name='apsetm_faq_edit'),
    
    #View related
    path('faq/',SettingsManagementFaqView.as_view(),name='apsetm_faq'),
    path('about_us/',SettingsManagementAboutUsView.as_view(),name='apsetm_aboutus'),
    path('privacy_policy/',SettingsManagementPrivacyPolicyView.as_view(),name='apsetm_privacypolicy'),
    path('terms_and_condition/',SettingsManagementTermsAndConditionView.as_view(),name='apsetm_termsandcondition'),
    path('help/',SettingsManagementHelpView.as_view(),name='apsetm_help'),
    path('legal/',SettingsManagementLegalView.as_view(),name='apsetm_legal'),
    #View arabic related
    # path('faq_ar/',SettingsManagementFaq_ArView.as_view(),name='apsetm_faq_ar'),
    # path('about_us_ar/',SettingsManagementAboutUs_ArView.as_view(),name='apsetm_aboutus_ar'),
    # path('privacy_policy_ar/',SettingsManagementPrivacyPolicy_ArView.as_view(),name='apsetm_privacypolicy_ar'),
    # path('terms_and_condition_ar/',SettingsManagementTermsAndCondition_ArView.as_view(),name='apsetm_termsandcondition_ar'),
    # path('help_ar/',SettingsManagementHelp_ArView.as_view(),name='apsetm_help_ar'),
    # path('legal_ar/',SettingsManagementLegal_ArView.as_view(),name='apsetm_legal_ar'),
]