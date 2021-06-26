from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.urls import reverse_lazy

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email') # エラーメッセージ
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password) # passwordを引数にとってパスワード設定
        user.save(using=self._db) # データベースへユーザーを保存
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # プロフィール画像をavatarとして設定
    avatar = models.ImageField(blank=True, null=True)  

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] 

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('accounts:home')

    # 　お気に入り機能の追加. Blank Trueを忘れずに。
    # DjangoはデフォルトでManyToManyはUniqueになる。
    # ManyToManyの場合は、on_deleteは不要
    favourite_post = models.ManyToManyField(
        'microposts.Post', blank=True,
        verbose_name='お気に入りの投稿'
    )

class Relationship(models.Model):
    # 自分をお気に入り登録してくれている人
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    # 自分がお気に入り登録している人
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

    # 重複してフォロー関係を作成しなように制約を設定する
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'],
                                    name='user-relationship')
        ]

    def __str__(self):
        return "{} : {}".format(self.follower.username, self.following.username)