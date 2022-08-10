from django.shortcuts import render


def privacy_policy(request):
    return render(request, 'templates/privacy_policy.html', {})


def personal_data(request):
    return render(request, 'templates/personal_data.html', {})
