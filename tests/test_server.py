import uuid
import pytest

import jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.testclient import TestClient
from psycopg2.errors import lookup

from config.settings import app_settings
from db.users import UsersRepo
from db.models import User
from db.words_repo import WordsRepo
from src.server.server import app, login
from src.server.contracts import Token
from src.word import word_client

client = TestClient(app)


def test_register_happy_path(mocker) -> None:  # type: ignore
    mocker_value = User(
        user_id=uuid.UUID(
            '74f3cde6-0c2d-4222-8b60-6ede5d0a661a'
        ),  # type: ignore
        user_name='Andrei',
        password_hash='\x243262243132245249776858453350637a4c714'
        '643633446726f4945654849355a6a793664393543'
        '58464467796e4e78557863774b545a4338317632',
    )

    mocker.patch.object(Session, "add", return_value=mocker_value)

    response = client.post(
        "/register", json={'user_name': 'Andrei', 'user_password': 'Hihi'}
    )
    assert response.status_code == 200
    assert response.json().get('token') is not None


def test_authorization_happy_path(mocker) -> None:  # type: ignore
    encoded_jwt = jwt.encode(
        {
            'user_id': '74f3cde6-0c2d-4222-8b60-6ede5d0a661a',
            'user_name': 'Andrei',
        },
        app_settings.secret_key,
        algorithm='HS256',
    )
    mocker_value = Token(token=encoded_jwt)
    mocker.patch.object(UsersRepo, "login_user", return_value=mocker_value)

    response = client.post(
        "/auth", json={'user_name': 'Andrei', 'user_password': 'Hihi'}
    )
    assert response.status_code == 200
    assert response.json() == {'token': encoded_jwt}


def test_register_account_already_exists(mocker) -> None:  # type: ignore
    mocker.patch.object(
        Session,
        "add",
        side_effect=IntegrityError(
            statement='INSERT INTO users (user_id, user_name, password_hash) '
            'VALUES (%(user_id)s::UUID, %(user_name)s, %(password_hash)s) )',
            orig=lookup('23505'),  # type: ignore
            params={
                'user_id': uuid.UUID('1b91138a-5de7-4c78-97fa-7d8d8ad5e595'),
                'user_name': 'Andrei',
                'password_hash': b'$2b$12$i6aWPnv1c8HbmJmBWxxHi.'
                b'kVNGkJBRw2asaSjWwObsJ4ECLik4MBe',
            },
        ),
    )
    response = client.post(
        "/register", json={'user_name': 'Andrei', 'user_password': 'Hihi'}
    )
    assert response.status_code == 409
    assert response.json() == {'detail': 'Account already exists'}


def test_get_world():  # type: ignore
    word = word_client.get_word()
    assert isinstance(word, str)
    assert len(word) > 1


@pytest.mark.parametrize(
    'word, translate_word',
    [('dog', 'собака'), ('cat', 'кот'), ('box', 'коробка')],
)
def test_translate(word, translate_word):  # type: ignore
    translate = word_client.translate_word(word)
    assert translate.lower() == translate_word.lower()


@pytest.mark.parametrize(
    'target_word, word',
    [('собака', 'собака'), ('код', 'кот'), ('коробки', 'коробка')],
)  # type: ignore
def test_assert_word_true(target_word, word):
    assert word_client.assert_word(target_word, word)


@pytest.mark.parametrize(
    'target_word, word',
    [('собака', 'кот'), ('кот', 'собака'), ('кобра', 'коробка')],
)
def test_assert_word_false(target_word, word):  # type: ignore
    assert not word_client.assert_word(target_word, word)


def test_login_happy_path():  # type: ignore
    return_value = {
        "user_name": "Andrei",
        "user_id": "4697eed7-8193-4249-b139-96af6b22417a",
    }
    assert (
        login(
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ"
            "9.eyJ1c2VyX2lkIjoiNDY5N2VlZDctODE5M"
            "y00MjQ5LWIxMzktOTZhZjZiMjI0MTdhIiwi"
            "dXNlcl9uYW1lIjoiQW5kcmVpIn0.B1tec9Y"
            "E-ayxwhWvG5fqapc5k7KVNMm5NoY6IF3_Inc"
        )
        == return_value
    )


@pytest.mark.parametrize('token', ['a', '1', None])
def test_login_bad_token(token):  # type: ignore
    assert login(token) is None


@pytest.mark.parametrize('token', ['a', '1', 'hello'])
def test_get_word_unauthorized(token):  # type: ignore
    response = client.get("/word", headers={'token': token})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect token'}


@pytest.mark.parametrize('token', ['a', '1', 'hello'])
def test_post_word_unauthorized(token):  # type: ignore
    response = client.post(
        "/word", headers={'token': token}, json={'translation': 'кот'}
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect token'}


def test_get_word(mocker):  # type: ignore
    mocker.patch.object(WordsRepo, "add_word", return_value=None)
    mocker.patch.object(WordsRepo, "add_last_word", return_value=None)
    response = client.get(
        "/word",
        headers={
            'token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ"
            "9.eyJ1c2VyX2lkIjoiNDY5N2VlZDctODE5M"
            "y00MjQ5LWIxMzktOTZhZjZiMjI0MTdhIiwi"
            "dXNlcl9uYW1lIjoiQW5kcmVpIn0.B1tec9Y"
            "E-ayxwhWvG5fqapc5k7KVNMm5NoY6IF3_Inc"
        },
    )
    assert response.status_code == 200
    assert 'word' in response.json()


def test_post_word(mocker):  # type: ignore
    mocker.patch.object(
        WordsRepo,
        "get_user_last_word",
        return_value='alter',
    )
    mocker.patch.object(
        WordsRepo, "get_translation_by_word_title", return_value='изменить'
    )
    mocker.patch.object(WordsRepo, "add_word", return_value=None)
    mocker.patch.object(WordsRepo, "add_last_word", return_value=None)
    mocker.patch.object(WordsRepo, "get_word", return_value=None)
    response = client.get(
        "/word",
        headers={
            'token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ"
            "9.eyJ1c2VyX2lkIjoiNDY5N2VlZDctODE5M"
            "y00MjQ5LWIxMzktOTZhZjZiMjI0MTdhIiwi"
            "dXNlcl9uYW1lIjoiQW5kcmVpIn0.B1tec9Y"
            "E-ayxwhWvG5fqapc5k7KVNMm5NoY6IF3_Inc"
        },
    )
    assert response.status_code == 200
    assert 'word' in response.json()
