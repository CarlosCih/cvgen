from django.db.models import Q
from django.shortcuts import render

from .models import Profile

def profile_view(request):
    query = request.GET.get('q', '').strip()
    resumes = Profile.objects.all().order_by('name')

    if query:
        resumes = resumes.filter(Q(name__icontains=query) | Q(email__icontains=query))

    return render(request, 'main/index.html', {'query': query, 'resumes': resumes})
