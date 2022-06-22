from django.forms import FileField, Form


class MassiveMenuUpdateForm(Form):
    menu_file = FileField()
