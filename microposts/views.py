from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView 
from django.views.generic.edit import CreateView, UpdateView 
from django.views.generic import ListView , DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post,Gallery# 追加
from accounts.models import Relationship, User 
from .forms import PostCreateForm, PostUpdateForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponse,JsonResponse # 追加

# Create your views here.
class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'microposts/create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('microposts:create')

    def form_valid(self, form):
        # formに問題なければ、owner id に自分のUser idを割り当てる        
        # request.userが一つのセットでAuthenticationMiddlewareでセットされている。
        form.instance.owner_id = self.request.user.id
        messages.success(self.request, '投稿が完了しました')
        return super(PostCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, '投稿が失敗しました')
        return redirect('microposts:create')

class PostListView(LoginRequiredMixin, ListView):   
    # テンプレートを指定
    template_name = 'microposts/postlist.html'
    # 利用するモデルを指定
    model = Post
    # ページネーションの表示件数
    paginate_by = 3

    # Postsテーブルの全データを取得するメソッド定義
    # テンプレートでは、object_listとしてreturnの値が渡される
    def get_queryset(self):
        return Post.objects.all()  


    def get_context_data(self, **kwargs): # 追加
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['favourite_list'] = user.favourite_post.all()

        return context

class PostUpdateView(LoginRequiredMixin, UpdateView): 
    model = Post
    form_class = PostUpdateForm
    template_name = 'microposts/update.html'

    def form_valid(self, form):
        messages.success(self.request, '更新が完了しました')
        return super(PostUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('microposts:update', kwargs={'pk': self.object.id})

    def form_invalid(self, form):
        messages.warning(self.request, '更新が失敗しました')
        return reverse_lazy('microposts:update', kwargs={'pk': self.object.id})

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'microposts/delete.html'
    # deleteviewでは、SuccessMessageMixinが使われないので設定する必要あり
    success_url = reverse_lazy('microposts:create')
    success_message = "投稿は削除されました。"

    # 削除された際にメッセージが表示されるようにする。
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

class MyPostsView(LoginRequiredMixin, ListView): 
    # テンプレートを指定
    template_name = 'microposts/myposts.html'
    # 利用するモデルを指定
    model = Post
    # ページネーションの表示件数
    paginate_by = 3

    # Postsテーブルのowner_idが自分自身の全データを取得するメソッド定義
    def get_queryset(self):  
        qs = Post.objects.filter(owner_id=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        qs = Post.objects.filter(owner_id=self.request.user)
        # qsのレコード数をmy_posts_countというコンテキストとして設定
        context['my_posts_count'] = qs.count()
        # Postsテーブルの全データを取得しpost_listへ格納
        context['favorite_list'] = user.favourite_post.all()
        context['following_list'] = Relationship.objects.filter(follower_id=user.id)
        # 自分がfollowしているidのみをmy_follow_listとして取得
        context['my_follow_list'] = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id', flat=True)
        # 自分がフォローしている人をfollowingsとして取得
        followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
        context['following_count'] = User.objects.filter(id__in=followings).count()
        # 自分をフォローしている人をfollowersとして取得
        followers = (Relationship.objects.filter(following_id=user.id)).values_list('follower_id')
        # context['followers_data] = User.objects.filter(id__in=followers).count()
        context['follower_count'] = followers.count()
        return context

def add_favourite(request, pk): # 追加
    # postのpkをhtmlから取得
    post = get_object_or_404(Post, pk=pk)
    # ログインユーザーを取得
    user = request.user
    # ログインユーザーをfavoritePostのUser_idとして、post_idは
    # 上で取得したPostを記録
    user.favourite_post.add(post)
    return redirect('microposts:postlist')


def remove_favourite(request, pk): # 追加
    # postのpkをhtmlから取得
    post = get_object_or_404(Post, pk=pk)
    # ログインユーザーを取得
    user = request.user
    # ログインユーザーをfavoritePostのUser_idとして、post_idは
    # 上で取得したPostを記録
    user.favourite_post.remove(post)
    return redirect('microposts:postlist')

class FollowersView(LoginRequiredMixin, ListView): # 追加
    # テンプレートを指定
    template_name = 'microposts/followers.html'
    # 利用するモデルを指定
    model = Relationship

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Postsテーブルの自分の投稿数をmy_posts_countへ格納
        context['my_posts_count'] = Post.objects.filter(owner_id=self.request.user).count()
        # 自分がフォローしている人をfollowingsとして取得
        followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
        # 自分がフォローしている人のオブジェクトを取得
        context['following_list'] = User.objects.filter(id__in=followings)
        # 自分がフォローしている人の数を取得
        context['following_count'] = User.objects.filter(id__in=followings).count()
        # 自分をフォローしている人をfollowersとして取得
        followers = (Relationship.objects.filter(following_id=user.id)).values_list('follower_id')
        # 自分をフォローしている人の数を取得
        context['follower_list'] = User.objects.filter(id__in=followers)
        return context


class FollowingView(LoginRequiredMixin, ListView): # 追加
    # テンプレートを指定
    template_name = 'microposts/followings.html'
    # 利用するモデルを指定
    model = Relationship

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Postsテーブルの自分の投稿数をmy_posts_countへ格納
        context['my_posts_count'] = Post.objects.filter(owner_id=self.request.user).count()
        # 自分がフォローしている人をfollowingsとして取得
        followings = (Relationship.objects.filter(follower_id=user.id)).values_list('following_id')
        # 自分がフォローしている人のオブジェクトを取得
        context['following_list'] = User.objects.filter(id__in=followings)
        # 自分をフォローしている人をfollowersとして取得
        followers = (Relationship.objects.filter(following_id=user.id)).values_list('follower_id')
        # 自分をフォローしている人の数を取得
        context['follower_count'] = User.objects.filter(id__in=followers).count()
        return context

# file(=画像)をアップロードする関数
def add_file(request):
    if request.method == "POST":        
        # ログインユーザーを取得
        user = request.user
        # 画像をテンプレートからfileとして取得
        pict = request.FILES.get('file')
        # Galleryモデルにオーナーと画像を保存
        Gallery.objects.create(owner = user, image=pict)
        return HttpResponse('')
    return HttpResponse('post error')

class GalleryView(LoginRequiredMixin,ListView):
    template_name = 'microposts/gallery.html'
    # 利用するモデルを指定
    model = Gallery    
    
    # Galleryテーブルのowner_idが自分自身の全データを取得するqs
    def get_queryset(self):  
        qs = Gallery.objects.filter(owner_id=self.request.user)
        return qs