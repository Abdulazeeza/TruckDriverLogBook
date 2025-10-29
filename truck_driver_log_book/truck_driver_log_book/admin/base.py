from django.contrib import admin
from django.db.models import QuerySet

class BaseModelAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        q = self.model.objects.with_deleted() #type: QuerySet

        if self.change_select_related:
            q = q.select_related(*self.change_select_related)
        elif self.list_select_related:
            q = q.select_related(*self.list_select_related)

        return q

    list_display = ('is_deleted',)
    list_filter = ('is_deleted',)
    readonly_fields = ('deleted_at', 'is_deleted')
    list_select_related = ()
    change_select_related = list_select_related + ()
    list_per_page = 50
