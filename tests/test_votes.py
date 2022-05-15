
from app import models
import pytest

@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Votes(post_id=test_posts[0].id,user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client,test_user,test_posts):
    data = {
        "post_id": test_posts[0].id,
        "dir": 1

    }
    res = authorized_client.post("/vote/", json = data)
    #print(res.json())
    assert res.status_code == 201
    assert res.json()['message'] == 'successfully voted'

def test_vote_twice_post(test_vote,test_posts,authorized_client):
    res = authorized_client.post("/vote/",json ={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 409

def test_vote_delete(authorized_client,test_posts,test_user,test_vote):
    res = authorized_client.post("/vote/",json ={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 201

def test_vote_delete_not_exist(authorized_client,test_posts,test_user,test_vote):
    res = authorized_client.post("/vote/",json ={"post_id": 999, "dir": 0})
    assert res.status_code == 404

def test_vote_not_authenticated(client,test_posts,test_user,test_vote):
    res = client.post("/vote/",json ={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401