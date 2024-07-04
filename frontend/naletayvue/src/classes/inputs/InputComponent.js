class InputComponent {
    constructor(value, placeholder = '') {
        this.value = value;
        this.placeholder = placeholder;
        this.icon = null;
    }

    setValue(newValue) {
        this.value = newValue;
    }

    setIcon(icon) {
        this.icon = icon;
    }

    clearIcon() {
        this.icon = null;
    }

    isValid(validationFunction, oldValue, newValue) {
        if (validationFunction) {
            return validationFunction(oldValue, newValue);
        }
        return true;
    }
}

export default InputComponent