from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from account.models import UserProfile, LawyerProfile
from .models import ContactRequest, TimeSlot, BookingSession, Message

from .emails import notify_new_message


# ── Booking ────────────────────────────────���──────────────────────────���────

@login_required
def book_session(request):
    lawyers = User.objects.filter(lawyer_profile__isnull=False)
    if request.method == 'POST':
        slot_pk = request.POST.get('time_slot')
        notes = request.POST.get('notes', '')
        slot = get_object_or_404(TimeSlot, pk=slot_pk, is_available=True)
        session = BookingSession.objects.create(
            customer=request.user,
            lawyer=slot.lawyer,
            time_slot=slot,
            notes=notes,
        )
        slot.is_available = False
        slot.save()
        return redirect('booking:session_detail', pk=session.pk)
    return render(request, 'booking/book_session.html', {'lawyers': lawyers})


@login_required
def session_list(request):
    user = request.user
    if hasattr(user, 'lawyer_profile'):
        sessions = BookingSession.objects.filter(lawyer=user).select_related('customer', 'time_slot')
    else:
        sessions = BookingSession.objects.filter(customer=user).select_related('lawyer', 'time_slot')
    return render(request, 'booking/session_list.html', {'sessions': sessions})


@login_required
def session_detail(request, pk):
    session = get_object_or_404(
        BookingSession.objects.select_related('customer', 'lawyer', 'time_slot')
        .prefetch_related('messages__sender'),
        pk=pk,
    )
    if request.user not in (session.customer, session.lawyer):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    return render(request, 'booking/session_detail.html', {'session': session})


@login_required
def send_message(request, pk):
    if request.method != 'POST':
        return redirect('booking:session_detail', pk=pk)
    session = get_object_or_404(BookingSession, pk=pk)
    if request.user not in (session.customer, session.lawyer):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    body = request.POST.get('body', '').strip()
    if body:
        msg = Message.objects.create(session=session, sender=request.user, body=body)
        notify_new_message(session, msg)
    return redirect('booking:session_detail', pk=pk)


@login_required
def lawyer_schedule(request):
    if not request.user.groups.filter(name='level_1').exists():
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    slots = TimeSlot.objects.filter(lawyer=request.user).order_by('date', 'start_time')
    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        TimeSlot.objects.get_or_create(
            lawyer=request.user,
            date=date,
            start_time=start_time,
            defaults={'end_time': end_time},
        )
        return redirect('booking:lawyer_schedule')
    return render(request, 'booking/lawyer_schedule.html', {'slots': slots})


# ── Contact Form ──────────────────────────────────────────────────────���────
def contact_form(request):
    if request.method == 'POST':
        ContactRequest.objects.create(
            name=request.POST.get('name', ''),
            email=request.POST.get('email', ''),
            subject=request.POST.get('subject', ''),
            body=request.POST.get('body', ''),
        )
        return redirect('main:home_view')
    return render(request, 'booking/contact_form.html')



def contact_success(request):
    return render(request, 'booking/contact_success.html')
