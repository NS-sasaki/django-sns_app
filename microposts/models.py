from django.db import models


class Post(models.Model):
    # Postのオーナーを設定する
    owner = models.ForeignKey('accounts.User', verbose_name='オーナー', on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='images/',blank=True, null=True) # 追加

    class Meta:
        db_table = 'posts'

class Gallery(models.Model):
    # Imageのオーナーを設定する
    owner = models.ForeignKey('accounts.User', verbose_name='オーナー', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='gallery/') # 追加

    class Meta:
        db_table = 'gallery'

    def __str__(self):
        return str(self.pk)