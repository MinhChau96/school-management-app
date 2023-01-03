from django import forms
from django.forms.widgets import DateInput, TextInput
from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(label='Địa chỉ mail', required=True)
    gender = forms.ChoiceField(label='Giới tính', choices=[('Nam', 'Nam'), ('Nữ', 'Nữ')])
    first_name = forms.CharField(label='Họ', required=True)
    last_name = forms.CharField(label='(Tên đệm) Tên', required=True)
    address = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={"rows": 2}))
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField(label='Ảnh đại diện', widget = forms.FileInput(
        attrs={"id": "image_field"}
    ))

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs[
                    'placeholder'] = "Chỉ điền thông tin vào ô này nếu bạn muốn thay đổi mật khẩu"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "Email đã được sử dụng, vui lòng điền email khác!")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("Email đã được sử dụng, vui lòng điền email khác!")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender', 'password', 'profile_pic', 'address']


class StudentForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + \
                 ['course', 'session']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + \
                 ['course']


class CourseForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        labels = {'name': 'Khóa học'}
        model = Course


class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        labels = {'name': 'Môn học',
                  'staff': 'Giáo viên',
                  'course': 'Khóa học'
                  }
        fields = ['name', 'staff', 'course']


class SubjectFeeForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SubjectFeeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SubjectFee
        labels = {'course': 'Khóa học',
                  'subject': 'Môn học',
                  'session': 'Nhóm',
                  'money': 'Học phí'}
        widgets = {
            'money': forms.NumberInput(attrs={'step': 50000}),
        }
        fields = ['course', 'subject', 'session', 'money']


class ReceiveSubjectFeeForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(ReceiveSubjectFeeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ReceiveSubjectFee
        labels = {'student': 'Học sinh',
                  'subject_fee': 'Học phí',
                  'other_fee': 'Chi phí khác',
                  'total_fee': 'Thành tiền phải thu',
                  'advance_money': 'Tiền đã ứng trước',
                  'payment': 'Tiền thanh toán',
                  'cash_in_return': 'Số dư tài khoản'}
        widgets = {
            'subject_fee': forms.NumberInput(attrs={'step': 10000}),
            'other_fee': forms.NumberInput(attrs={'step': 10000}),
            'total_fee': forms.NumberInput(attrs={'step': 10000}),
            'advance_money': forms.NumberInput(attrs={'step': 10000}),
            'payment': forms.NumberInput(attrs={'step': 10000}),
            'cash_in_return': forms.NumberInput(attrs={'step': 10000}),
        }
        fields = ['student', 'subject_fee', 'other_fee', 'total_fee', 'advance_money', 'payment', 'cash_in_return']


class SessionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = '__all__'
        labels = {'start_year': 'Bắt đầu',
                  'end_year': 'Kết thúc'
                  }
        widgets = {
            'start_year': DateInput(attrs={'type': 'date'}),
            'end_year': DateInput(attrs={'type': 'date'}),
        }


class LeaveReportStaffForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStaff
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackStaffForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStaff
        fields = ['feedback']


class LeaveReportStudentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStudent
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackStudentForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStudent
        fields = ['feedback']


class StudentEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields


class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields


class EditResultForm(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultForm, self).__init__(*args, **kwargs)

    class Meta:
        model = StudentResult
        fields = ['session_year', 'subject', 'student', 'test', 'exam']
