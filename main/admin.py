from django.contrib import admin
from .models import Citation, Source, Like, Dislike

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    
@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('text',)}
    exclude=('views',)

admin.site.register(Like)

admin.site.register(Dislike)