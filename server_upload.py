import requests

files = { 'file': open('data.csv', 'rb') }
data = {
	'fieldType': 'compressed',
}
r = requests.post('http://localhost:8080/csv/upload', files = files, data = data)
print r