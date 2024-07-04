export function validatePassword(value) {
    if (!value) {
        return 'Пароль обязателен для заполнения';
    } else if (value.length < 8) {
        return 'Пароль должен содержать не менее 8 символов';
    }
    return '';
}

export function validateRepeatPassword(value, password) {
    if (!value) {
        return 'Повтор пароля обязателен для заполнения';
    } else if (value !== password) {
        return 'Пароли не совпадают';
    }
    return '';
}