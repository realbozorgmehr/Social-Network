from django.contrib import admin
from .models import Post, Comment, Vote


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated', 'user')
    search_fields = ('title', 'body', 'slug')
    list_filter = ('created', 'updated', 'user')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'is_reply')
    raw_id_fields = ('user', 'post', 'reply')


admin.site.register(Vote)
