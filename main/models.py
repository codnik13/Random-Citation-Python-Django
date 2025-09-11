from os import name
from django.db import models

class Source(models.Model):
    title=models.CharField(max_length=250, unique=True, verbose_name='Название')
    count=models.PositiveIntegerField(default=1, verbose_name='Счетчик')
    slug=models.SlugField(max_length=250,unique=True,blank=True,null=True, verbose_name='URL')
    
    def __str__(self):
        return self.source

class Citation(models.Model):
    source=models.CharField(max_length=250, verbose_name='Источник')
    text=models.TextField(unique=True, verbose_name='Цитата')
    weight=models.PositiveIntegerField(default=0, verbose_name='Вес')
    views=models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    likes=models.PositiveIntegerField(default=0, verbose_name='Лайки', )
    dislikes=models.PositiveIntegerField(default=0, verbose_name='Дизлайки')
    slug=models.SlugField(max_length=250,unique=True,blank=True,null=True, verbose_name='URL')
    
    class Meta:
        db_table='citation'
        verbose_name='Цитата'
        verbose_name_plural='Цитаты'
        
    def __str__(self):
        return self.source
    
class Like(models.Model):
    user=models.GenericIPAddressField(verbose_name='IP пользователя')
    citation=models.ForeignKey(Citation, on_delete=models.CASCADE, verbose_name='Цитата')
    
    def __str__(self):
        return f'пользователь {self.user}: цитата {self.citation}'
    
class Dislike(models.Model):
    user=models.GenericIPAddressField(verbose_name='IP пользователя')
    citation=models.ForeignKey(Citation, on_delete=models.CASCADE, verbose_name='Цитата')
    def __str__(self):
        return f'пользователь {self.user}: цитата {self.citation}'