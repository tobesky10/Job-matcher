
from django import forms

class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(required=False, label="Upload Resume File")
    resume_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10}),
        required=False,
        label="Or Paste Resume Text"
    )

    def clean(self):
        cleaned_data = super().clean()
        resume_file = cleaned_data.get("resume_file")
        resume_text = cleaned_data.get("resume_text")

        if not resume_file and not resume_text:
            raise forms.ValidationError("Please upload a file or paste resume text.")
        return cleaned_data



class Profileform(forms.Form):
    first_name = forms.CharField(label='Firstname', max_length=15, required=True)
    last_name = forms.CharField(label='Lastname', max_length=15, required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', max_length=256, required=True, widget=forms.PasswordInput)
    mode = [
        ('Personal', 'Personal'),
        ('Business', 'Business'),
    ]
    dropdown = forms.ChoiceField(choices=mode, label="Account Type", required=True)


class Loginform(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', max_length=256, required=True, widget=forms.PasswordInput)

