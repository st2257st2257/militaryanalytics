class Checkbox {
    constructor(id, name, value, label, checked = false) {
        this.id = id;
        this.name = name;
        this.value = value;
        this.label = label;
        this.checked = checked;
    }
}

export default Checkbox