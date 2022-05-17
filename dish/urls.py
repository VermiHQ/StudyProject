from django.urls import path
from . import views
# ограничение не авториованных пользователей
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

app_name = 'dish'
urlpatterns = [
	path('by_type/<int:pk>/', view = views.ByTypeView.as_view(), name = 'by_type'),
	path('by_user/<int:pk>/', views.ByUserView.as_view(), name = 'by_user'),
	path('by_user_like/<int:pk>/', view=login_required(views.ByUserLikeView.as_view(), login_url=reverse_lazy('auth:login')), name = 'by_user_like'),
	path('dish/<int:dish_id>/', views.by_dish_id, name='by_dish_id'),
	path('search/', views.ingr_search, name='search'),
	path('new_dish/', view=login_required(views.CreateDish.as_view(), login_url=reverse_lazy('auth:login')), name='new_dish'),
	path('new_dish/new_ingr/', view=login_required(views.CreateIngredient.as_view(), login_url=reverse_lazy('auth:login')), name='new_ingr'),
	path('update/<int:pk>/', view=login_required(views.UpdateDish.as_view(), login_url=reverse_lazy('auth:login')), name='update'),
	path('dish/<int:pk>/delete_dish', view=login_required(views.DeleteDish.as_view(), login_url=reverse_lazy('auth:login')), name='delete'),
	path('like/<int:dish_id>/', views.like, name='like'),
	path('', views.IndexView.as_view(), name = 'index'),
]