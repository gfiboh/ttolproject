from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    
    class Meta:
        verbose_name_plural = 'ユーザー'

        
class TeachModel(models.Model):
    CATEGORY = (
        ('japanese','国語'), ('english', '英語'), ('society','社会'),
        ('math','数学'), ('physics','物理'), ('chemistry', '化学'),
        ('biology', '生物'), ('trivia','雑学'), ('howtostudy','勉強法'),
        ('etc.', 'その他')
        )

    title = models.CharField(
        verbose_name='タイトル', max_length=100
        )

    category = models.CharField(
        verbose_name='カテゴリ',
        max_length=30,
        choices=CATEGORY
    )

    serchword = models.CharField(
        verbose_name='キーワード',
        max_length=50, 
        null=True,
        blank=True
    )
    teacher = models.ForeignKey(
        CustomUser, verbose_name='作成者',
        on_delete = models.CASCADE
    )

    content = models.TextField(verbose_name='コンテンツ')

    def __str__(self):
        return self.title
