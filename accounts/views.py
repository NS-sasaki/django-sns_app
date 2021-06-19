from django.shortcuts import render, redirect, get_object_or_404 # 追加
from django.views.generic.edit import CreateView, UpdateView 
from django.views.generic.base import TemplateView
from .forms import RegistForm, LoginForm, ProfileForm  
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView 
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import User, Relationship # 追加

class HomeView(TemplateView):
    template_name = 'accounts/home.html'

class RegistUserView(CreateView):
    template_name = 'accounts/regist.html'
    form_class = RegistForm

class UserLoginView(LoginView):  
    template_name = 'accounts/login.html'
    authentication_form = LoginForm

    # def form_valid(self, form):
    #     remember = form.cleaned_data['remember']
    #     if remember:
    #         self.request.session.set_expiry(120000)
    #     return super().form_valid(form)

class UserLogoutView(LogoutView): 
    pass

class ProfileEditView(LoginRequiredMixin, UpdateView): # 追加
    template_name = 'accounts/edit_profile.html'
    model = User
    form_class = ProfileForm
    success_url = '/accounts/edit_profile/'

    def get_object(self):
        return self.request.user


class UserListView(LoginRequiredMixin, ListView): 
    template_name = 'accounts/userlist.html'
    model = User
    # ページネーションの表示件数
    #paginate_by = 3

    def get_queryset(self):
        # return Users.objects.all()
        return User.objects.all()

    def get_context_data(self, **kwargs): # 追加
        context = super().get_context_data(**kwargs)
        user = self.request.user
        followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
        context['following_list'] = User.objects.filter(id__in=followings)
        return context


## htmlからpkお気に入りに入れたい人のpkを取得
def mk_relation(request, pk): # 追加
    # ログインユーザーを取得
    follower = get_object_or_404(User, pk=request.user.pk)
    # フォローしたい相手(引数pkをテンプレートから取得)
    following = get_object_or_404(User, pk=pk)
    make_relation = Relationship(follower_id=follower.id, following_id=following.id)
    make_relation.save()

    return redirect('accounts:userlist')


def rm_relation(request, pk): # 追加
    # ログインユーザーを取得
    follower = get_object_or_404(User, pk=request.user.pk)
    # フォローしたい相手(引数pkをテンプレートから取得)
    following = get_object_or_404(User, pk=pk)
    # Relationship内のデータレコード（objects)を削除
    # model.objects.filter(***)でQuetySetを取得し.delete()で削除
    clear_relation = Relationship.objects.filter(follower_id=follower.id, following_id=following.id)
    clear_relation.delete()

    return redirect('accounts:userlist')
