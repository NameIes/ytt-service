from db_models.models import ContactPerson, Worker


def get_current_contact_person(**model_param) -> ContactPerson | None:
    """
    **model_param: Поля модели по которой произойдет выборка объекта модели ContactPerson
    """
    try:
        contact_person = ContactPerson.objects.get(**model_param)
        return contact_person
    except ContactPerson.DoesNotExist:
        return None


def get_current_worker(**model_param) -> Worker | None:
    """
    **model_param: Поля модели по которой произойдет выборка объекта модели Worker
    """
    try:
        worker = Worker.objects.get(**model_param)
        return worker
    except Worker.DoesNotExist:
        return None
