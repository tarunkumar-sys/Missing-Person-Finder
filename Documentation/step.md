3. **Activate the virtual environment**
  
     venv\Scripts\activate  

4. **Install dependencies** 


   pip install -r requirements.txt


## Running the Project

1. **Navigate to the core folder**

   cd core

2. **Run the development server**

   python manage.py runserver

3. **Open in browser**


   http://127.0.0.1:8000/

---

## note-

**Check Camera Connection:**   http://127.0.0.1:8000/check-cameras/
**Start Multi-Camera Detection:**   http://127.0.0.1:8000/multi-camera/start/
*output:* multi-camera list page open

**Check Debug Status:**   http://127.0.0.1:8000/debug-detection/ 
*output:*  
{
  "detection_active": true,
  "active_threads": {
    "21": true
  },
  "email_flags": {
    "21": {

    }
  },
  "missing_persons_count": 4,
  "cameras_count": 1,
  "camera_details": [
    {
      "id": 21,
      "name": "Oppo",
      "type": "ip",
      "source": "https://192.0.0.4:8080/video",
      "thread_alive": true
    }
  ]
}





"GET /camera-preview/21/?t=1757151752635 HTTP/1.1" 200 268184
"GET /camera-preview/21/?t=1757151754740 HTTP/1.1" 200 291790
"GET /camera-preview/21/?t=1757151756634 HTTP/1.1" 200 207125
📊 Oppo: Processed 700 frames
📊 Oppo: Processed 800 frames
👤 Oppo: Found 1 faces in frame 820
"GET /detection-status/ HTTP/1.1" 200 75
"GET /all-cameras-preview/ HTTP/1.1" 200 140
"GET /camera-preview/21/?t=1757151800383 HTTP/1.1" 200 162806
"GET /cameras/delete/21/ HTTP/1.1" 200 1371
"POST /cameras/delete/21/ HTTP/1.1" 302 0
"GET /cameras/ HTTP/1.1" 200 14539
"GET /detection-status/ HTTP/1.1" 200 75
"GET /all-cameras-preview/ HTTP/1.1" 200 2
🎉 MATCH FOUND: RDJ rodi on camera: Oppo
📧 Sending email notification...
"GET /detection-status/ HTTP/1.1" 200 75
✅ Email sent successfully to scarycrimson629@gmail.com for RDJ rodi on Oppo
"GET /detection-status/ HTTP/1.1" 200 75
"GET /detection-status/ HTTP/1.1" 200 75
"GET /detection-status/ HTTP/1.1" 200 75
"GET /detection-status/ HTTP/1.1" 200 75
👤 Oppo: Found 1 faces in frame 830
"GET /detection-status/ HTTP/1.1" 200 75
"GET /all-cameras-preview/ HTTP/1.1" 200 2
"GET /detection-status/ HTTP/1.1" 200 75
"GET /detection-status/ HTTP/1.1" 200 75


