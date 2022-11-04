import pytz
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from dashboard.models import Period, Record, TimeTable
from django.db.utils import IntegrityError

IST = pytz.timezone('Asia/Kolkata')
EXPIRY = 60*2
DAYS = {0: 'monday', 1: 'tuesday',
        2: 'wednesday', 3: 'thursday', 4: 'friday'}

TOLERENCE = 6


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def entry(request):
    today = datetime.now(IST).date()
    if (today.weekday() == 5 or today.weekday() == 6):
        return Response({"message": f"No Class Today"}, status=status.HTTP_404_NOT_FOUND)

    is_cached = cache.get(request.user.id)
    if (is_cached):
        return Response({"message": f"{request.user.student.roll_number} : Entry Already Recorded"}, status=status.HTTP_208_ALREADY_REPORTED)

    start = datetime.now(IST)-timedelta(minutes=TOLERENCE)
    end = datetime.now(IST)+timedelta(minutes=TOLERENCE)
    try:
        period: Period = getattr(TimeTable.objects.get(
            course=request.user.student.course), DAYS[today.weekday()]).filter(start__range=(start, end)).get()
        new_entry = Record(student=request.user.student,
                           date=today, entry_time=period.start)
        new_entry.save()
        cache.set(f'{request.user.id}-Entry', True, EXPIRY)
        return Response({"message": f"{request.user.student.roll_number} : Entry Recorded"}, status=status.HTTP_201_CREATED)
    except IntegrityError:
        return Response({"message": f"{request.user.student.roll_number} : Entry Recorded"}, status=status.HTTP_208_ALREADY_REPORTED)
    except Period.DoesNotExist:
        return Response({"message": f"{request.user.student.roll_number} : No Entry"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def exit(request):
    if (datetime.now(IST).weekday() == 5 or datetime.now(IST).weekday() == 6):
        return Response({"message": f"No Class Today"}, status=status.HTTP_404_NOT_FOUND)

    is_cached = cache.get(request.user.id)
    if (is_cached):
        return Response({"message": f"{request.user.student.roll_number} : Exit Already Recorded"}, status=status.HTTP_208_ALREADY_REPORTED)

    try:
        record: Record = Record.objects.get(
            student=request.user.student, date=datetime.now(IST).date())
        start = datetime.now(IST).now()-timedelta(minutes=TOLERENCE)
        end = datetime.now(IST).now()+timedelta(minutes=TOLERENCE)
        try:
            period: Period = getattr(TimeTable.objects.get(
                course=request.user.student.course), DAYS[datetime.now(IST).weekday()]).filter(end__range=(start, end)).get()
            record.exit_time = period.end
            record.save()
            cache.set(f'{request.user.id}-Exit', True, EXPIRY)
            return Response({"message": f"{request.user.student.roll_number} : Exit Recorded"}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"message": f"{request.user.student.roll_number} : Invalid Exit"}, status=status.HTTP_400_BAD_REQUEST)
        except Period.DoesNotExist:
            return Response({"message": f"{request.user.student.roll_number} : Invalid Exit"}, status=status.HTTP_404_NOT_FOUND)
    except Record.DoesNotExist:
        return Response({"message": f"{request.user.student.roll_number} : Invalid Exit"}, status=status.HTTP_404_NOT_FOUND)
