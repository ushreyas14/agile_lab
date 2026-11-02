import pytest
import json


def test_add_student(client):
    response = client.post('/add_student', data={'name': 'Alice'}, follow_redirects=True)
    assert response.status_code == 200

    api_response = client.get('/api/students')
    students = json.loads(api_response.data)
    assert 'Alice' in students


def test_mark_attendance(client):
    client.post('/add_student', data={'name': 'Bob'}, follow_redirects=True)

    response = client.post('/attendance', data={'attendance_Bob': 'present'}, follow_redirects=True)
    assert response.status_code == 200

    api_response = client.get('/api/attendance')
    attendance = json.loads(api_response.data)
    assert len(attendance) > 0

    for day_records in attendance.values():
        assert day_records.get('Bob') == 'present'


def test_get_records(client):
    client.post('/add_student', data={'name': 'Charlie'}, follow_redirects=True)
    client.post('/attendance', data={'attendance_Charlie': 'absent'}, follow_redirects=True)

    response = client.get('/records')
    assert response.status_code == 200
    assert b'Charlie' in response.data


def test_remove_student(client):
    client.post('/add_student', data={'name': 'Dave'}, follow_redirects=True)

    api_before = client.get('/api/students')
    assert b'Dave' in api_before.data

    client.post('/remove_student/Dave', follow_redirects=True)

    api_after = client.get('/api/students')
    students = json.loads(api_after.data)
    assert 'Dave' not in students
