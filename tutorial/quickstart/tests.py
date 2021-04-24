from django.test import TestCase
from django.contrib.auth.models import User
from quickstart.models import Follow


class UsersTestCase(TestCase):
    def test_unknown_url(self):
        response = self.client.get('/incorrect')
        self.assertEqual(response.status_code, 404)

    def test_list_users_with_users_username(self):
        User.objects.create(username='Kallor')
        User.objects.create(username='John')
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        usernames = {row['username'] for row in response.json()['results']}
        self.assertEqual(usernames, {'Kallor', 'John'})  # порядок не смотрит
        # self.assertSetEqual(usernames, {'Kallor', 'John'})

    def test_list_users_with_users(self):
        User.objects.create(username='Kallor')
        User.objects.create(username='John')
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    'email': '',
                    'first_name': '',
                    'last_name': '',
                    'url': 'http://testserver/v1/users/John/',
                    'username': 'John'
                },
                {
                    'email': '',
                    'first_name': '',
                    'last_name': '',
                    'url': 'http://testserver/v1/users/Kallor/',
                    'username': 'Kallor'
                }
            ]
        })

    def test_list_users_without_users(self):
        response = self.client.get('/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        })


class FollowTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(username='Karl')
        self.user2 = User.objects.create(username='Pol')
        self.user3 = User.objects.create(username='Mo')
        Follow.objects.create(follower=self.user1, follows=self.user2)

    def test_data_exists(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(Follow.objects.count(), 1)

    def test_new_follow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user3.username}/')
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(Follow.objects.get(
            follower=self.user1,
            follows=self.user3
        ))

    def test_unfollow_correct(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user2.username}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Follow.objects.count(), 0)

    def test_follow_yourself_failed(self):
        self.client.force_login(self.user1)
        response = self.client.post(f'/v1/follow/{self.user1.username}/')
        self.assertEqual(response.status_code, 400)

    def test_unfollow_not_exists_return_fail(self):
        self.client.force_login(self.user1)
        response = self.client.delete(f'/v1/follow/{self.user1.username}/')
        self.assertEqual(response.status_code, 400)

    # def test_follow_dublicate_failed(self):
    #     self.client.force_login(self.user1)
    #     self.assertEqual(Follow.objects.)



# class PutFollowTestCase(TestCase):
#
#     def setUp(self):
#         self.user1 = User.objects.create(username="Leon")
#         self.user2 = User.objects.create(username="Kate")
#
#     def test_simple_add_follow(self):
#         self.assertEqual(Follow.objects.count(), 0)
#         self.client.force_login(self.user1)
#         response = self.client.post(f'/v1/follow/{self.user2.username}/')
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Follow.objects.count(), 1)
#
#     def test_simple_delete_follow(self):
#         self.assertEqual(Follow.objects.count(), 0)
#         self.client.force_login(self.user1)
#         self.client.post(f'/v1/follow/{self.user2.username}/')
#         self.assertEqual(Follow.objects.count(), 1)
#         response = self.client.delete(f'/v1/follow/{self.user2.username}/')
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Follow.objects.count(), 0)
#
#     # def test_add_follow_twice_without_errors(self):
#     #     self.assertEqual(Follow.objects.count(), 0)
#     #     self.client.force_login(self.user1)
#     #     self.assertEqual(self.client.post(f'/v1/follow/{self.user2.username}/').status_code, 201)
#     #     self.assertEqual(Follow.objects.count(), 1)
#     #     self.assertEqual(self.client.post(f'/v1/follow/{self.user2.username}/').status_code, 201)
#     #     self.assertEqual(Follow.objects.count(), 1)
#
#
# class GetUserTestCase(TestCase):
#
#     def setUp(self):
#         self.user = User.objects.create(username="Leon")
#
#     def test_get_existing_user_200(self):
#         response = self.client.get(f'/v1/users/{self.user.username}/')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['username'], self.user.username)
#
#     def test_get_not_existing_user_404(self):
#         self.assertEqual(self.client.get(f'/v1/users/incorrect/').status_code, 404)
#
#
# class GetUsersTestCase(TestCase):
#
#     def setUp(self):
#         self.user1 = User.objects.create(username="Leon")
#         self.user2 = User.objects.create(username="Kate")
#         self.user3 = User.objects.create(username="John")
#
#     def test_get_users_all(self):
#         response = self.client.get(f'/v1/users/')
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(data['count'], 3)
#         self.assertEqual(
#             [r['username'] for r in data['results']],
#             [self.user3.username, self.user2.username, self.user1.username]
#         )
#
#     def test_get_users_page_1(self):
#         response = self.client.get(f'/v1/users/', {'page': 1})
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(data['count'], 3)
#         self.assertEqual(
#             [r['username'] for r in data['results']],
#             [self.user3.username, self.user2.username, self.user1.username]
#         )
#
#     def test_get_users_page_2(self):
#         self.assertEqual(self.client.get(f'/v1/users/', {'page': 2}).status_code, 404)
