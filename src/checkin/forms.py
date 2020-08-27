from django import forms


class EmailCheckinForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput(
            attrs={'placeholder': 'Email'}),
			required=False,
	)


class SwipeCheckinForm(forms.Form):
    fsu_num = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Swipe your FSU Card'}),
		required=False,
    )

    # determines if the swipe is valid
    def valid_read(self):
        if self.cleaned_data['fsu_num'][1] == 'B':
            return True
        return False

    # returns last 8 numbers of fsu number
    def parse(self):
        return self.cleaned_data['fsu_num'][10:18]
