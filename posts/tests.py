from django.test import TestCase , SimpleTestCase,Client
from django.urls import reverse,resolve
from . import views,models,forms
from django.contrib.auth.models import User
from django.contrib import auth

# Create your tests here.
class PostsUrlTests(SimpleTestCase):

    def test_post_list_url_is_resolve(self):
        url = reverse("posts:list")
        self.assertEqual(resolve(url).func,views.posts_list_view)

    def test_post_detail_url_is_resolve(self):
        url = reverse("posts:details",kwargs={"pk":1})
        self.assertEqual(resolve(url).func,views.posts_details_view)

    def test_add_post_url_is_resolve(self):
        url = reverse("posts:add")
        self.assertEqual(resolve(url).func,views.posts_add_view)

    def test_edit_post_url_is_resolve(self):
        url = reverse("posts:edit")
        self.assertEqual(resolve(url).func,views.posts_edit_view)

    def test_delete_url_is_resolve(self):
        url = reverse("posts:delete",kwargs={"pk":1})
        self.assertEqual(resolve(url).func,views.posts_delete_view)
        
class PostsModelsTests(TestCase):
    def setUp(self):
        self.client  = Client()
        self.client.force_login(User.objects.get_or_create(username="testuser")[0])
        self.testPost = models.Post.objects.create(
            title = "test post",
            content = 'testcontent',
            author = auth.get_user(self.client)
        )
        self.test_comment = models.Comment.objects.create(
            content = "testComment",
            comment_for = self.testPost,
            author = auth.get_user(self.client)
        )

    def test_create_slug(self):
        self.assertEqual(self.testPost.slug , "test-post")

    def test_created_object_is_correct(self):
        self.assertEqual(self.testPost.title , "test post")

    def test_comment_created_object_is_correct(self):
        self.assertEqual(self.test_comment.content , "testComment")

class PostsLoggedInViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.force_login(User.objects.update_or_create(username = "testuser")[0])
        self.test_post = models.Post.objects.create(
            title = "test post",
            content = 'testcontent',
            author = auth.get_user(self.client)
        )

    def test_posts_list_view_GET(self):
        response = self.client.get(reverse("posts:list"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"posts/posts_list.html")
    
    def test_posts_details_view_GET(self):
        response = self.client.get(reverse("posts:details",kwargs={"pk" : self.test_post.pk}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"posts/posts_details.html")
    
    def test_posts_details_view_POST(self):
        response = self.client.post(
            reverse("posts:details",kwargs={"pk":self.test_post.pk}),
                data={
                    "content":"testComment",
                    "comment_for":self.test_post,
                    "author":auth.get_user(self.client)
                }
            )
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"posts/posts_details.html")
    
    def test_posts_add_view_GET(self):
        response = self.client.get(reverse("posts:add"))
        self.assertEqual(response.status_code , 200)
        self.assertTemplateUsed(response,"posts/posts_add.html")

    def test_posts_add_view_POST(self):
        response = self.client.post(
            reverse("posts:add"),
            data= {
                "title" : "test post",
                'content' : 'testcontent',
                'author' : auth.get_user(self.client)
            }
        )
        self.assertRedirects(response,reverse("users:info"))

    def test_posts_edit_view_GET(self):
        response = self.client.get(reverse("posts:edit"))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"posts/posts_edit.html")

    def test_posts_edit_view_POST(self):
        response = self.client.post(
            reverse("posts:add"),
            data= {
                "title" : "test post",
                'content' : 'testcontent',
                'target' : self.test_post.pk,
                '_method':"PUT"
            }
        )
        self.assertRedirects(response,reverse("users:info"))

    def test_posts_delete_GET(self):
        response = self.client.get(reverse("posts:delete",kwargs={"pk" : self.test_post.pk}))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response , "posts/posts_delete.html")
    
    def test_posts_delete_POST(self):
        response = self.client.post(
            reverse("posts:delete",kwargs={"pk" : self.test_post.pk}),
            data={"_method":"DELETE",},
            )
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("users:info"))


class PostsLoggedOutViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.update_or_create(username = "testuser")[0]
        self.test_post = models.Post.objects.get_or_create(title = "test post" , author = self.user)[0]

    def test_logged_out_posts_add_view_GET(self):
        response = self.client.get(reverse("posts:add"))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,"/users/login?next=/posts/add/",target_status_code=301)

    def test_logged_out_posts_edit_view_GET(self):
        response = self.client.get(reverse("posts:edit"))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,"/users/login?next=/posts/edit/",target_status_code=301)
    
    def test_logged_out_posts_delete_GET(self):
        response = self.client.get(reverse("posts:delete",kwargs={"pk":1}))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,"/users/login?next=/posts/1/delete",target_status_code=301)

    def test_logged_out_posts_details_POST(self):
        response = self.client.post(
            reverse("posts:details",kwargs={"pk":self.test_post.pk}),
            data={
                "content":"testComment"
            }
        )
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("users:login"))


class PostsFormsTest(SimpleTestCase):

    def test_post_form_with_valid_data(self):
        form = forms.PostForm(
            data={
                "title": "testpost",
                "content":"testcontent",
            }
        )
        self.assertTrue(form.is_valid())

    def test_post_form_with_invalid_data(self):
        form = forms.PostForm(
            data={}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),2)

    def test_comment_form_with_invalid_data(self):
        form = forms.CommentsForm(
            data={
                "content":"testComment",
            }
        )
        self.assertTrue(form.is_valid())


    def test_comment_form_with_invalid_data(self):
        form = forms.CommentsForm(
            data={}
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors),1)