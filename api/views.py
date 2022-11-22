from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta
from dashboard.models import Period, Record, TimeTable
from django.db.utils import IntegrityError
from django.conf import settings
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def entry(request):
    today = datetime.now(settings.IST).date()
    if (today.weekday() == 5 or today.weekday() == 6):
        return Response({"message": f"No Class Today"}, status=status.HTTP_404_NOT_FOUND)

    is_cached = cache.get(request.user.id)
    if (is_cached):
        return Response({"message": f"{request.user.student.roll_number} : Entry Already Recorded"}, status=status.HTTP_208_ALREADY_REPORTED)

    now = datetime.now(settings.IST)
    start = now-timedelta(minutes=settings.TOLERENCE)
    end = now+timedelta(minutes=settings.TOLERENCE)
    try:
        # fetch start period in the current_time+-tolerence range to set the entry time for record
        period: Period = getattr(TimeTable.objects.get(
            course=request.user.student.course), settings.DAYS[today.weekday()]).filter(start__range=(start, end)).get()
        new_entry = Record(student=request.user.student,
                           date=today, entry_time=period.start)
        new_entry.save()
        cache.set(f'{request.user.id}-Entry', True, settings.EXPIRY)
        return Response({"message": f"{request.user.student.roll_number} : Entry Recorded"}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({"message": f"{request.user.student.roll_number} : Entry Recorded"}, status=status.HTTP_208_ALREADY_REPORTED)
    except Period.DoesNotExist:
        return Response({"message": f"{request.user.student.roll_number} : No Entry"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def exit(request):
    if (datetime.now(settings.IST).weekday() == 5 or datetime.now(settings.IST).weekday() == 6):
        return Response({"message": f"No Class Today"}, status=status.HTTP_404_NOT_FOUND)

    is_cached = cache.get(request.user.id)
    if (is_cached):
        return Response({"message": f"{request.user.student.roll_number} : Exit Already Recorded"}, status=status.HTTP_208_ALREADY_REPORTED)

    try:
        # fetch last period in the current_time+-tolerence range to set the exit time for todays record
        record: Record = Record.objects.get(
            student=request.user.student, date=datetime.now(settings.IST).date())
        start = datetime.now(settings.IST) - \
            timedelta(minutes=settings.TOLERENCE)
        end = datetime.now(settings.IST)+timedelta(minutes=settings.TOLERENCE)
        try:
            period: Period = getattr(TimeTable.objects.get(
                course=request.user.student.course), settings.DAYS[datetime.now(settings.IST).weekday()]).filter(end__range=(start, end)).get()
            record.exit_time = period.end
            record.save()
            cache.set(f'{request.user.id}-Exit', True, settings.EXPIRY)
            return Response({"message": f"{request.user.student.roll_number} : Exit Recorded"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"message": f"{request.user.student.roll_number} : Invalid Exit"}, status=status.HTTP_400_BAD_REQUEST)
        except Period.DoesNotExist:
            return Response({"message": f"{request.user.student.roll_number} : Invalid Exit"}, status=status.HTTP_404_NOT_FOUND)
    except Record.DoesNotExist:
        return Response({"message": f"{request.user.student.roll_number} : Invalid Exit"}, status=status.HTTP_404_NOT_FOUND)
