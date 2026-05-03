from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from account.models import LawyerProfile
from booking.models import BookingSession, ContactRequest
from .decorators import manager_required


def _unread_count():
    return ContactRequest.objects.filter(is_read=False).count()


# ── Dashboard ──────────────────────────────────────────────────────────────

@manager_required
def dashboard(request):
    context = {
        'pending_sessions': BookingSession.objects.filter(status='pending').count(),
        'unread_contacts': _unread_count(),
        'total_lawyers': User.objects.filter(lawyer_profile__isnull=False).count(),
        'total_customers': User.objects.filter(lawyer_profile__isnull=True, is_staff=False).count(),
    }
    return render(request, 'managment/dashboard.html', context)


# ── Users & Lawyers ────────────────────────────────────────────────────────

@manager_required
def user_list(request):
    users = User.objects.prefetch_related('groups').order_by('date_joined')
    return render(request, 'managment/user_list.html', {
        'users': users,
        'unread_count': _unread_count(),
    })


@manager_required
def assign_lawyer(request, pk):
    if request.method != 'POST':
        return redirect('managment:user_list')
    user = get_object_or_404(User, pk=pk)
    LawyerProfile.objects.get_or_create(user=user)
    messages.success(request, f'{user.get_full_name() or user.username} has been assigned as a lawyer.')
    return redirect('managment:user_list')


@manager_required
def revoke_lawyer(request, pk):
    if request.method != 'POST':
        return redirect('managment:user_list')
    user = get_object_or_404(User, pk=pk)
    LawyerProfile.objects.filter(user=user).delete()
    messages.warning(request, f'{user.get_full_name() or user.username} lawyer role has been revoked.')
    return redirect('managment:user_list')


# ── Sessions ───────────────────────────────────────────────────────────────

@manager_required
def session_list(request):
    status_filter = request.GET.get('status', '')
    sessions = BookingSession.objects.select_related('customer', 'lawyer', 'time_slot').order_by('-created_at')
    if status_filter:
        sessions = sessions.filter(status=status_filter)
    lawyers = User.objects.filter(lawyer_profile__isnull=False)
    return render(request, 'managment/session_list.html', {
        'sessions': sessions,
        'status_filter': status_filter,
        'status_choices': BookingSession.STATUS_CHOICES,
        'lawyers': lawyers,
        'unread_count': _unread_count(),
    })


@manager_required
def session_detail(request, pk):
    session = get_object_or_404(
        BookingSession.objects.select_related('customer', 'lawyer', 'time_slot')
                              .prefetch_related('messages__sender'),
        pk=pk,
    )
    lawyers = User.objects.filter(lawyer_profile__isnull=False)
    return render(request, 'managment/session_detail.html', {
        'session': session,
        'lawyers': lawyers,
        'status_choices': BookingSession.STATUS_CHOICES,
        'unread_count': _unread_count(),
    })


@manager_required
def update_session_status(request, pk):
    if request.method != 'POST':
        return redirect('managment:session_list')
    session = get_object_or_404(BookingSession, pk=pk)
    new_status = request.POST.get('status')
    valid = [s[0] for s in BookingSession.STATUS_CHOICES]
    if new_status in valid:
        session.status = new_status
        session.save()
        messages.success(request, f'Session #{pk} status updated to {new_status}.')
    return redirect('managment:session_detail', pk=pk)


@manager_required
def reassign_session(request, pk):
    if request.method != 'POST':
        return redirect('managment:session_list')
    session = get_object_or_404(BookingSession, pk=pk)
    new_lawyer_pk = request.POST.get('lawyer_id')
    new_lawyer = get_object_or_404(User, pk=new_lawyer_pk, lawyer_profile__isnull=False)
    session.lawyer = new_lawyer
    session.status = 'rescheduled'
    session.save()
    messages.success(request, f'Session #{pk} reassigned to {new_lawyer.get_full_name()}.')
    return redirect('managment:session_detail', pk=pk)


# ── Blog Posts (depends on Dev A's posts app) ──────────────────────────────

# @manager_required
# def post_list(request):
#     from posts.models import BlogPost
#     posts = BlogPost.objects.select_related('author').order_by('-created_at')
#     return render(request, 'managment/post_list.html', {
#         'posts': posts,
#         'unread_count': _unread_count(),
#     })


# @manager_required
# def toggle_publish(request, pk):
#     if request.method != 'POST':
#         return redirect('managment:post_list')
#     from posts.models import BlogPost
#     post = get_object_or_404(BlogPost, pk=pk)
#     post.is_published = not post.is_published
#     post.save()
#     return redirect('managment:post_list')


# @manager_required
# def delete_post(request, pk):
#     if request.method != 'POST':
#         return redirect('managment:post_list')
#     from posts.models import BlogPost
#     post = get_object_or_404(BlogPost, pk=pk)
#     title = post.title
#     post.delete()
#     messages.warning(request, f'Post "{title}" has been deleted.')
#     return redirect('managment:post_list')


# ── Contact Requests ───────────────────────────────────────────────────────

@manager_required
def contact_requests(request):
    contacts = ContactRequest.objects.order_by('-submitted_at')
    return render(request, 'managment/contact_requests.html', {
        'contacts': contacts,
        'unread_count': _unread_count(),
    })


@manager_required
def mark_contact_read(request, pk):
    if request.method != 'POST':
        return redirect('managment:contact_requests')
    contact = get_object_or_404(ContactRequest, pk=pk)
    contact.is_read = True
    contact.save()
    return redirect('managment:contact_requests')
