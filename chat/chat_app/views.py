from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Organization, OrganizationUser, Message
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

# Create Organization
@csrf_exempt
def create_organization(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            organization_id = data.get('organization_id')
            name = data.get('name')

            if Organization.objects.filter(organization_id=organization_id).exists():
                return JsonResponse({'error': 'Organization ID already exists'}, status=400)

            organization = Organization.objects.create(organization_id=organization_id, name=name)
            return JsonResponse({'message': 'Organization created successfully', 'organization_id': organization.organization_id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

# Delete Organization
@csrf_exempt
def delete_organization(request, organization_id):
    if request.method == 'DELETE':
        organization = get_object_or_404(Organization, organization_id=organization_id)
        organization.delete()
        return JsonResponse({'message': 'Organization deleted successfully'}, status=200)

# Update Organization
@csrf_exempt
def update_organization(request, organization_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            updated_name = data.get('updated_name')

            organization = get_object_or_404(Organization, organization_id=organization_id)
            organization.name = updated_name
            organization.save()

            return JsonResponse({'message': 'Organization updated successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

# Add User to Organization
@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            organization_id = data.get('organization_id')

            organization = get_object_or_404(Organization, organization_id=organization_id)
            user = User.objects.create_user(username=username, password=password)
            OrganizationUser.objects.create(user=user, organization=organization)

            return JsonResponse({'message': 'User added successfully', 'username': username, 'organization': organization.name}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

# Delete User from Organization
@csrf_exempt
def delete_user(request, username, organization_id):
    if request.method == 'DELETE':
        user = get_object_or_404(User, username=username)
        organization = get_object_or_404(Organization, organization_id=organization_id)

        user_org = get_object_or_404(OrganizationUser, user=user, organization=organization)
        user_org.delete()

        return JsonResponse({'message': 'User deleted successfully from the organization'}, status=200)

# Update User in Organization
@csrf_exempt
def update_user(request, username, organization_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            updated_username = data.get('updated_username')
            updated_password = data.get('updated_password')

            user = get_object_or_404(User, username=username)
            organization = get_object_or_404(Organization, organization_id=organization_id)

            if updated_username:
                user.username = updated_username
            if updated_password:
                if len(updated_password) < 6:
                    return JsonResponse({'error': 'Password must be at least 6 characters long'}, status=400)
                user.set_password(updated_password)

            user.save()

            return JsonResponse({'message': 'User updated successfully'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

# Send Message in Group
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("bilal",data)
            organization_id = int(data.get('organization_id'))
            username = data.get('username')
            message_text = data.get('message')

            if not all([organization_id, username, message_text]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            organization = get_object_or_404(Organization, organization_id=organization_id)
            user = get_object_or_404(User, username=username)

            message = Message.objects.create(
                organization=organization,
                user=user,
                message=message_text
            )

            return JsonResponse({'message': 'Message sent successfully', 'message_id': message.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

# Retrieve messages for an organization or user
@csrf_exempt
def get_messages(request):
    if request.method == 'GET':
        organization_id = request.GET.get('organization_id')
        username = request.GET.get('username')

        if organization_id and username:
            messages = Message.objects.filter(organization__organization_id=organization_id, user__username=username)
        elif organization_id:
            messages = Message.objects.filter(organization__organization_id=organization_id)
        elif username:
            messages = Message.objects.filter(user__username=username)
        else:
            messages = Message.objects.all()

        message_list = [
            {
                "id": msg.id,
                "datetime": msg.datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "organization": msg.organization.name,
                "user": msg.user.username,
                "message": msg.message,
            }
            for msg in messages
        ]

        return JsonResponse({"messages": message_list}, status=200)
