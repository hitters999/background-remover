import io
from PIL import Image
from app import app

client = app.test_client()

health = client.get('/api/health')
assert health.status_code == 200, health.data
assert health.get_json()['status'] == 'healthy'

missing = client.post('/api/remove')
assert missing.status_code == 400, missing.data
assert 'No image file' in missing.get_json()['error']

invalid = client.post('/api/remove', data={'image': (io.BytesIO(b'not an image'), 'bad.txt')}, content_type='multipart/form-data')
assert invalid.status_code == 400, invalid.data
assert 'Unsupported image type' in invalid.get_json()['error']

img = Image.new('RGB', (64, 64), (255, 0, 0))
source = io.BytesIO()
img.save(source, format='PNG')
source.seek(0)
valid = client.post('/api/remove', data={'image': (source, 'sample.png')}, content_type='multipart/form-data')
assert valid.status_code == 200, valid.data
assert valid.mimetype == 'image/png'
result = Image.open(io.BytesIO(valid.data))
assert result.format == 'PNG'
assert result.mode == 'RGBA'
print('PASS: health, validation, processing, PNG output, and alpha channel')
