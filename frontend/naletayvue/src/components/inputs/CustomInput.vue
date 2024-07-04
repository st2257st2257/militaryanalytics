<template>
    <div class="custom-input" :data-designation="designation" ref="customInput">
        <label :for="variableName" class="input-label">
            {{ label }}
            <span v-if="required" class="required">*</span>
        </label>

        <template v-if="inputType === 'input' || inputType === 'password'">
            <div class="input-container" :class="{ 'is-invalid': error && shouldShowError }">
                <input
                    :type="inputType === 'password' ? (showPassword ? 'text' : 'password') : 'text'"
                    :value="inputValue"
                    :placeholder="placeholder"
                    @input="handleInput($event.target.value)"
                    @keydown.enter="handleKeyPress"
                    class="input-field"
                    :maxlength="maxLength"
                    :required="required"
                />
                <span v-if="inputType === 'password'" class="toggle-password" @click="toggleShowPassword">
                    <showIcon class="file-icon" v-if="showPassword"/>
                    <hideIcon class="file-icon" v-if="!showPassword"/>
                </span>
                <label v-if="fileLoader" for="fileInput_input" class="file-icon">
                    <saveFiles />
                    <input
                        id="fileInput_input"
                        type="file"
                        @change="handleFileInput($event.target.files)"
                        class="file-input"
                        :accept="accept"
                        :multiple="multiple"
                    />
                </label>
                <span v-if="inputComponent.icon" class="icon">{{ inputComponent.icon }}</span>
                <span class="designation">{{ designation }}</span>
                <sendIcon class="file-icon" v-if="showSendButton" @click="handleSubmit" />
            </div>
        </template>

        <template v-else-if="inputType === 'textarea'">
            <div class="input-container" :class="{ 'is-invalid': error && shouldShowError }">
                <textarea
                    :value="inputValue"
                    :placeholder="placeholder"
                    @input="handleInput($event.target.value)"
                    @keydown.enter="handleKeyPress"
                    class="textarea-field"
                    :maxlength="maxLength"
                    :required="required"
                ></textarea>
                <label v-if="fileLoader" for="fileInput_textarea" class="file-icon">
                    <saveFiles />
                    <input
                        id="fileInput_textarea"
                        type="file"
                        @change="handleFileInput($event.target.files)"
                        class="file-input"
                        :accept="accept"
                        :multiple="multiple"
                    />
                </label>
            </div>
        </template>

        <template v-else-if="inputType === 'select'">
            <div class="custom-select">
                <div class="selected-option-container">
                    <div :class="{ 'selected-option': true}" @click="toggleDropdown">
                        {{ selectedLabel || placeholder }}
                        <span class="clear-icon" v-if="selectedValue" @click="clearSelection">×</span>
                    </div>
                </div>
                <ul :class="{ 'options-list': true}" ref="optionsList">
                    <li
                        v-for="option in options"
                        :key="option.value || option.label"
                        @click="selectOption(option)"
                        :class="{ 'selected': option.value === selectedValue }"
                    >
                        {{ option.label }}
                    </li>
                </ul>
            </div>
        </template>

        <template v-else-if="inputType === 'search'">
            <div class="input-container search">
                <span class="icon"><searchIcon class="search-icon" /></span>
                <input
                    type="text"
                    :value="inputValue"
                    :placeholder="placeholder"
                    @input="handleInput($event.target.value)"
                    @keydown.enter="handleKeyPress"
                    class="input-field search"
                    :maxlength="maxLength"
                />
                <span v-if="showSendButton" class="btn search-btn" @click="handleSubmit">Найти</span>
            </div>
        </template>

        <p v-if="error && shouldShowError" class="error">{{ error }}</p>
    </div>
</template>

<script>
import { ref, watch, onMounted } from 'vue';
import Input from '@/classes/inputs/Input.js';
import Select from '@/classes/inputs/Select.js';
import TextArea from '@/classes/inputs/TextArea.js';
import saveFiles from '@/assets/icons/saveFiles.svg';
import sendIcon from '@/assets/icons/sendIcon.svg';
import showIcon from '@/assets/icons/show_pass.svg';
import hideIcon from '@/assets/icons/hide_pass.svg';
import searchIcon from '@/assets/icons/search.svg';

export default {
    components: {
        saveFiles,
        sendIcon,
        hideIcon,
        showIcon,
        searchIcon,
    },
    props: {
        label: String,
        variableName: String,
        modelValue: [String, Number, File],
        inputType: {
            type: String,
            default: 'input'
        },
        placeholder: String,
        maxLength: {
            type: Number,
            default: Infinity
        },
        validationFunction: Function,
        designation: String,
        required: {
            type: Boolean,
            default: false
        },
        showSendButton: {
            type: Boolean,
            default: false
        },
        fileLoader: {
            type: Boolean,
            default: false
        },
        accept: String,
        multiple: Boolean,
        options: Array,
        error: String,
        shouldShowError: Boolean
    },
    emits: ['update:modelValue', 'send', 'change', 'update:modelFile', 'input-error'],
    setup(props, { emit }) {
        let inputComponent = null;

        switch (props.inputType) {
            case 'input':
            case 'password':
                inputComponent = new Input(props.modelValue);
                break;
            case 'select':
                inputComponent = new Select(props.modelValue, props.options);
                break;
            case 'textarea':
                inputComponent = new TextArea(props.modelValue);
                break;
            case 'search':
                inputComponent = new Input(props.modelValue);
                inputComponent.setIcon(searchIcon);
                break;
            default:
                inputComponent = new Input(props.modelValue);
        }

        const inputValue = ref(props.modelValue || '');
        const selectedValue = ref(props.modelValue || '');
        const selectedLabel = ref('');
        const error = ref(props.error);
        const showPassword = ref(false);
        const shouldShowError = ref(props.shouldShowError);

        const selectOption = (option) => {
            selectedValue.value = option.value || option.label;
            selectedLabel.value = option.label;
            emit('update:modelValue', option.value || option.label);
            emit('change', selectedValue.value);
            validate(option.value || option.label);
            closeAllSelects();
        };

        watch(() => props.modelValue, (newValue) => {
            if (props.inputType === 'select') {
                selectedValue.value = newValue;
                const selectedOption = props.options.find(option => {
                    return String(option.value).toLowerCase() === String(newValue).toLowerCase() || 
                           String(option.label).toLowerCase() === String(newValue).toLowerCase();
                });
                if (selectedOption) {
                    selectedLabel.value = selectedOption.label;
                } else {
                    selectedLabel.value = newValue;
                }
            } else {
                inputValue.value = newValue;
            }
        }, { immediate: true });

        watch(() => props.error, (newError) => {
            error.value = newError;
        }, { immediate: true });

        watch(() => props.shouldShowError, (newShowError) => {
            shouldShowError.value = newShowError;
        });

        const toggleDropdown = (event) => {
            const select = event.target.closest('.custom-select');
            if (select) {
                if (select.classList.contains('open')) {
                    select.classList.remove('open');
                } else {
                    closeAllSelects();
                    select.classList.add('open');
                }
            }
        };

        const closeAllSelects = () => {
            const allSelects = document.querySelectorAll('.custom-select');
            allSelects.forEach(select => {
                select.classList.remove('open');
            });
        };

        const clearSelection = () => {
            selectedValue.value = '';
            selectedLabel.value = '';
            emit('update:modelValue', '');
            emit('change', '');
            validate('');
        };

        const handleClickOutside = (event) => {
            if (!event.target.closest('.custom-select')) {
                closeAllSelects();
            }
        };

        onMounted(() => {
            document.addEventListener('click', handleClickOutside);

            if (props.inputType === 'select' && props.modelValue) {
                const selectedOption = props.options.find(option => {
                    return String(option.value).toLowerCase() === String(props.modelValue).toLowerCase() || 
                           String(option.label).toLowerCase() === String(props.modelValue).toLowerCase();
                });
                if (selectedOption) {
                    selectOption(selectedOption);
                } else {
                    selectedLabel.value = props.modelValue;
                }
            }
        });

        const handleInput = (newValue) => {
            inputValue.value = newValue;
            emit('update:modelValue', newValue);
            validate(newValue);
        };

        const handleFileInput = (files) =>
        {
            const file = files[0];
            emit('update:modelFile', file);
        };

        const handleSubmit = () => {
            if (props.showSendButton) {
                emit('send', props.modelValue);
            }
        };

        const handleKeyPress = (event) => {
            if (event.key === 'Enter') {
                handleSubmit();
            }
        };

        const setError = (validationError) => {
            error.value = validationError;
            emit('input-error', { variableName: props.variableName, error: validationError });
        };

        const validate = (value) => {
            if (props.validationFunction) {
                const validationError = props.validationFunction(value || inputValue.value);
                setError(validationError);
            } else {
                setError('');
            }
        };

        const toggleShowPassword = () => {
            showPassword.value = !showPassword.value;
        };

        return {
            inputComponent,
            inputValue,
            selectedValue,
            selectedLabel,
            error,
            toggleDropdown,
            selectOption,
            clearSelection,
            handleInput,
            handleFileInput,
            handleSubmit,
            handleKeyPress,
            validate,
            shouldShowError,
            showPassword,
            toggleShowPassword,
        };
    }
};
</script>

<style scoped>
.input-label {
    display: block;
}

.required {
    color: red;
}

.custom-input {
    position: relative;
    display: flex;
    flex-flow: column;
    justify-content: center;
    align-items: flex-start;
    width: 100%;
    height: 100%;
}

.input-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 10px;
    gap:5px;
    border: 1px solid var(--color-border);
    border-radius: 5px;
    background-color: #fff;
    color: #252525;
    outline: none;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease-in-out;
}

.input-field,
.textarea-field {
    width: 100%;
    border: none;
    background-color: none;
    color: #252525;
    outline: none;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease-in-out;
}

.textarea-field {
    resize: none;
    overflow-y: scroll;
    min-height: 100px;
}

.input-container.search {
    gap: 0;
    display: flex;
    flex-flow: row;
    align-items: center;
    justify-content: center;
    padding: 0;
    border-radius: 50px;
    width: 100%;
    overflow: hidden;
}

.input-container .input-field.search {
    padding: 10px;
    padding-left: 0;
}

.icon {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 55px;
}

.search-icon {
    max-width: 18px;
}

.custom-select {
    position: relative;
    min-width: 150px;
    width: 100%;
}

.selected-option-container {
    display: flex;
    align-items: center;
}

.selected-option {
    position: relative;
    display: flex;
    text-align: left;
    line-height: 15px;
    align-items: center;
    padding: 8px;
    width: 100%;
    height: 38px;
    background-color: #fff;
    border: 3px solid #97C2CF;
    border-radius: 5px;
    color: #252525;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.1s ease;
    z-index: 1;
    overflow: hidden;
    white-space: nowrap;
}

.clear-icon {
    z-index: 3;
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    right: 0px;
    font-size: 18px;
    color: #97C2CF;
    cursor: pointer;
    user-select: none;
    transition: color 0.3s ease;
    background: var(--color-background);
}

.clear-icon:hover {
    color: #FF0000;
}

.options-list {
    position: absolute;
    width: 100%;
    padding: 0;
    text-align: left;
    list-style: none;
    background-color: #fff;
    border: 3px solid #97C2CF;
    border-top: none;
    overflow: hidden;
    opacity: 0;
    transition: all 0.3s ease;
    max-height: 0;
    z-index: 4;
}

@media (hover: hover) {
    .options-list li:hover {
        background-color: #ebfaff;
        transition: all 0.3s ease;
    }
}
.custom-select.open .options-list {
    width: 100%;
    opacity: 1;
    max-height: 200px;
    box-shadow: 0px 4px 5px #97C2CF;
    overflow-y: auto;
}

.custom-select.open .selected-option {
    border-bottom: #fff;
    border-radius: 5px 5px 0 0;
    box-shadow: 0px -2px 5px #97C2CF;
    transition: all 0.3s ease;
}

.options-list li {
    padding: 8px;
    color: #252525;
    cursor: pointer;
    opacity: 0;
    transform: translateY(-10px);
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.custom-select.open .options-list li {
    opacity: 1;
    transform: translateY(0);
}

.options-list li.selected {
    background-color: #bee7f3;
    border-radius: 0;
}

.options-list li:last-child {
    border-radius: 0;
}

.error {
    font-size: 12px;
    color: red;
}

.input-container.is-invalid {
    border: 1px solid red;
}

.toggle-password .file-icon{
    width: 18px;
    height: 18px;
}

.toggle-password {
    display: flex;
    justify-content: center;
    align-items: center;
    user-select: none;
}
</style>
