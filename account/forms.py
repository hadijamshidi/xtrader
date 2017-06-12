from django.forms import (Form, ModelForm,
                          PasswordInput, ValidationError,
                          CharField, ImageField, EmailField, DateField)
from django.contrib.auth import (authenticate, get_user_model)
from django.contrib.auth.forms import (PasswordChangeForm,
                                       PasswordResetForm,
                                       UserCreationForm)
from django.db.models import Q
from .models import Profile

User = get_user_model()


class UserLoginForm(Form):
    username = CharField(label='نام‌کاربری', error_messages={'required': 'لطفا نام‌کاربری خود را وارد نمایید.'})
    password = CharField(label='گذرواژه', widget=PasswordInput,
                         error_messages={'required': 'لطفا گذرواژهٔ خود را وارد نمایید.'})

    def clean(self, *args, **kargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            user_qs = User.objects.filter(Q(username=username) | Q(email=username))
            if user_qs.count() == 0:
                if '@' in username:
                    raise ValidationError("کاربری با ایمیل " + username + " وجود ندارد!")
                else:
                    raise ValidationError("کاربر " + username + " وجود ندارد!")
            if not user:
                raise ValidationError("گذرواژه اشتباه است!")
            if not user.check_password(password):
                raise ValidationError("گذرواژه اشتباه است!")
            if not user.is_active:
                raise ValidationError("اشتراک کاربر " + username + " غیر فعال شده است.")

        return super(UserLoginForm, self).clean(*args, **kargs)


class UserRegistrationForm(UserCreationForm):
    email = EmailField(label='آدرس ایمیل', error_messages={'required': 'لطفا ایمیل خود را وارد نمایید.'})
    password1 = CharField(label='گذرواژه', widget=PasswordInput,
                          error_messages={'required': 'لطفا گذرواژهٔ خود را وارد نمایید.'})
    password2 = CharField(label='تکرار گذرواژه', widget=PasswordInput,
                          error_messages={'required': 'لطفا گذرواژهٔ خود را دوباره وارد نمایید.'})
    first_name = CharField(label='نام', error_messages={'required': 'لطفا نام خود را وارد نمایید.'})
    last_name = CharField(label='نام خانوادگی',
                          error_messages={'required': 'لطفا نام خانوادگی خود را وارد نمایید.'})
    username = CharField(label='نام کاربری',
                         error_messages={'required': 'لطفا نام کاربری خود را وارد نمایید.'},
                         help_text='الزامی. ۳۰ کاراکتر یا کمتر. فقط حروف الفبا، ارقام و @/./+/-/_.')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        ]


class UserEditForm():
    # first_name = CharField(label='نام',
    #                              error_messages={'required': 'لطفا نام خود را وارد نمایید.'})
    # last_name = CharField(label='نام خانوادگی',
    #                             error_messages={'required': 'لطفا نام خانوادگی خود را وارد نمایید.'})
    # email = EmailField(label='ایمیل', error_messages={'required': 'لطفا ایمیل خود را وارد نمایید.'})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(ModelForm):
    date_of_birth = DateField(label='تاریخ تولد', required=False)
    photo = ImageField(label='عکس', required=False)

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')


class MyPasswordChangeForm(PasswordChangeForm):
    #
    # old_password = CharField(label='گذرواژهٔ قدیمی', widget=PasswordInput, strip=False,
    #                                error_messages={'required': 'لطفا گذرواژهٔ خود را وارد نمایید.'})
    # new_password1 = CharField(label='گذرواژهٔ جدید', widget=PasswordInput, strip=False,
    #                                 help_text=password_validation.password_validators_help_text_html(),
    #                                 error_messages={'required': 'لطفا گذرواژهٔ خود را وارد نمایید.'})
    # new_password2 = CharField(label='تکرار گذرواژه', widget=PasswordInput, strip=False,
    #                                 error_messages={'required': 'لطفا گذرواژهٔ خود را وارد نمایید.'})
    pass


class MyPasswordResetForm(PasswordResetForm):
    # email = EmailField(label='ایمیل', error_messages={'required': 'لطفا ایمیل خود را وارد نمایید.'})
    pass
