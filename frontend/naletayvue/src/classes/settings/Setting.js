class Setting {
    constructor(variableName, variableValue, description, inputType, options = []) {
        this.variableName = variableName;
        this.variableValue = variableValue;
        this.description = description;
        this.inputType = inputType;
        this.options = options;
    }
}

export default Setting;
