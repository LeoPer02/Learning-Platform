from django.test import TestCase
from users.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from course.models import Course, CourseAdmin

class CourseTests(TestCase):

    def setUp(self):
        # Create users
        self.admin_user = User.objects.create_user(username='adminForTests', password='adminpass', is_staff=True, email='adminForTests@example.com')
        self.course_admin_user = User.objects.create_user(username='courseadminForTests', password='courseadminpass', email='courseadminForTests@example.com')
        self.enrolled_user = User.objects.create_user(username='enrolleduserForTests', password='enrolleduserpass', email='enrolleduserForTests@example.com')
        self.anonymous_client = APIClient()

        # Create tokens for users
        self.admin_token = self.get_jwt_token(self.admin_user)
        self.course_admin_token = self.get_jwt_token(self.course_admin_user)
        self.enrolled_user_token = self.get_jwt_token(self.enrolled_user)

        # Create course
        self.course = Course.objects.create(title='Test Course', visibility='private')
        self.course_public = Course.objects.create(title='Test Course Public', visibility='public')

        # Assign CourseAdmin
        CourseAdmin.objects.create(user=self.course_admin_user, course=self.course, is_admin=True)

        # Enroll user in the course
        self.course.enrolled_users.add(self.enrolled_user)

        # Create API clients
        self.admin_client = APIClient()
        self.course_admin_client = APIClient()
        self.enrolled_user_client = APIClient()

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def tearDown(self):
        # Explicitly delete objects if needed
        CourseAdmin.objects.all().delete()
        Course.objects.all().delete()
        User.objects.all().delete()

    def test_course_list_authenticated(self):
        self.enrolled_user_client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.enrolled_user_token)
        response = self.enrolled_user_client.get('/api/courses/')
        if response.status_code != 200:
            print("test_course_list_authenticated",response.content)
        self.assertEqual(response.status_code, 200)

    def test_course_list_anonymous(self):
        response = self.anonymous_client.get('/api/courses/')
        if response.status_code != 200:
            print("test_course_list_anonymous",response.content)
        self.assertEqual(response.status_code, 200)

    def test_course_detail_authenticated(self):
        self.enrolled_user_client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.enrolled_user_token)
        response = self.enrolled_user_client.get(f'/api/courses/{self.course.id}/')
        if response.status_code != 200:
            print("test_course_detail_authenticated",response.content)
        self.assertEqual(response.status_code, 200)

    def test_course_detail_anonymous(self): ##
        self.assertEqual(self.course.visibility, 'private')
        response = self.anonymous_client.get(f'/api/courses/{self.course.id}/')
        if response.status_code != 403:
            print("test_course_detail_anonymous",response.content)
        self.assertEqual(response.status_code, 403)

    def test_course_detail_anonymous_public(self):
        response = self.anonymous_client.get(f'/api/courses/{self.course_public.id}/')
        if response.status_code != 200:
            print("test_course_detail_anonymous_public",response.content)
        self.assertEqual(response.status_code, 200)

    def test_course_detail_admin(self):##
        self.admin_client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.admin_client.get(f'/api/courses/{self.course.id}/')
        if response.status_code != 200:
            print("test_course_detail_admin",response.content)
        self.assertEqual(response.status_code, 200)

    def test_course_detail_course_admin(self): ## 
        self.course_admin_client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.course_admin_token)
        response = self.course_admin_client.get(f'/api/courses/{self.course.id}/')
        if response.status_code != 200:
            print("test_course_detail_course_admin",response.content)
        self.assertEqual(response.status_code, 200)

    def test_course_admin_user_is_course_admin(self):
        self.assertTrue(CourseAdmin.objects.filter(user=self.course_admin_user, course=self.course, is_admin=True).exists())

    def test_enrolled_user_is_enrolled_in_course(self):
        self.assertIn(self.enrolled_user, self.course.enrolled_users.all())
