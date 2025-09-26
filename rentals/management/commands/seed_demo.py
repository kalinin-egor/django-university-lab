from datetime import date, timedelta
import io
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from rentals.models import ekexam

try:
    from PIL import Image, ImageDraw
except ImportError as exc:  # pragma: no cover
    raise SystemExit('Pillow is required to run this command.') from exc


class Command(BaseCommand):
    help = 'Populate the database with sample users and ekexam records.'

    def handle(self, *args, **options):
        base_dir = Path('media/exam_tasks')
        base_dir.mkdir(parents=True, exist_ok=True)

        users = self._ensure_users()
        exams_created = self._ensure_exams(users)

        self.stdout.write(self.style.SUCCESS(f'Seed complete. Exams in database: {exams_created}'))

    def _ensure_users(self):
        User = get_user_model()
        user_specs = [
            {
                'username': 'student1',
                'email': 'student1@example.com',
                'first_name': 'Иван',
                'last_name': 'Иванов',
            },
            {
                'username': 'student2',
                'email': 'student2@example.com',
                'first_name': 'Мария',
                'last_name': 'Петрова',
            },
            {
                'username': 'student3',
                'email': 'student3@example.com',
                'first_name': 'Дмитрий',
                'last_name': 'Смирнов',
            },
            {
                'username': 'student4',
                'email': 'student4@example.com',
                'first_name': 'Анна',
                'last_name': 'Соколова',
            },
        ]

        users = []
        for spec in user_specs:
            user, created = User.objects.get_or_create(username=spec['username'], defaults=spec)
            if created:
                user.set_password('password123')
                user.save(update_fields=['password'])
            else:
                for field, value in spec.items():
                    if getattr(user, field) != value:
                        setattr(user, field, value)
                user.save()
            users.append(user)
        return users

    def _ensure_exams(self, users):
        base_date = date.today()
        exam_specs = [
            {
                'name': 'Экзамен по Django',
                'offset': 7,
                'is_public': True,
                'participants': users[:3],
            },
            {
                'name': 'Экзамен по Базам данных',
                'offset': 14,
                'is_public': True,
                'participants': users[1:4],
            },
            {
                'name': 'Экзамен по Python',
                'offset': -5,
                'is_public': True,
                'participants': users[:2],
            },
            {
                'name': 'Экзамен по Построению API',
                'offset': 21,
                'is_public': False,
                'participants': users[::2],
            },
            {
                'name': 'Экзамен по Docker',
                'offset': 30,
                'is_public': True,
                'participants': users,
            },
        ]

        for spec in exam_specs:
            exam_date = base_date + timedelta(days=spec['offset'])
            exam, created = ekexam.objects.get_or_create(
                name=spec['name'],
                defaults={
                    'exam_date': exam_date,
                    'is_public': spec['is_public'],
                },
            )
            if not created:
                exam.exam_date = exam_date
                exam.is_public = spec['is_public']

            task_image = self._build_image(spec['name'])
            exam.task_image.save(task_image.name, task_image, save=False)
            exam.save()
            exam.participants.set(spec['participants'])
        return ekexam.objects.count()

    def _build_image(self, title: str) -> ContentFile:
        width, height = 640, 360
        image = Image.new('RGB', (width, height), color='#f3f4f6')
        draw = ImageDraw.Draw(image)

        heading = f'Экзамен: {title}'
        subheading = 'Задание 1'

        def center_text(text, y):
            bbox = draw.textbbox((0, 0), text)
            text_width = bbox[2] - bbox[0]
            draw.text(((width - text_width) / 2, y), text, fill='#1f2937')

        center_text(heading, height * 0.35)
        center_text(subheading, height * 0.55)

        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        filename = f"{title.lower().replace(' ', '_').replace('/', '_')}.png"
        return ContentFile(buffer.getvalue(), name=filename)
