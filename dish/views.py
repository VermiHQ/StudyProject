from .models import Dish, Type, Ingredient
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import Http404
# используется для наследования классами различного преднащначения
from django.views import generic
from django.contrib.auth.models import User
from .forms import SearchForm, DishForm
# пагинатор
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(generic.ListView):
	paginate_by = 6
	model = Dish
	template_name = 'dish/index.html'
	context_object_name = 'ds'
	queryset = Dish.objects.order_by('-update_date')
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet
		context['types'] = Type.objects.order_by('name')
		return context


# !!!переписана как класс!!! см. выше
# def index(request):
# 	ds = Dish.objects.order_by('-update_date')[:10]
# 	types = Type.objects.all()
# 	context = {'ds': ds, 'types': types}
# 	return render(request=request, template_name='dish/index.html', context=context)

# создание нового ингредиента
class CreateIngredient(generic.CreateView):
	model = Ingredient
	fields = ['name']
	template_name = 'dish/new_ingr.html'
	def get_success_url(self):
		return reverse('dish:new_dish')
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet
		context['types'] = Type.objects.order_by('name')
		return context

# создание нового рецепта
class CreateDish(generic.CreateView):
	model = Dish
	form_class = DishForm
	template_name = 'dish/new_dish.html'
	def form_valid(self, form):
		form.instance.author = self.request.user
		self.dish = form.save()
		return super().form_valid(form)
	def get_success_url(self):
		return reverse('dish:by_dish_id', args=(self.dish.id, ))
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet
		context['types'] = Type.objects.order_by('id')
		return context

# обновление рецепта
class UpdateDish(generic.UpdateView):
	model = Dish
	fields = ['title', 'type', 'ingredients', 'recipe', 'image']
	template_name = 'dish/new_dish.html'
	def get_success_url(self):
		return reverse('dish:by_dish_id', args=(self.object.id, ))
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet
		context['types'] = Type.objects.order_by('name')
		return context

# удаление рецепта
class DeleteDish(generic.DeleteView):
	model = Dish
	template_name = 'dish/delete_dish.html'
	def get_success_url(self):
		return reverse('dish:index')

# просмотр списка рецептов по типу/категории блюда
class ByTypeView(generic.DetailView):
	model = Type
	template_name = 'dish/by_type.html'
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet
		context['types'] = Type.objects.order_by('name')
		if Dish.objects.filter(type = self.kwargs['pk']):
			context['ds'] = Dish.objects.filter(type = self.kwargs['pk'])
		context['current_type'] = get_object_or_404(Type, pk = self.kwargs['pk'])
		return context

# !!!переписана как класс!!! см. выше
# def by_type(request, type_id):
# 	ds = Dish.objects.filter(type = type_id)
# 	types = Type.objects.all()
# 	current_type = get_object_or_404(Type, pk = type_id)
# 	context = {'ds': ds, 'types': types, 'current_type': current_type}
# 	return render(request, 'dish/by_type.html', context)

# просмотр блюд пользователя
class ByUserView(generic.DetailView):
	model = User
	template_name = 'dish/by_user.html'
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet
		context['types'] = Type.objects.order_by('name')
		context['ds'] = Dish.objects.filter(author = self.kwargs['pk'])
		context['current_user'] = get_object_or_404(User, pk = self.kwargs['pk'])
		return context

# просмотр лайкнутых блюд пользователя
class ByUserLikeView(generic.DetailView):
	model = User
	template_name = 'dish/by_user_like.html'
	list_dishs_like = []
	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		# Add in a QuerySet
		for d in Dish.objects.all():
			if d.was_like(str(self.kwargs['pk'])) and d not in self.list_dishs_like:
				self.list_dishs_like.append(d)
		context['types'] = Type.objects.order_by('name')
		context['ds'] = self.list_dishs_like
		context['current_user'] = get_object_or_404(User, pk = self.kwargs['pk'])
		return context

# просмотр отдельного рецепта
def by_dish_id(request, dish_id):
	types = Type.objects.order_by('name')
	try:
		current_dish = Dish.objects.get(pk = dish_id)
	except Dish.DoesNotExist:
		raise Http404("Такого блюда в данный момент нету в списке блюд.")
	current_ingr = current_dish.ingredients.all()
	liked = current_dish.was_like(request.user.id)
	context = {'types': types, 'current_dish': current_dish, 'current_ingr': current_ingr, 'liked': liked}
	return render(request, 'dish/by_dish_id.html', context)

# возможность ставить метку "лайк"
def like(request, dish_id):
	current_dish = get_object_or_404(Dish, pk=dish_id)
	if not current_dish.was_like(request.user.id):
		current_dish.likes += 1
		current_dish.user_likes += str(request.user.id) + " "
		current_dish.save()
	return redirect('/dish/' + str(dish_id))

# поиск по ингредиентам
def ingr_search(request):
	types = Type.objects.order_by('name')
	form = SearchForm()
	query = None
	results = []
	paginator = Paginator(results, 7)
	page = request.GET.get('page') or 1
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			for q in query.replace(',','').split():
				# если объекта не существует, просто продолжим поиск(обход ошибки DoesNotExists)
				try:
					q_id = Ingredient.objects.get(name=q).id
				except:
					continue
				if not results:
					results = set(Dish.objects.filter(ingredients = q_id))
				else:
					results = set(results)
					results &= set(Dish.objects.filter(ingredients=q_id))
				results = list(results)
				paginator = Paginator(results, 7)
				page = request.GET.get('page') or 1
				try:
					results = paginator.page(page)
				except PageNotAnInteger:
					results = paginator.page(1)
				except EmptyPage:
					results = paginator.page(paginator.num_pages)
	count = len(results)
	context = {'types': types, 'form': form, 'query': query, 'results': results, 'count': count, 'page': page}
	return render(request, 'dish/search.html', context)

