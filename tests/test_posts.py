import pytest
from app  import schemas

def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    #print(res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code ==200


def test_unauthorized_user_get_all_posts(client,test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/99999")
    assert res.status_code == 404

def test_get_one_valid_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")    
    first_post= schemas.PostOut(**res.json())
    first_post = list(first_post)
    #print(first_post)
    assert first_post[0][1].id == test_posts[0].id
    assert first_post[0][1].title == test_posts[0].title
    assert first_post[0][1].content == test_posts[0].content
    assert res.status_code ==  200


@pytest.mark.parametrize("title, content, published",[
    ("awesome title", "content for this title", True),
    ("pizza", "I love pepperoni pizza", False),
    ("something", "something something meri jaan", True),
])
def test_create_post(authorized_client,test_user,test_posts,title,content,published):
    res = authorized_client.post("/posts/",  json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client,test_user,test_posts):
    res = authorized_client.post("/posts/", json={"title":test_posts[0].title, "content": test_posts[0].content})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.published == True

def test_unauthorized_user_post_create(client,test_user):
    res = client.post('/posts/', json={"title":"ghjh", "content": "hhgfhn"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client,test_user,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_authorized_user_delete_post(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_non_existing_post(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/99999")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[4].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[4].id

    }
    res = authorized_client.put(f"/posts/{test_posts[4].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404