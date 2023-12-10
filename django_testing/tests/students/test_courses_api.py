import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_course_retrieve(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.get(f'/api/v1/courses/1/')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course[0].name


@pytest.mark.django_db
def test_get_course_list(client, course_factory):
    course = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert len(data) == len(course)
    for i, m in enumerate(data):
        assert m['name'] == course[i].name


@pytest.mark.django_db
def test_get_course_id(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.get(f'/api/v1/courses/?id={course[0].id}')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(course)
    assert data[0]['id'] == course[0].id


@pytest.mark.django_db
def test_get_course_name(client, course_factory):
    course = course_factory(_quantity=1)
    response = client.get(f'/api/v1/courses/?name={course[0].name}')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(course)
    assert data[0]['name'] == course[0].name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'python'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(_quantity=1)
    data = {'name': 'python'}
    response = client.patch(f'/api/v1/courses/{course[0].pk}/', data=data)
    request = client.get(f'/api/v1/courses/{course[0].pk}/')
    assert request.status_code == 200
    data_request = request.json()
    assert data['name'] == data_request['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)
    count = Course.objects.count()
    response = client.delete(f'/api/v1/courses/{course[0].pk}/')
    request = client.get(f'/api/v1/courses/{course[0].pk}/')
    assert request.status_code == 404
    assert Course.objects.count() == count - 1
