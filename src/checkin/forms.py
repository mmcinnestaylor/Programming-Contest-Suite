from django import forms


class EmailCheckinForm(forms.Form):
    """
    Form for email based check-in.
    """
     
    email = forms.EmailField(widget=forms.EmailInput(
            attrs={'placeholder': 'Enter your registered email'}),
            required=False,
    )


class SwipeCheckinForm(forms.Form):
    """
    Form for swipe based check-in with FSUCard.
    """

    fsu_num = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Swipe your FSU Card'}),
        required=False,
    )

    # determines if the swipe is valid
    def valid_read(self):
        return len(self.cleaned_data['fsu_num']) > 2 and self.cleaned_data['fsu_num'][1] == 'B'


    # returns last 8 numbers of fsu number
    def parse(self):
        return int(self.cleaned_data['fsu_num'][10:18])


class WalkinForm(forms.Form):
    """
    Form for walk-in contestant check-in.
    """
    
    DIVISIONS = (
        (1, "Upper"),
        (2, "Lower"),
    )
    
    division = forms.ChoiceField(choices=DIVISIONS, widget=forms.RadioSelect(), required=False)


class VolunteerForm(forms.Form):
    """
    Form for contest volunteer check-in.
    """

    username = forms.CharField(max_length=150, label='Username', help_text='Your account username.')
    pin = forms.CharField(max_length=8, label='Volunteer PIN', help_text='Provided by contest organizers.', widget=forms.PasswordInput())
