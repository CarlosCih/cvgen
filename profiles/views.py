from django.db.models import Q
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .generador import build_profile_pdf, profile_pdf_filename
from .models import Profile


def profile_view(request):
    query = request.GET.get('q', '').strip()
    resumes = Profile.objects.all().order_by('name')

    if query:
        resumes = resumes.filter(Q(name__icontains=query) | Q(email__icontains=query))

    return render(request, 'main/index.html', {'query': query, 'resumes': resumes})


class CVCreateView(CreateView):
    model = Profile
    fields = [
        'name',
        'email',
        'phone',
        'degree',
        'school',
        'university',
        'sumary',
        'previous_work',
        'skills',
    ]
    template_name = 'main/form.html'
    success_url = reverse_lazy('profile')


class CVUpdateView(UpdateView):
    model = Profile
    fields = [
        'name',
        'email',
        'phone',
        'degree',
        'school',
        'university',
        'sumary',
        'previous_work',
        'skills',
    ]
    template_name = 'main/form.html'
    success_url = reverse_lazy('profile')


def CVDelete(request, id):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, id=id)
        profile.delete()
    return redirect('profile')


def resume(request, id):
    user_profile = get_object_or_404(Profile, id=id)
    return render(request, 'main/resume.html', {'user_profile': user_profile})


def DownloadPDF(request, id):
    user_profile = get_object_or_404(Profile, id=id)

    try:
        pdf_buffer = build_profile_pdf(user_profile)
    except RuntimeError as exc:
        return HttpResponseServerError(str(exc))

    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{profile_pdf_filename(user_profile)}"'
    return response
