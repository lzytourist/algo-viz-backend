from django.contrib import admin

from .forms import AlgorithmCategoryForm, AlgorithmForm
from .filters import YearFilter
from .models import Algorithm, AlgorithmCategory, Comment, UserProgress


class AlgorithmCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_parent')
    prepopulated_fields = {'slug': ('name',)}
    form = AlgorithmCategoryForm

    def get_parent(self, obj):
        if not obj.parent:
            return '-'
        return obj.parent.name

    get_parent.short_description = 'Parent Category'


class AlgorithmAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category__name', YearFilter)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'category__name')
    form = AlgorithmForm


admin.site.register(AlgorithmCategory, AlgorithmCategoryAdmin)
admin.site.register(Algorithm, AlgorithmAdmin)
admin.site.register(Comment)
admin.site.register(UserProgress)
