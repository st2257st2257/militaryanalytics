import InputComponent from './InputComponent';

export default class Select extends InputComponent {
    constructor(value, options, placeholder = '') {
        super(value, placeholder);
        this.options = options;
    }
}
