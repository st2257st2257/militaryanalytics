<template>
    <div class="dropdown" ref="dropdown">
        <button class="dropbtn" @click="toggleDropdown">{{ selectedText }}</button>
        <div v-if="isOpen" class="dropdown-content">
            <a 
                v-for="option in options" 
                :key="`option-${option.value}`" 
                @click="selectOption(option)"
                :class="{ 'selected': option.value === selected }"
            >
                {{ option.text }}
            </a>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        options: {
            type: Array,
            required: true,
        },
        selected: {
            type: [String, Number],
            default: '',
        },
        confirmable: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            isOpen: false,
            selectedText: '',
            pendingSelection: null,
        };
    },
    watch: {
        selected: {
            immediate: true,
            handler(newValue) {
                const selectedOption = this.options.find(option => option.value === newValue);
                this.selectedText = selectedOption ? selectedOption.text : '';
            }
        }
    },
    methods: {
        toggleDropdown() {
            this.isOpen = !this.isOpen;
        },
        selectOption(option) {
            if (option.value === this.selected) {
                this.isOpen = false;
                return;
            }
            if (this.confirmable) {
                this.pendingSelection = option;
                this.$emit('select', option.value, true);
            } else {
                this.applySelection(option);
            }
        },
        applySelection(option) {
            this.selectedText = option.text;
            this.isOpen = false;
            this.$emit('select', option.value);
        },
        handleClickOutside(event) {
            if (this.$refs.dropdown && !this.$refs.dropdown.contains(event.target)) {
                this.isOpen = false;
            }
        }
    },
    mounted() {
        document.addEventListener('mousedown', this.handleClickOutside);
        const selectedOption = this.options.find(option => option.value === this.selected);
        this.selectedText = selectedOption ? selectedOption.text : '';
    },
    beforeDestroy() {
        document.removeEventListener('mousedown', this.handleClickOutside);
    },
};
</script>

<style scoped>
.dropdown {
    position: relative;
    display: inline-block;
    border-radius: 10px;
}

.dropbtn {
    width: 100%;
    background-color: transparent;
    color: inherit;
    font-size: 16px;
    border: none;
    min-width: 160px;
    cursor: pointer;
    min-height: 20px;
    height: fit-content;
}

.dropdown-content {
    display: block;
    top: 55px;
    left: 0;
    position: absolute;
    background-color: #f9f9f9;
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    z-index: 4;
    border-radius: 10px;
    overflow: hidden;
    width: 100%;
    text-align: left;
}

.dropdown-content a {
    color: black;
    width: 100%;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
}

.dropdown-content a:hover {
    background-color: #f1f1f1;
}

.dropdown-content a.selected {
    background-color: #e0e0e0;
    font-weight: bold;
    pointer-events: none;
}
</style>
