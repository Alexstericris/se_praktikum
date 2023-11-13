from django.urls import path

from .views import LogView, DataTupelView
from . import views

# im 2. Path stand zwischen den '' noch test
urlpatterns = [
    path('logs', LogView.as_view()),
    path('datatuple', DataTupelView.as_view()),
    #path("loginUser/", views.loginUser),
    path("getLog/", views.getLog),
    path("filterApply/", views.filterApply),
    path("filterApplySave/", views.filterApplySave),
    path("isFilenameAvailiable/", views.isFilenameAvailable),
    path("uploadFile/", views.uploadFile),
    path("deleteFile/", views.deleteFile),
    path("getMyFilenames/", views.getMyFilenames),
    path("getAllUserFilenames/", views.getAllUserFilenames),
    path("getMyUserInformation/", views.getMyUserInformation),
    path("isTokenValid/", views.isTokenValid)
]
