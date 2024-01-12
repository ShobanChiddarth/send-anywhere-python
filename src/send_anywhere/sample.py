from selenium import webdriver
from selenium.webdriver.common.by import By



driver = webdriver.Chrome()

html_content = """\
<html>
<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
</head>
<body>
	<blockquote>
		<p>Send Anywhere</p>
		<footer>API Sample</footer>
	</blockquote>
	<form id="sendForm" class="col-sm-6">
		<div class="form-group">
			<label for="">Send</label>
			<input id="fileInput" name="file[]" type="file" class="form-control" multiple/><br/>
			<div id="sendBtn" class="btn btn-default form-control">Send</div><br/><br/>
			<label for="">Key: </label> <span id="key" class="text-success"></span>
		</div>
	</form>
	<form id="receiveForm" class="col-sm-6">
		<div class="form-group">
			<label for="">Receive</label>
			<input id="keyInput" class="form-control" onkeypress="return event.keyCode != 13;"/><br/>
			<div id="receiveBtn" class="btn btn-default form-control">Receive</div><br/><br/>
			<label for="">Status: </label> <span id="status" class="text-success"></span>
		</div>
	</form>

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
	<script type="text/javascript">
		$(document).ready(function () {
			function updateDevice() {
				$.ajax({
					url: 'https://send-anywhere.com/web/v1/device',
					type: 'GET',
					dataType: 'jsonp',
					data: {api_key: "YOUR_API_KEY", profile_name: "username"},
					cache: false
				}).done(function (data) {
				});
			}
			function createKey(files) {
				var params = { file: [] };
				var formData = new FormData();
				for (var i = 0; i < files.length; i++) {
					var file = files[i];
					params.file.push({ name: file.name, size: file.size });
					formData.append("file" + i, file, file.name);
				}
                console.log(params);
                console.warn("---");
                console.log(formData);

				$.ajax({
					url: 'https://send-anywhere.com/web/v1/key',
					type: 'GET',
					data: params,
					dataType: 'jsonp',
					cache: false
				}).done(function (data, textStatus, xhr) {
					$('#key').text(data.key);
					sendFile(data.weblink, formData);
				});
			}

			function sendFile(url, data) {
				$.ajax({
					url: url,
					type: 'POST',
					processData: false,
					contentType: false,
					data: data,
					cache: false
				}).done(function (data) {
				});
			}

			function receiveKey(key) {
				$('#status').text('waiting');
				$.ajax({
					url: 'https://send-anywhere.com/web/v1/key/' + key,
					type: 'GET',
					dataType: 'jsonp',
					timeout: 3000,
					cache: false
				}).done(function (data) {
					receiveFile(data.weblink);
					$('#status').text('done');
				}).fail(function (xhr, textStatus, error) {
					$('#receiveForm .form-group').addClass('has-error');
					$('#status').text('failed').removeClass('text-success').addClass('text-danger');
				});
			}

			function receiveFile(url) {
				$('<iframe />')
					.attr('src', url)
					.hide()
					.appendTo('body');
			}

			$('#sendBtn').click(function (){
				var files = $('#fileInput').prop('files')
				if (files.length > 0) {
					createKey(files);
				}
			});

			$('#receiveBtn').click(function (){
				receiveKey($('#keyInput').val());
			});

			$('#keyInput').keyup(function (e) {
				if(e.keyCode == 13){
					$('#receiveBtn').click();
				}
			});

			$('#keyInput').keydown(function () {
				$('#receiveForm .form-group').removeClass('has-error');
				$('#status').text('').removeClass('text-danger').addClass('text-success');
			});

		    updateDevice();
		})
	</script>
</body>
</html>
"""

driver.get('data:text/html;charset=utf-8,' + html_content)

files_list = [r"C:\Users\Admin\Downloads\Images\profile photo.png",
              r"C:\Users\Admin\Downloads\Images\privateinvestocat.jpg"]

file_input = driver.find_element(By.ID, "fileInput")
file_input.send_keys('\n'.join(files_list))

send_btn = driver.find_element(By.ID, "sendBtn")
send_btn.click()
print(driver.find_element(By.ID, "key"))
