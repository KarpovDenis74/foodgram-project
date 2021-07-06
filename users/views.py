from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
from users.forms import CreationForm, FormUsersEdit
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
import logging

# настраиваем логирование в приложении Users
users_logger = logging.getLogger("Users")
users_logger.setLevel(logging.INFO)
fh = logging.FileHandler(filename="users.log", mode="w")
formatter = logging.Formatter('%(asctime)s - %(name)s'
                              ' - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
users_logger.addHandler(fh)

User = get_user_model()


class SignUp(CreateView):
    template_name = 'users/reg.html'
    form_class = CreationForm
    success_url = reverse_lazy(
        "login")

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        try:
            send_mail(
                'Подтверждение пароля',
                'Вам необходимо подтвердить пароль, пройдя по сслке <a href=""> Cskrf </a>',
                settings.EMAIL_HOST_USER,
                [self.object.email],
                fail_silently=False,
            )
        except Exception as e:
            users_logger.error(f'Регистрация пользователя username: {self.object.username}.'
                               f'Ошибка отправки письма на адрес: {self.object.email} {e.args[-1]}')
        return super().form_valid(form)


@login_required
def users_admin(request):
    count = User.objects.all()
    return render(request, 'users/users_admin.html',
                  {'count': count}
                  )


@login_required
def users_admin_edit(request, user_id):
    if not request.user.is_admin:
        return redirect('index')
    user = get_object_or_404(User, pk=user_id)
    form = FormUsersEdit(request.POST or None, instance=user)
    if not form.is_valid():
        return render(request, 'users/users_admin_edit.html',
                      {'user': user, 'form': form}
                      )
    user = form.save()

    return redirect('users_admin')


@login_required
def users_admin_delete(request, user_id):
    if not request.user.is_admin:
        return redirect('index')
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('users_admin')
