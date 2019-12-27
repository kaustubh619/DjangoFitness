from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^blog_categories', views.BlogCategoryView.as_view({'get': 'cat_list'})),
    path('blog_post/', views.BlogPostView.as_view(), name="blog_post$"),
    path('blog/', views.BlogPostViewWithoutPagination.as_view(), name="blog_post$"),
    url(r'^blogbycategory/(?P<pk>[0-9]+)', views.BlogByCategory.as_view()),
    url(r'^blogbyid/(?P<slug>[-\w]+)$', views.BlogById.as_view()),
    url(r'^blogcomment/(?P<pk>[0-9]+)$', views.BlogCommentView.as_view()),
    path('comment/', views.BlogCommentPostView.as_view({'get': 'comment_list'})),
    url(r'^blog_like/(?P<slug>[-\w]+)$', views.BlogPostLikeView.as_view()),
]
