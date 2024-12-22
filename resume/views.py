from django.http import HttpResponse
from django.shortcuts import render 

# def homepage(request):
#     # return HttpResponse("Hello World! I'm Home.")
#     return render(request, 'home.html')

def about(request):
    # return HTTPResponse("My about Page")
    return render(request, 'about.html')

def contact(request):
    # return HTTPResponse("My about Page")
    return render(request, 'contact.html')

def journal(request):
    # return HTTPResponse("My about Page")
    return render(request, 'journal.html')

def project(request):
    # return HTTPResponse("My about Page")
    return render(request, 'project.html')

def skill(request):
    # return HTTPResponse("My about Page")
    return render(request, 'skill.html')

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES_FILE = os.path.join(BASE_DIR, 'static', 'data', 'notes.json')
IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'data', 'images')

# Ensure directories exist
os.makedirs(IMAGES_DIR, exist_ok=True)
if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "w") as f:
        json.dump([], f)

# Read notes from file
def read_notes():
    try:
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If the file is corrupted, return an empty list and log the issue
        print("Error: notes.json contains invalid JSON. Resetting to empty.")
        return []

# Write notes to file
def write_notes(data):
    with open(NOTES_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_notes(request):
    try:
        category = request.GET.get('category', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)

        notes = read_notes()

        # Filter by category if provided
        if category:
            notes = [note for note in notes if note['category'] == category]

        # Filter by date range if provided
        if start_date:
            start_date = datetime.datetime.fromisoformat(start_date)
            notes = [note for note in notes if datetime.datetime.fromisoformat(note['timestamp'].replace('Z', '')).replace(tzinfo=None) >= start_date]
        if end_date:
            end_date = datetime.datetime.fromisoformat(end_date)
            notes = [note for note in notes if datetime.datetime.fromisoformat(note['timestamp'].replace('Z', '')).replace(tzinfo=None) <= end_date]

        # Sort by pinned first, then latest to oldest
        notes.sort(key=lambda x: (-x.get('pinned', 0), x['timestamp']), reverse=True)

        return JsonResponse(notes, safe=False)
    except Exception as e:
        print(f"Error in get_notes: {e}")
        return JsonResponse({"error": "Failed to retrieve notes."}, status=500)



@csrf_exempt
def save_note(request):
    if request.method == "POST":
        try:
            notes = read_notes()
            new_note = json.loads(request.body)

            # Ensure consistent UTC timestamp
            new_note['timestamp'] = datetime.datetime.utcnow().isoformat() + 'Z'
            new_note['pinned'] = new_note.get('pinned', 0)  # Default to not pinned

            notes.append(new_note)
            write_notes(notes)
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(f"Error in save_note: {e}")
            return JsonResponse({"error": "Failed to save note."}, status=500)


@csrf_exempt
def edit_note(request):
    if request.method == "POST":
        try:
            notes = read_notes()
            updated_note = json.loads(request.body)

            for note in notes:
                if note["id"] == updated_note["id"]:
                    # Update the note's fields
                    note.update(updated_note)
                    # Ensure timestamp is updated in UTC
                    note['timestamp'] = datetime.datetime.utcnow().isoformat() + 'Z'
                    break

            write_notes(notes)
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(f"Error in edit_note: {e}")
            return JsonResponse({"error": "Failed to edit note."}, status=500)



# API to upload an image
@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        if not image:
            return JsonResponse({"status": "error", "message": "No image provided."})
        
        image_name = image.name
        image_path = os.path.join(IMAGES_DIR, image_name)
        
        with open(image_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        
        image_url = f"/static/data/images/{image_name}"
        return JsonResponse({"status": "success", "url": image_url})
        
@csrf_exempt
def delete_note(request):
    if request.method == "POST":
        try:
            notes = read_notes()
            data = json.loads(request.body)
            note_id = data.get("id")
            notes = [note for note in notes if note["id"] != note_id]
            write_notes(notes)
            return JsonResponse({"status": "success"})
        except Exception as e:
            print(f"Error in delete_note: {e}")
            return JsonResponse({"error": "Failed to delete note."}, status=500)



