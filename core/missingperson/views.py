# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse, JsonResponse
# from .models import *
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils import timezone
# from datetime import datetime
# import face_recognition
# import cv2
# import threading
# import time
# import numpy as np
# from django.views.decorators.csrf import csrf_exempt
# import json
# import logging

# # Set up logging
# logger = logging.getLogger(__name__)

# # Global variables for multi-camera processing
# camera_threads = {}
# stop_threads = False
# email_sent_flags = {}  # Track email notifications per camera
# camera_frames = {}  # Store frames for each camera

# def home(request):
#     return render(request, "index.html")

# def detect(request):
#     video_capture = cv2.VideoCapture(0)
#     face_detected_flags = {}
#     while True:
#         ret, frame = video_capture.read()
#         if not ret:
#             break
#         frame = process_frame_and_notify(frame, "Webcam", face_detected_flags)
#         cv2.imshow('Camera Feed', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     video_capture.release()
#     cv2.destroyAllWindows()
#     return render(request, "surveillance.html")

# def surveillance(request):
#     return render(request, "surveillance.html")

# def register(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         father_name = request.POST.get('fathers_name')
#         date_of_birth = request.POST.get('dob')
#         address = request.POST.get('address')
#         phone_number = request.POST.get('phonenum')
#         aadhar_number = request.POST.get('aadhar_number')
#         missing_from = request.POST.get('missing_date')
#         email = request.POST.get('email')
#         image = request.FILES.get('image')
#         gender = request.POST.get('gender')
        
#         aadhar = MissingPerson.objects.filter(aadhar_number=aadhar_number)
#         if aadhar.exists():
#             messages.info(request, 'Aadhar Number already exists')
#             return redirect('/register')
            
#         person = MissingPerson.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             father_name=father_name,
#             date_of_birth=date_of_birth,
#             address=address,
#             phone_number=phone_number,
#             aadhar_number=aadhar_number,
#             missing_from=missing_from,
#             email=email,
#             image=image,
#             gender=gender,
#         )
#         person.save()
#         messages.success(request, 'Case Registered Successfully')
#         current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
#         subject = 'Case Registered Successfully'
#         from_email = 'pptodo01@gmail.com'
#         recipientmail = person.email
#         context = {
#             "first_name": person.first_name,
#             "last_name": person.last_name,
#             'fathers_name': person.father_name,
#             "aadhar_number": person.aadhar_number,
#             "missing_from": person.missing_from,
#             "date_time": current_time
#         }
#         html_message = render_to_string('regmail.html', context=context)
#         send_mail(subject, '', from_email, [recipientmail], fail_silently=False, html_message=html_message)

#     return render(request, "register.html")

# def missing(request):
#     queryset = MissingPerson.objects.all()
#     search_query = request.GET.get('search', '')
#     if search_query:
#         queryset = queryset.filter(aadhar_number__icontains=search_query)
    
#     context = {'missingperson': queryset}
#     return render(request, "missing.html", context)

# def delete_person(request, person_id):
#     person = get_object_or_404(MissingPerson, id=person_id)
#     person.delete()
#     return redirect('missing')

# def update_person(request, person_id):
#     person = get_object_or_404(MissingPerson, id=person_id)

#     if request.method == 'POST':
#         # Retrieve data from the form
#         first_name = request.POST.get('first_name', person.first_name)
#         last_name = request.POST.get('last_name', person.last_name)
#         father_name = request.POST.get('fathers_name', person.father_name)
#         date_of_birth = request.POST.get('dob', person.date_of_birth)
#         address = request.POST.get('address', person.address)
#         email = request.POST.get('email', person.email)
#         phone_number = request.POST.get('phonenum', person.phone_number)
#         aadhar_number = request.POST.get('aadhar_number', person.aadhar_number)
#         missing_from = request.POST.get('missing_date', person.missing_from)
#         gender = request.POST.get('gender', person.gender)

#         # Check if a new image is provided
#         new_image = request.FILES.get('image')
#         if new_image:
#             person.image = new_image

#         # Update the person instance
#         person.first_name = first_name
#         person.last_name = last_name
#         person.father_name = father_name
#         person.date_of_birth = date_of_birth
#         person.address = address
#         person.email = email
#         person.phone_number = phone_number
#         person.aadhar_number = aadhar_number
#         person.missing_from = missing_from
#         person.gender = gender

#         # Save the changes
#         person.save()

#         return redirect('missing')

#     return render(request, 'edit.html', {'person': person})

# def camera_processor(camera):
#     global stop_threads, email_sent_flags, camera_frames

#     cap = cv2.VideoCapture(camera.source)
#     if not cap.isOpened():
#         print(f"Could not open camera {camera.name}")
#         return

#     if camera.id not in email_sent_flags:
#         email_sent_flags[camera.id] = {}

#     while not stop_threads:
#         ret, frame = cap.read()
#         if not ret:
#             continue

#         processed_frame = process_frame_and_notify(frame, camera.name, email_sent_flags[camera.id])

#         ret, jpeg = cv2.imencode('.jpg', processed_frame)
#         if ret:
#             camera_frames[str(camera.id)] = {
#                 'frame': jpeg.tobytes(),
#                 'timestamp': time.time(),
#                 'camera_name': camera.name
#             }
#         time.sleep(0.03)
#     cap.release()

# def camera_list(request):
#     cameras = Camera.objects.filter(is_active=True)
#     return render(request, 'camera_list.html', {
#         'cameras': cameras,
#         'preview_url': '/all-cameras-preview/'
#     })

# def add_camera(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         camera_type = request.POST.get('camera_type')
#         source = request.POST.get('source')
#         description = request.POST.get('description')
        
#         camera = Camera.objects.create(
#             name=name,
#             camera_type=camera_type,
#             source=source,
#             description=description
#         )
#         messages.success(request, 'Camera added successfully')
#         return redirect('camera_list')
    
#     return render(request, 'add_camera.html')

# def edit_camera(request, camera_id):
#     camera = get_object_or_404(Camera, id=camera_id)
    
#     if request.method == 'POST':
#         camera.name = request.POST.get('name')
#         camera.camera_type = request.POST.get('camera_type')
#         camera.source = request.POST.get('source')
#         camera.description = request.POST.get('description')
#         camera.save()
        
#         messages.success(request, 'Camera updated successfully')
#         return redirect('camera_list')
    
#     return render(request, 'edit_camera.html', {'camera': camera})

# def delete_camera(request, camera_id):
#     camera = get_object_or_404(Camera, id=camera_id)
    
#     if request.method == 'POST':
#         camera.is_active = False
#         camera.save()
#         messages.success(request, 'Camera deleted successfully')
#         return redirect('camera_list')
    
#     return render(request, 'delete_camera.html', {'camera': camera})

# def start_multi_camera_detection(request):
#     global camera_threads, stop_threads, email_sent_flags
    
#     logger.info("Starting multi-camera detection")
    
#     stop_threads = False
#     email_sent_flags = {}  # Reset email flags
    
#     cameras = Camera.objects.filter(is_active=True)
    
#     if not cameras:
#         messages.warning(request, 'No active cameras found. Please add cameras first.')
#         return redirect('camera_list')
    
#     # Stop any existing threads
#     for camera_id, thread in camera_threads.items():
#         if thread.is_alive():
#             stop_threads = True
#             thread.join(timeout=2.0)
    
#     camera_threads = {}
#     stop_threads = False
    
#     # Start new threads for each camera
#     for camera in cameras:
#         thread = threading.Thread(
#             target=camera_processor, 
#             args=(camera,),
#             daemon=True
#         )
#         camera_threads[camera.id] = thread
#         thread.start()
#         logger.info(f"Started detection thread for camera: {camera.name} (ID: {camera.id})")
    
#     messages.success(request, f'Started detection on {len(cameras)} cameras')
#     logger.info(f"Detection started on {len(cameras)} cameras")
#     return render(request, 'multi_camera_detection.html', {'cameras': cameras})

# def stop_multi_camera_detection(request):
#     global stop_threads, camera_threads
    
#     stop_threads = True
    
#     # Wait for all threads to finish
#     for camera_id, thread in camera_threads.items():
#         if thread.is_alive():
#             thread.join(timeout=2.0)
    
#     camera_threads = {}
#     messages.success(request, 'Stopped all camera detection')
#     logger.info("Stopped all camera detection")
#     return redirect('camera_list')

# def camera_preview(request, camera_id):
#     """Generate preview frames from camera"""
#     camera = get_object_or_404(Camera, id=camera_id)
    
#     try:
#         if camera.camera_type == 'webcam':
#             cap = cv2.VideoCapture(int(camera.source))
#         else:
#             cap = cv2.VideoCapture(camera.source)
        
#         if not cap.isOpened():
#             return HttpResponse(status=404)
        
#         # Set camera properties for better performance
#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
#         cap.set(cv2.CAP_PROP_FPS, 10)
        
#         ret, frame = cap.read()
#         cap.release()
        
#         if ret:
#             # Convert frame to JPEG
#             ret, jpeg = cv2.imencode('.jpg', frame)
            
#             if ret:
#                 return HttpResponse(jpeg.tobytes(), content_type='image/jpeg')
        
#         return HttpResponse(status=404)
    
#     except Exception as e:
#         logger.error(f"Camera preview error: {str(e)}")
#         return HttpResponse(status=500)

# def all_cameras_preview(request):
#     """Check status of all cameras and return their preview URLs"""
#     cameras = Camera.objects.filter(is_active=True)
#     camera_status = {}
    
#     for camera in cameras:
#         try:
#             if camera.camera_type == 'webcam':
#                 cap = cv2.VideoCapture(int(camera.source))
#             else:
#                 cap = cv2.VideoCapture(camera.source)
            
#             if cap.isOpened():
#                 camera_status[camera.id] = {
#                     'name': camera.name,
#                     'type': camera.get_camera_type_display(),
#                     'source': camera.source,
#                     'status': 'connected',
#                     'url': f'/camera-preview/{camera.id}/'
#                 }
#                 cap.release()
#             else:
#                 camera_status[camera.id] = {
#                     'name': camera.name,
#                     'type': camera.get_camera_type_display(),
#                     'source': camera.source,
#                     'status': 'disconnected',
#                     'error': 'Could not open camera'
#                 }
                
#         except Exception as e:
#             camera_status[camera.id] = {
#                 'name': camera.name,
#                 'type': camera.get_camera_type_display(),
#                 'source': camera.source,
#                 'status': 'error',
#                 'error': str(e)
#             }
    
#     return JsonResponse(camera_status)

# @csrf_exempt
# def detection_status(request):
#     """Check if detection is running and get status"""
#     global camera_threads
#     active_threads = {cam_id: thread.is_alive() for cam_id, thread in camera_threads.items()}
#     return JsonResponse({
#         'detection_running': any(active_threads.values()),
#         'active_cameras': list(active_threads.keys()),
#         'status': active_threads
#     })

# def test_detection(request):
#     """Test if face detection is working"""
#     # Test with a sample image
#     test_person = MissingPerson.objects.first()
#     if test_person:
#         try:
#             image = face_recognition.load_image_file(test_person.image.path)
#             encodings = face_recognition.face_encodings(image)
#             if encodings:
#                 return HttpResponse(f"Detection working! Loaded encoding for {test_person.first_name}")
#             else:
#                 return HttpResponse("No face found in test image")
#         except Exception as e:
#             return HttpResponse(f"Error: {str(e)}")
#     return HttpResponse("No test person available")

# def check_cameras(request):
#     """Check if cameras are accessible"""
#     cameras = Camera.objects.filter(is_active=True)
#     results = []
    
#     for camera in cameras:
#         try:
#             if camera.camera_type == 'webcam':
#                 cap = cv2.VideoCapture(int(camera.source))
#             else:
#                 cap = cv2.VideoCapture(camera.source)
            
#             if cap.isOpened():
#                 ret, frame = cap.read()
#                 if ret:
#                     results.append(f"{camera.name}: OK (Frame captured)")
#                 else:
#                     results.append(f"{camera.name}: Error (No frame)")
#                 cap.release()
#             else:
#                 results.append(f"{camera.name}: Error (Cannot open)")
#         except Exception as e:
#             results.append(f"{camera.name}: Exception ({str(e)})")
    
#     return HttpResponse("<br>".join(results))
# def process_frame_and_notify(frame, camera_name, email_sent_flags):
#     """
#     Detect faces in the frame, compare with missing persons, 
#     send notification if found, and draw rectangles.
#     """
#     print("Running detection on frame from", camera_name)
#     face_locations = face_recognition.face_locations(frame)
#     face_encodings = face_recognition.face_encodings(frame, face_locations)
#     face_detected = False

#     for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
#         for person in MissingPerson.objects.all():
#             stored_image = face_recognition.load_image_file(person.image.path)
#             stored_encodings = face_recognition.face_encodings(stored_image)
#             if not stored_encodings:
#                 print(f"No face found in image for {person.first_name}")
#                 continue
#             stored_face_encoding = stored_encodings[0]
#             matches = face_recognition.compare_faces([stored_face_encoding], face_encoding)
#             if any(matches):
#                 name = person.first_name + " " + person.last_name
#                 cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#                 font = cv2.FONT_HERSHEY_DUPLEX
#                 cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#                 # Notification logic
#                 if not email_sent_flags.get(person.id, False):
#                     print(f"Hi {name} is found on camera: {camera_name}")
#                     current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
#                     subject = 'Missing Person Found'
#                     from_email = 'pptodo01@gmail.com'
#                     recipientmail = person.email
#                     context = {
#                         "first_name": person.first_name,
#                         "last_name": person.last_name,
#                         'fathers_name': person.father_name,
#                         "aadhar_number": person.aadhar_number,
#                         "missing_from": person.missing_from,
#                         "date_time": current_time,
#                         "location": camera_name
#                     }
#                     html_message = render_to_string('findemail.html', context=context)
#                     send_mail(subject, '', from_email, [recipientmail], fail_silently=False, html_message=html_message)
#                     email_sent_flags[person.id] = True
#                 face_detected = True
#                 break
#         if not face_detected:
#             name = "Unknown"
#             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#             font = cv2.FONT_HERSHEY_DUPLEX
#             cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#     return frame


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime
import face_recognition
import cv2
import threading
import time
import numpy as np
from django.views.decorators.csrf import csrf_exempt
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Global variables for multi-camera processing
camera_threads = {}
stop_threads = False
email_sent_flags = {}  # Track email notifications per camera
detection_active = False  # Track if detection is active

def home(request):
    return render(request, "index.html")

def detect(request):
    video_capture = cv2.VideoCapture(0)
    
    # Initialize a flag to track if a face has been detected in the current video stream
    face_detected = False
    
    while True:
        ret, frame = video_capture.read()
        
        # Find face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        
        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            # Compare detected face with stored face images
            for person in MissingPerson.objects.all():
                stored_image = face_recognition.load_image_file(person.image.path)
                stored_face_encoding = face_recognition.face_encodings(stored_image)[0]

                # Compare face encodings using a tolerance value
                matches = face_recognition.compare_faces([stored_face_encoding], face_encoding)

                if any(matches):
                    name = person.first_name + " " + person.last_name
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                    # Check if a face has already been detected in this video stream
                    if not face_detected:
                        print("Hi " + name + " is found")
                        
                        current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
                        subject = 'Missing Person Found'
                        from_email = 'pptodo01@gmail.com'
                        recipientmail = person.email
                        
                        context = {
                            "first_name": person.first_name,
                            "last_name": person.last_name,
                            'fathers_name': person.father_name,
                            "aadhar_number": person.aadhar_number,
                            "missing_from": person.missing_from,
                            "date_time": current_time,
                            "location": "India"
                        }
                        
                        html_message = render_to_string('findemail.html', context=context)
                        send_mail(subject, '', from_email, [recipientmail], fail_silently=False, html_message=html_message)
                        face_detected = True  # Set the flag to True to indicate a face has been detected
                        break  # Break the loop once a match is found

            # Check if no face was detected in the current frame
            if not face_detected:
                name = "Unknown"
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Camera Feed', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    video_capture.release()
    cv2.destroyAllWindows()
    return render(request, "surveillance.html")

def surveillance(request):
    return render(request, "surveillance.html")

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        father_name = request.POST.get('fathers_name')
        date_of_birth = request.POST.get('dob')
        address = request.POST.get('address')
        phone_number = request.POST.get('phonenum')
        aadhar_number = request.POST.get('aadhar_number')
        missing_from = request.POST.get('missing_date')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        gender = request.POST.get('gender')
        
        aadhar = MissingPerson.objects.filter(aadhar_number=aadhar_number)
        if aadhar.exists():
            messages.info(request, 'Aadhar Number already exists')
            return redirect('/register')
            
        person = MissingPerson.objects.create(
            first_name=first_name,
            last_name=last_name,
            father_name=father_name,
            date_of_birth=date_of_birth,
            address=address,
            phone_number=phone_number,
            aadhar_number=aadhar_number,
            missing_from=missing_from,
            email=email,
            image=image,
            gender=gender,
        )
        person.save()
        messages.success(request, 'Case Registered Successfully')
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
        subject = 'Case Registered Successfully'
        from_email = 'pptodo01@gmail.com'
        recipientmail = person.email
        context = {
            "first_name": person.first_name,
            "last_name": person.last_name,
            'fathers_name': person.father_name,
            "aadhar_number": person.aadhar_number,
            "missing_from": person.missing_from,
            "date_time": current_time
        }
        html_message = render_to_string('regmail.html', context=context)
        send_mail(subject, '', from_email, [recipientmail], fail_silently=False, html_message=html_message)

    return render(request, "register.html")

def missing(request):
    queryset = MissingPerson.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(aadhar_number__icontains=search_query)
    
    context = {'missingperson': queryset}
    return render(request, "missing.html", context)

def delete_person(request, person_id):
    person = get_object_or_404(MissingPerson, id=person_id)
    person.delete()
    return redirect('missing')

def update_person(request, person_id):
    person = get_object_or_404(MissingPerson, id=person_id)

    if request.method == 'POST':
        # Retrieve data from the form
        first_name = request.POST.get('first_name', person.first_name)
        last_name = request.POST.get('last_name', person.last_name)
        father_name = request.POST.get('fathers_name', person.father_name)
        date_of_birth = request.POST.get('dob', person.date_of_birth)
        address = request.POST.get('address', person.address)
        email = request.POST.get('email', person.email)
        phone_number = request.POST.get('phonenum', person.phone_number)
        aadhar_number = request.POST.get('aadhar_number', person.aadhar_number)
        missing_from = request.POST.get('missing_date', person.missing_from)
        gender = request.POST.get('gender', person.gender)

        # Check if a new image is provided
        new_image = request.FILES.get('image')
        if new_image:
            person.image = new_image

        # Update the person instance
        person.first_name = first_name
        person.last_name = last_name
        person.father_name = father_name
        person.date_of_birth = date_of_birth
        person.address = address
        person.email = email
        person.phone_number = phone_number
        person.aadhar_number = aadhar_number
        person.missing_from = missing_from
        person.gender = gender

        # Save the changes
        person.save()

        return redirect('missing')

    return render(request, 'edit.html', {'person': person})

def camera_processor(camera):
    """Process a single camera stream for face detection"""
    global stop_threads, email_sent_flags
    
    print(f"Starting camera processor for: {camera.name} (ID: {camera.id})")
    
    try:
        # Initialize camera capture
        if camera.camera_type == 'webcam':
            cap = cv2.VideoCapture(int(camera.source))
            print(f"Opening webcam with index: {camera.source}")
        else:
            cap = cv2.VideoCapture(camera.source)
            print(f"Opening camera with source: {camera.source}")
        
        if not cap.isOpened():
            print(f"Error: Could not open camera {camera.name}")
            return
        
        print(f"Successfully opened camera: {camera.name}")
        
        # Initialize email flags for this camera
        if camera.id not in email_sent_flags:
            email_sent_flags[camera.id] = {}
        
        # Load all missing person encodings
        missing_persons = MissingPerson.objects.all()
        known_face_encodings = []
        known_face_names = []
        
        print(f"Loading {missing_persons.count()} missing persons for recognition")
        
        for person in missing_persons:
            try:
                image = face_recognition.load_image_file(person.image.path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    encoding = encodings[0]
                    known_face_encodings.append(encoding)
                    known_face_names.append(f"{person.first_name} {person.last_name}")
                    print(f"Loaded encoding for: {person.first_name} {person.last_name}")
                else:
                    print(f"No face found in image for: {person.first_name} {person.last_name}")
            except Exception as e:
                print(f"Error loading image for {person.first_name}: {str(e)}")
                continue
        
        print(f"Loaded {len(known_face_encodings)} face encodings")
        
        frame_count = 0
        # Main processing loop
        while not stop_threads:
            ret, frame = cap.read()
            if not ret:
                print(f"Error: Could not read frame from {camera.name}")
                time.sleep(2)
                continue
            
            frame_count += 1
            
            # Process every 5th frame to reduce CPU load
            if frame_count % 5 != 0:
                time.sleep(0.01)
                continue
            
            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]  # BGR to RGB
            
            # Find all faces in the current frame
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            if face_locations:
                print(f"Found {len(face_locations)} faces in frame from {camera.name}")
            
            face_names = []
            for face_encoding in face_encodings:
                # See if the face matches any known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                
                # Use the known face with the smallest distance to the new face
                if known_face_encodings:  # Check if list is not empty
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                
                face_names.append(name)
            
            # Process the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame was scaled down
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                if name != "Unknown":
                    print(f"MATCH FOUND: {name} on camera: {camera.name}")
                    print(f"Hi {name} is found on camera: {camera.name}")
                    
                    # Find the person in database
                    try:
                        first_name, last_name = name.split(' ', 1)
                        person = MissingPerson.objects.get(
                            first_name=first_name, 
                            last_name=last_name
                        )
                        
                        # Check if we've already sent a notification for this person on this camera
                        if not email_sent_flags[camera.id].get(person.id, False):
                            print(f"Sending email notification for: {name}")
                            
                            current_time = datetime.now().strftime('%d-%m-%Y %H:%M')
                            subject = 'Missing Person Found'
                            from_email = 'pptodo01@gmail.com'
                            recipientmail = person.email
                            
                            context = {
                                "first_name": person.first_name,
                                "last_name": person.last_name,
                                'fathers_name': person.father_name,
                                "aadhar_number": person.aadhar_number,
                                "missing_from": person.missing_from,
                                "date_time": current_time,
                                "location": camera.name
                            }
                            
                            html_message = render_to_string('findemail.html', context=context)
                            send_mail(subject, '', from_email, [recipientmail], 
                                     fail_silently=False, html_message=html_message)
                            
                            # Update the flag
                            email_sent_flags[camera.id][person.id] = True
                            
                            # Create a location record
                            Location.objects.create(
                                missing_person=person,
                                latitude=0,
                                longitude=0,
                                detected_at=timezone.now(),
                                camera=camera.name
                            )
                    except Exception as e:
                        print(f"Error processing person {name}: {str(e)}")
            
            # Add a small delay to prevent overloading
            time.sleep(0.03)
            
        cap.release()
        print(f"Stopped processing camera: {camera.name}")
        
    except Exception as e:
        print(f"Error processing camera {camera.name}: {str(e)}")
        import traceback
        print(traceback.format_exc())

def camera_list(request):
    cameras = Camera.objects.filter(is_active=True)
    return render(request, 'camera_list.html', {
        'cameras': cameras,
        'preview_url': '/all-cameras-preview/'
    })

def add_camera(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        camera_type = request.POST.get('camera_type')
        source = request.POST.get('source')
        description = request.POST.get('description')
        
        camera = Camera.objects.create(
            name=name,
            camera_type=camera_type,
            source=source,
            description=description
        )
        messages.success(request, 'Camera added successfully')
        return redirect('camera_list')
    
    return render(request, 'add_camera.html')

def edit_camera(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    
    if request.method == 'POST':
        camera.name = request.POST.get('name')
        camera.camera_type = request.POST.get('camera_type')
        camera.source = request.POST.get('source')
        camera.description = request.POST.get('description')
        camera.save()
        
        messages.success(request, 'Camera updated successfully')
        return redirect('camera_list')
    
    return render(request, 'edit_camera.html', {'camera': camera})

def delete_camera(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    
    if request.method == 'POST':
        camera.is_active = False
        camera.save()
        messages.success(request, 'Camera deleted successfully')
        return redirect('camera_list')
    
    return render(request, 'delete_camera.html', {'camera': camera})

def start_multi_camera_detection(request):
    global camera_threads, stop_threads, email_sent_flags, detection_active
    
    print("Starting multi-camera detection")
    
    stop_threads = False
    email_sent_flags = {}  # Reset email flags
    detection_active = True
    
    cameras = Camera.objects.filter(is_active=True)
    
    if not cameras:
        messages.warning(request, 'No active cameras found. Please add cameras first.')
        return redirect('camera_list')
    
    # Stop any existing threads
    for camera_id, thread in camera_threads.items():
        if thread.is_alive():
            stop_threads = True
            thread.join(timeout=2.0)
    
    camera_threads = {}
    stop_threads = False
    
    # Start new threads for each camera
    for camera in cameras:
        thread = threading.Thread(
            target=camera_processor, 
            args=(camera,),
            daemon=True
        )
        camera_threads[camera.id] = thread
        thread.start()
        print(f"Started detection thread for camera: {camera.name} (ID: {camera.id})")
    
    messages.success(request, f'Started detection on {len(cameras)} cameras')
    print(f"Detection started on {len(cameras)} cameras")
    return render(request, 'multi_camera_detection.html', {'cameras': cameras})

def stop_multi_camera_detection(request):
    global stop_threads, camera_threads, detection_active
    
    stop_threads = True
    detection_active = False
    
    # Wait for all threads to finish
    for camera_id, thread in camera_threads.items():
        if thread.is_alive():
            thread.join(timeout=2.0)
    
    camera_threads = {}
    messages.success(request, 'Stopped all camera detection')
    print("Stopped all camera detection")
    return redirect('camera_list')

def camera_preview(request, camera_id):
    """Generate preview frames from camera"""
    camera = get_object_or_404(Camera, id=camera_id)
    
    try:
        if camera.camera_type == 'webcam':
            cap = cv2.VideoCapture(int(camera.source))
        else:
            cap = cv2.VideoCapture(camera.source)
        
        if not cap.isOpened():
            return HttpResponse(status=404)
        
        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        cap.set(cv2.CAP_PROP_FPS, 10)
        
        ret, frame = cap.read()
        cap.release()
        
        if ret:
            # Convert frame to JPEG
            ret, jpeg = cv2.imencode('.jpg', frame)
            
            if ret:
                return HttpResponse(jpeg.tobytes(), content_type='image/jpeg')
        
        return HttpResponse(status=404)
    
    except Exception as e:
        print(f"Camera preview error: {str(e)}")
        return HttpResponse(status=500)

def all_cameras_preview(request):
    """Check status of all cameras and return their preview URLs"""
    cameras = Camera.objects.filter(is_active=True)
    camera_status = {}
    
    for camera in cameras:
        try:
            if camera.camera_type == 'webcam':
                cap = cv2.VideoCapture(int(camera.source))
            else:
                cap = cv2.VideoCapture(camera.source)
            
            if cap.isOpened():
                camera_status[camera.id] = {
                    'name': camera.name,
                    'type': camera.get_camera_type_display(),
                    'source': camera.source,
                    'status': 'connected',
                    'url': f'/camera-preview/{camera.id}/'
                }
                cap.release()
            else:
                camera_status[camera.id] = {
                    'name': camera.name,
                    'type': camera.get_camera_type_display(),
                    'source': camera.source,
                    'status': 'disconnected',
                    'error': 'Could not open camera'
                }
                
        except Exception as e:
            camera_status[camera.id] = {
                'name': camera.name,
                'type': camera.get_camera_type_display(),
                'source': camera.source,
                'status': 'error',
                'error': str(e)
            }
    
    return JsonResponse(camera_status)

@csrf_exempt
def detection_status(request):
    """Check if detection is running and get status"""
    global camera_threads, detection_active
    active_threads = {cam_id: thread.is_alive() for cam_id, thread in camera_threads.items()}
    return JsonResponse({
        'detection_running': detection_active and any(active_threads.values()),
        'active_cameras': list(active_threads.keys()),
        'status': active_threads
    })

def test_detection(request):
    """Test if face detection is working"""
    # Test with a sample image
    test_person = MissingPerson.objects.first()
    if test_person:
        try:
            image = face_recognition.load_image_file(test_person.image.path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                return HttpResponse(f"Detection working! Loaded encoding for {test_person.first_name}")
            else:
                return HttpResponse("No face found in test image")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    return HttpResponse("No test person available")

def check_cameras(request):
    """Check if cameras are accessible"""
    cameras = Camera.objects.filter(is_active=True)
    results = []
    
    for camera in cameras:
        try:
            if camera.camera_type == 'webcam':
                cap = cv2.VideoCapture(int(camera.source))
            else:
                cap = cv2.VideoCapture(camera.source)
            
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    results.append(f"{camera.name}: OK (Frame captured)")
                else:
                    results.append(f"{camera.name}: Error (No frame)")
                cap.release()
            else:
                results.append(f"{camera.name}: Error (Cannot open)")
        except Exception as e:
            results.append(f"{camera.name}: Exception ({str(e)})")
    
    return HttpResponse("<br>".join(results))