from django.urls import path
from .views import *

urlpatterns = [
    path('listings', ListingListView.as_view()),
    path('listings/mine', MineView.as_view()),
    path('listings/<int:pk>', ListingDetailView.as_view()),
    path('listings/<int:pk>/contact', ListingContactView.as_view()),

]
