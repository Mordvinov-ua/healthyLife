from django.contrib import admin, messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from carts.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin
from users.forms import TrackingNumberForm
from users.models import *

@admin.action(description='Отправить e-mail с трекинговым номером')
def send_tracking_email(modeladmin, request, queryset):

    if "apply" in request.POST:
        form = TrackingNumberForm(request.POST)
        
        # Проверяем, валидна ли форма
        if form.is_valid():
            tracking_number = form.cleaned_data['tracking_number']
            success_count = 0
            failure_count = 0

            for obj in queryset:
                if obj.email:
                    try:
                        send_mail(
                            'Your tracking number',
                            f'Your tracking number: {tracking_number}',
                            'ukrainehealthy.life@gmail.com',
                            [obj.email],
                            fail_silently=False,
                        )
                        success_count += 1
                    except Exception as e:
                        failure_count += 1
                        modeladmin.message_user(request, f'Ошибка при отправке для {obj.email}: {e}', messages.ERROR)
                else:
                    failure_count += 1
                    modeladmin.message_user(request, f'У пользователя {obj} нет e-mail адреса', messages.WARNING)

            if success_count > 0:
                modeladmin.message_user(request, f'Письма успешно отправлены: {success_count}', messages.SUCCESS)
            if failure_count > 0:
                modeladmin.message_user(request, f'Не удалось отправить письма: {failure_count}', messages.WARNING)

            return HttpResponseRedirect(request.get_full_path())
        else:
            modeladmin.message_user(request, 'Ошибка валидации формы', messages.ERROR)

    else:
        form = TrackingNumberForm()

    return render(request, 'admin/send_tracking_email.html', {'form': form, 'users': queryset})

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email", ]
    search_fields = ["username", "first_name", "last_name", "email", ]
    inlines = [CartTabAdmin, OrderTabulareAdmin, ]
    actions = [send_tracking_email]


