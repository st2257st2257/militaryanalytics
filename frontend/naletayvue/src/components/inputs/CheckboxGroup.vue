<template>
    <div class="checkboxes-container">
        <label
            v-for="checkbox in checkboxes"
            :key="checkbox.id"
            :class="buttonClass(checkbox)"
        >
            <input
                :type="inputType"
                :checked="isSelected(checkbox)"
                :id="checkbox.id"
                :name="checkbox.name"
                :value="checkbox.value"
                :class="[inputClass]"
                @change="handleCheckboxChange(checkbox)"
            />
            <span v-if="['checkbox', 'radio'].includes(inputType) && displayType === 'checkbox'" class="checkmark"></span>
            <p class="">{{ checkbox.label }}</p>
        </label>
    </div>
</template>

<script>
class Checkbox {
    constructor(id, name, value, label, checked = false) {
        this.id = id;
        this.name = name;
        this.value = value;
        this.label = label;
        this.checked = checked;
    }
}

export default {
    props: {
        checkboxesData: {
            type: Array,
            required: true,
        },
        inputType: {
            type: String,
            default: 'checkbox',
            validator: value => ['checkbox', 'radio'].includes(value),
        },
        displayType: {
            type: String,
            default: 'button',
            validator: value => ['button', 'checkbox'].includes(value),
        },
        minSelects: {
            type: Number,
            default: 1,
        },
        maxSelects: {
            type: Number,
            default: 1,
        },
        modelValue: {
            type: Array,
            default: () => []
        }
    },
    data() {
        return {
            checkboxes: [],
            selectedCheckboxValues: [],
            error: '',
        };
    },
    watch: {
        modelValue: {
            handler(newSelectedValues) {
                this.selectedCheckboxValues = newSelectedValues;
            },
            immediate: true
        }
    },
    computed: {
        inputClass() {
            return this.displayType === 'button' ? 'button-input' : 'checkbox-input';
        }
    },
    methods: {
        buttonClass(checkbox) {
            if (this.displayType === 'checkbox') return 'checkbox-label';
            return {
                btn: this.displayType === 'button',
                'checkbox-btn': this.displayType === 'button',
                'checked': this.isSelected(checkbox),
                'checkbox-label': this.displayType === 'checkbox'
            };
        },
        isSelected(checkbox) {
            return this.selectedCheckboxValues.some(selected => selected.id === checkbox.id);
        },
        handleCheckboxChange(checkbox) {
            if (this.inputType === 'radio') {
                this.selectedCheckboxValues = [checkbox];
            } else {
                if (this.isSelected(checkbox)) {
                    this.selectedCheckboxValues = this.selectedCheckboxValues.filter(val => val.id !== checkbox.id);
                } else {
                    if (this.selectedCheckboxValues.length < this.maxSelects) {
                        this.selectedCheckboxValues.push(checkbox);
                    }
                }
            }
            this.$emit('update:modelValue', this.selectedCheckboxValues);
            this.$emit('selected', this.selectedCheckboxValues);
        },
        validate() {
            if (this.selectedCheckboxValues.length < this.minSelects) {
                this.error = `Вы должны выбрать как минимум ${this.minSelects} элементов.`;
                return this.error;
            }
            this.error = '';
            return '';
        },
    },
    mounted() {
        this.checkboxes = this.checkboxesData.map(checkboxData => new Checkbox(checkboxData.id, checkboxData.name, checkboxData.value, checkboxData.label));
    },
};
</script>

<style scoped>
.checkbox-btn {
    text-align: left;
    border: 2px solid var(--color-btn-background);
}

.checkboxes-container {
    display: flex;
    flex-flow: row wrap;
    gap: 10px;
}

.button-input {
    z-index: -1;
    position: absolute;
    opacity: 0;
}

.checkbox-input {
    position: absolute;
    opacity: 0;
}

.checkbox-btn.checked {
    background: var(--color-btn-green-background);
    color: var(--color-active-text);
    border: 2px solid var(--color-btn-green-background);
    box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
}

.checkbox-label {
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    font-size: 15px;
}

.btn {
    padding: 10px 15px;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.2s;
}

.btn:hover {
    color: var(--color-active-text);
    background: var(--color-btn-green-background);
    border: 2px solid var(--color-btn-green-background);
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

/* Checkmark styles */
.checkmark {
    cursor: pointer;
    display: inline-block;
    width: 22px;
    height: 22px;
    margin-right: 10px;
    border-radius: 4px;
    position: relative;
    border: 2px solid #ddd;
    transition: background-color 0.3s, border-color 0.3s;
}

.checkmark::after {
    content: "";
    position: absolute;
    display: none;
    left: 6px;
    top: 3px;
    width: 6px;
    height: 12px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
}

.checkbox-input:checked + .checkmark {
    background-color: var(--color-btn-green-background);
    border-color: var(--color-btn-green-background);
}

.checkbox-input:checked + .checkmark::after {
    display: block;
}

.error {
    font-size: 12px;
    color: red;
}
</style>
