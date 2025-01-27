import sender_stand_request
import data

def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," + user_body["address"] + ",,," + \
               user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    message_response = "Has introducido un nombre de usuario no válido. El nombre solo puede contener letras del alfabeto latino, la longitud debe ser de 2 a 15 caracteres."

    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400
    assert user_response.json()["message"] == message_response

def negative_assert_no_first_name(user_body):
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    response = sender_stand_request.post_new_user(user_body)
    message_response = "No se han aprobado todos los parámetros requeridos"

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == message_response

def negative_assert_empty_first_name(user_body):
    user_body = get_user_body("")
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")

def test_create_user_1_letter_in_first_name_get_success_response():
    negative_assert_symbol("A")

def test_create_user_16_letters_in_first_name_get_success_response():
    negative_assert_symbol("Аааааааааааааааa")

def test_create_user_has_blank_space_between_letters_in_first_name_get_error_response():
    negative_assert_symbol("Che cho")

def test_create_user_has_special_characters_in_first_name_get_error_response():
    negative_assert_symbol("Ch&ch@")

def test_create_user_has_numbers_in_first_name_get_error_response():
    negative_assert_symbol("Ch3ch0")

def test_create_user_no_first_name_get_error_response():
    negative_assert_no_first_name(user_body="")

def test_create_user_empty_first_name_get_error_response():
    negative_assert_empty_first_name(user_body="")

def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400