from .views import ( ProjectCreateView, ProjectAllListView, ProjectListViewDelete, ProjectIDListView,
 ProjectListView, CategoriesListView, Sub_CategoriesListView, subSub_CategoriesListView,ProjectUploadImage, Sub_CategoriesListOnlyView, subSub_CategoriesListOnlyView, subSub_CategoriesDeleteView, CategoriesDeleteView, Sub_CategoriesDeleteView, ProjectUserListView )
# from .views import ProjectListView, ProjectAllListView, ProjectListViewDelete, ProjectCreateView
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from . import views

urlpatterns = [
      path('<slug>/', ProjectListView.as_view(), name="SingleProjectList"),
      path('single/<int:pk>/', ProjectIDListView.as_view(), name="ProjectIDListView"),
      path('product/delete/<int:pk>/', ProjectListViewDelete.as_view(), name="ProjectListViewDelete"),
      path('product_update/<int:pk>/', views.Product.as_view()),

      path('', ProjectAllListView.as_view(), name="AllProjectList"),
      path('<int:seller_id>', ProjectUserListView.as_view(), name="AllProjectList"),
      path('create/product', ProjectCreateView.as_view(), name="createProduct"),

 
      path('product/category', CategoriesListView.as_view(), name="category"),
      path('product/category/delete/<int:pk>', CategoriesDeleteView.as_view(), name="category_delete"),
      path('product/category/<int:pk>', views.CategoryDetailView.as_view()),
      path('category/update/<int:pk>', views.CategoryUpdate.as_view()),
      path('category/add', views.CategoryAdd.as_view({'get': 'category_list'})),


      path('product/subcategory/<int:category>', Sub_CategoriesListView.as_view(), name="subcategory"),
      path('product/subcategory/all', Sub_CategoriesListOnlyView.as_view(), name="subcategory"),
      path('product/subcategory/delete/<int:pk>', Sub_CategoriesDeleteView.as_view(), name="subcategory_delete"),
      path('subcategory/<int:pk>/', views.SubCategory.as_view()),
      path('subcategory/add', views.SubCategoryAdd.as_view({'get': 'subcategory_list'})),

      path('product/brand/create', subSub_CategoriesListView.as_view(), name="create_brand"),
      path('product/brand/<int:category>', subSub_CategoriesListView.as_view(), name="brand"),
      path('product/brand/all', subSub_CategoriesListOnlyView.as_view(), name="brand"),
      path('product/brand/delete/<int:pk>', subSub_CategoriesDeleteView.as_view(), name="brand"),
      path('brand/<int:pk>/', views.Brand.as_view()),

      path('upload/image', ProjectUploadImage.as_view(), name="image_uploader"),

      path('product_pagination', views.ProductByPagination.as_view(), name="product_pagination"),
      url(r'^productbycategory/(?P<pk>[0-9]+)', views.ProductsByCategory.as_view()),
      url(r'^product_image$', views.ProductUploadImage.as_view()),

      #frontEnd

      


      
]
