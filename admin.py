from django.contrib import admin
from blogApp.models import Post,Author
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display=['id','title','content','Author','created_at','updated_at']
    
admin.site.register(Post,PostAdmin)
admin.site.register(Author)
    