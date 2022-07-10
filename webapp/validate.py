def issue_validate(summary, status, type):
    errors = {}
    if not summary:
        errors["summary"] = "Поле обязательное"
    elif len(summary) > 50:
        errors["summary"] = "Должно быть меньше 50 символов"
    if not status:
        errors["status"] = "Поле обязательное"
    if not type:
        errors["type"] = "Поле обязательное"
    return errors
