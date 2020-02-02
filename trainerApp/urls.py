from django.urls import path
from . import views

urlpatterns = [
    path('trainer_list', views.TrainerList.as_view({'get': 'trainer_list'})),
    path('add_trainer', views.AddTrainer.as_view({'get': 'trainer_data'})),
    path('update_trainer/<slug:slug>', views.UpdateTrainer.as_view()),
    path('get_trainer_by_slug/<slug:slug>', views.GetTrainerBySlug.as_view()),
    path('post_ratings', views.RatingsPostView.as_view({'get': 'ratings_list'})),
    path('update_ratings/<int:trainer>/<int:user>', views.RatingsPutView.as_view()),
    path('user_update_ratings/<int:trainer>/<int:user>', views.UserRatingsPutView.as_view()),
    path('all_ratings/<int:pk>', views.UserTrainerReviews.as_view()),
]
