from django.shortcuts import render

from .models import ekexam


def ekexam_page(request):
    exams = (
        ekexam.objects.filter(is_public=True)
        .prefetch_related('participants')
        .order_by('-exam_date', '-created_at')
    )
    context = {
        'student_name': 'Егор Калинин',
        'student_group': '241-671',
        'exams': exams,
    }
    return render(request, 'rentals/ekexam.html', context)
