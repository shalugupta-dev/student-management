
from django import forms
from .models import Attendance


class AttendanceDateForm(forms.Form):
    date = forms.DateField(
        label="Attendance Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        )
    )


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["status"]

        widgets = {
            "status": forms.Select(
                attrs={"class": "form-select"}
            )
        }
