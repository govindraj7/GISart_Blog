
# basic_pgs tests
def test_index_success(client):
  # Page loads
  response = client.get('/')
  assert response.status_code == 200

def test_about_me_redirects(client):
  # Page redirects
  response = client.get('/inspiration')
  assert response.status_code == 302

def test_info_sheet_download(client):
  # Returns legal.txt file
  response = client.get('/download')
  assert response.headers['Content-Disposition'] == 'attachment; filename=info-sheet.txt'