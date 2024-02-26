from db_models.models import ContactPerson, Worker


def get_current_contact_person(telegram_user_name: str) -> ContactPerson | None:
    try:
        contact_person = ContactPerson.objects.get(telegram_user_name=telegram_user_name)
        return contact_person
    except Exception as err:
        print(err)
        return None


def get_current_worker(telegram_user_name: str) -> Worker | None:
    try:
        worker = Worker.objects.get(telegram_user_name=telegram_user_name)
        return worker
    except Exception as err:
        print(err)
        return None
