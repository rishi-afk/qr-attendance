from django.shortcuts import render, redirect


def entry(request):
    return render(request, 'scanner/entry.html')


def exit(request):
    return render(request, 'scanner/exit.html')
