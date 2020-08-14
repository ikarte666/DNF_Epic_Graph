from django import forms


class DateInput(forms.DateInput):
    input_type = "date"


class SearchForm(forms.Form):

    SERVER_VALUE = (
        ("cain", "카인"),
        ("hilder", "힐더"),
        ("prey", "프레이"),
        ("casillas", "카시야스"),
        ("siroco", "시로코"),
        ("diregie", "디레지에"),
        ("anton", "안톤"),
        ("bakal", "바칼"),
    )
    server = forms.ChoiceField(choices=SERVER_VALUE, label_suffix="", label="서버")
    char_name = forms.CharField(max_length=12, label_suffix="", label="캐릭터명", required=False)
    start_date = forms.DateField(widget=DateInput, label_suffix="", label="시작일", required=False)
    end_date = forms.DateField(widget=DateInput, label_suffix="", label="종료일", required=False)
