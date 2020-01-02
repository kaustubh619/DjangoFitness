from django.urls import path
from . import views

urlpatterns = [
    path('blog_categories', views.BlogCategoryView.as_view({'get': 'cat_list'})),
    path('blog_post/', views.BlogPostView.as_view(), name="blog_post$"),
    path('blog/', views.BlogPostViewWithoutPagination.as_view(), name="blog_post$"),
    path('blogbycategory/<int:pk>', views.BlogByCategory.as_view()),
    path('blogbyid/<slug:slug>', views.BlogById.as_view()),
    path('blogcomment/<int:pk>', views.BlogCommentView.as_view()),
    path('comment/', views.BlogCommentPostView.as_view({'get': 'comment_list'})),
    path('blog_like/<slug:slug>', views.BlogPostLikeView.as_view()),
]