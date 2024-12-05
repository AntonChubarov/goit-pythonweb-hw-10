import requests

BASE_URL = 'http://127.0.0.1:8000'


def create_contact():
    url = f'{BASE_URL}/contacts/'
    contact_data = {
        "first_name": "John",
        "last_name": "Smith",
        "email": "jsmth@example.com",
        "phone_number": "+380501234567",
        "birthday": "1990-05-15",
        "additional_data": "Some data"
    }
    response = requests.post(url, json=contact_data)
    print('Create Contact:')
    print(response.status_code)
    print(response.json())
    return response.json()


def get_all_contacts():
    url = f'{BASE_URL}/contacts/'
    response = requests.get(url)
    print('Get All Contacts:')
    print(response.status_code)
    print(response.json())


def get_contact(contact_id):
    url = f'{BASE_URL}/contacts/{contact_id}'
    response = requests.get(url)
    print(f'Get Contact ID {contact_id}:')
    print(response.status_code)
    print(response.json())


def update_contact(contact_id):
    url = f'{BASE_URL}/contacts/{contact_id}'
    update_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "jdoe@example.com",
        "phone_number": "+380501234567",
        "birthday": "1990-11-22",
        "additional_data": "Some data"
    }
    response = requests.put(url, json=update_data)
    print(f'Update Contact ID {contact_id}:')
    print(response.status_code)
    print(response.json())


def delete_contact(contact_id):
    url = f'{BASE_URL}/contacts/{contact_id}'
    response = requests.delete(url)
    print(f'Delete Contact ID {contact_id}:')
    print(response.status_code)
    print(response.text)


def search_contacts(first_name=None, last_name=None, email=None):
    url = f'{BASE_URL}/contacts/'
    params = {}
    if first_name:
        params['first_name'] = first_name
    if last_name:
        params['last_name'] = last_name
    if email:
        params['email'] = email
    response = requests.get(url, params=params)
    print('Search Contacts:')
    print(f'Parameters: {params}')
    print(response.status_code)
    print(response.json())


def get_upcoming_birthdays():
    url = f'{BASE_URL}/contacts/upcoming_birthdays'
    response = requests.get(url)
    print('Get Upcoming Birthdays:')
    print(response.status_code)
    print(response.json())


def main():
    contact = create_contact()
    contact_id = contact['id']

    get_all_contacts()

    get_contact(contact_id)

    update_contact(contact_id)

    search_contacts(first_name="John")

    get_upcoming_birthdays()

    delete_contact(contact_id)

    get_contact(contact_id)


if __name__ == '__main__':
    main()
