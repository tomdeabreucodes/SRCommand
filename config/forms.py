from django import forms


class GameForm(forms.Form):
    game_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': "e.g. 'Wii Sports' or 'smb'"}))


class GameAlias(forms.Form):
    game_alias = forms.CharField(max_length=20)


class CategoryAlias(forms.Form):
    category_alias = forms.CharField(max_length=20)


class SrdcUserForm(forms.Form):
    srdc_username = forms.CharField(max_length=100)
