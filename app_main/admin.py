from django.contrib import admin
from app_main.models import (
    Slider , RoadMap , Team, Blog,
    CecMembers, years_list, rank_list,
    AttachmentFiles)
    
    
class AttachmentFilesInline(admin.TabularInline):
    model = AttachmentFiles
    extra = 1


class SliderAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'publish')
    list_editable = ('publish',)
    list_filter = ('publish',)
    search_fields = ('name',)
    ordering = ['-id',]


class RoadMapAdmin(admin.ModelAdmin):
    list_display = ('text', 'DateCreate', 'state')
    list_editable = ('state', 'DateCreate')
    list_filter = ('state', 'DateCreate')
    search_fields = ('text', 'DateCreate', 'state')
    ordering = ['state' , '-DateCreate']


class TeamAdmin(admin.ModelAdmin):
    list_display = ('avatar_tag', 'name', 'description')
    list_editable = ('name', 'description')
    list_filter = ('name', 'description')
    search_fields = ('name', 'description')


class BlogAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'title', 'publish', 'category', 'DateCreate')
    list_editable = ('title', 'publish', 'category')
    list_filter = ('category', 'title','publish')
    search_fields = ('title','DateCreate','publish' , 'category')
    ordering = ['-_DateCreate', 'category' , 'title']
    
    inlines = [
        AttachmentFilesInline,
    ]


class CecMembersAdmin(admin.ModelAdmin):
        list_display = ('profile_pic','name','rank', 'year')
        list_editable = ('name','rank', 'year')
        list_filter = ('rank', 'year')
        search_fields = ('name', 'rank')
        ordering = ['-year__start_year', 'rank__rank_type_order', 'rank__order', 'name']


class RankListAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'order', 'rank_type_order', 'rank_type')
    list_editable = ('order', 'rank_type', 'year', 'rank_type_order')
    list_filter = ('rank_type', 'name', 'order')
    ordering = ['-year__start_year', 'rank_type_order', 'order']


admin.site.register(Slider, SliderAdmin)
admin.site.register(RoadMap, RoadMapAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(CecMembers , CecMembersAdmin)
admin.site.register(years_list)
admin.site.register(rank_list, RankListAdmin)
admin.site.register(AttachmentFiles)

