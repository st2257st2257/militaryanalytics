<template>
    <div class="range-slider">
        <label v-if="label">{{ label }}: {{ localMin }} {{ unit }} - {{ localMax }} {{ unit }}</label>
        <div class="slider-container">
            <input type="range" :min="min" :max="max" :step="step" v-model="localMin" @input="updateRange('min')" class="thumb thumb-min" />
            <input type="range" :min="min" :max="max" :step="step" v-model="localMax" @input="updateRange('max')" class="thumb thumb-max" />
            <div class="slider-track"></div>
            <div class="slider-range" :style="rangeStyle"></div>
        </div>
        <div class="input-container">
            <input style="text-align: left;" type="number" v-model="localMin" @input="updateRange('min', true)" :min="min" :max="max" class="range-input" />
            <input style="text-align: right;" type="number" v-model="localMax" @input="updateRange('max', true)" :min="min" :max="max" class="range-input" />
        </div>
    </div>
</template>

<script>
export default {
    name: "RangeSlider",
    props: {
        label: String,
        min: {
            type: Number,
            default: 0
        },
        max: {
            type: Number,
            default: 10000000
        },
        step: {
            type: Number,
            default: 100
        },
        unit: {
            type: String,
            default: ''
        },
        modelValue: {
            type: [Object, String],
            required: true
        }
    },
    data() {
        return {
            localMin: this.modelValue.min !== undefined ? this.modelValue.min : this.min,
            localMax: this.modelValue.max !== undefined ? this.modelValue.max : this.max,
            minDifference: 0
        };
    },
    watch: {
        modelValue: {
            handler(newValue) {
                this.localMin = newValue.min !== undefined ? newValue.min : this.min;
                this.localMax = newValue.max !== undefined ? newValue.max : this.max;
            },
            immediate: true,
            deep: true
        },
        min(newVal) {
            this.localMin = this.modelValue.min !== undefined ? this.modelValue.min : newVal;
        },
        max(newVal) {
            this.localMax = this.modelValue.max !== undefined ? this.modelValue.max : newVal;
        }
    },
    computed: {
        rangeStyle() {
            const minPercentage = ((this.localMin - this.min) / (this.max - this.min)) * 90;
            const maxPercentage = ((this.localMax - this.min) / (this.max - this.min)) * 90;
            return {
                left: `${Math.max(minPercentage, 1)}%`,
                width: `${maxPercentage - minPercentage + 9}%`,
                transition: 'none'
            };
        }
    },
    methods: {
        updateRange(type, fromInput = false) {
            const min = parseFloat(this.localMin);
            const max = parseFloat(this.localMax);
            const diff = max - min;

            if (type === 'min' && min >= max - this.minDifference) {
                this.localMin = (max - this.minDifference).toFixed(0);
            } else if (type === 'max' && max <= min + this.minDifference) {
                this.localMax = (min + this.minDifference).toFixed(0);
            }

            if (parseFloat(this.localMin) < this.min) this.localMin = this.min.toString();
            if (parseFloat(this.localMax) > this.max) this.localMax = this.max.toString();

            if (!fromInput) {
                this.localMin = Math.min(parseFloat(this.localMin), parseFloat(this.localMax)).toFixed(0);
                this.localMax = Math.max(parseFloat(this.localMin), parseFloat(this.localMax)).toFixed(0);
            }

            this.$emit("update:modelValue", { min: parseFloat(this.localMin), max: parseFloat(this.localMax) });
        }
    }
};
</script>

<style scoped>
.range-slider {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    box-sizing: border-box;
    user-select: none;
}

.range-slider > label {
    font-size: 11px;
    margin-bottom: 5px;
}

.slider-container {
    position: relative;
    width: 100%;
    height: 20px;
}

input[type="range"] {
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    background: transparent;
    position: absolute;
    pointer-events: none;
    height: 20px;
}

input[type="range"].thumb-min {
    width: 90%;
    left: 0;
    z-index: 2;
}

input[type="range"].thumb-max {
    width: 90%;
    right: 0;
    z-index: 2;
}

input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 15px;
    height: 15px;
    background: var(--color-btn-green-background);
    cursor: pointer;
    pointer-events: auto;
    border-radius: 50%;
}

input[type="range"]::-moz-range-thumb {
    width: 15px;
    height: 15px;
    background: var(--color-btn-green-background);
    cursor: pointer;
    pointer-events: auto;
    border-radius: 50%;
}

.slider-track {
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 4px;
    background: #ddd;
    transform: translateY(-50%);
}

.slider-range {
    position: absolute;
    top: 50%;
    max-width: 100%;
    min-width: 10%;
    height: 4px;
    background: var(--color-btn-green-background);
    transform: translateY(-50%);
    z-index: 1;
    transition: none;
}

.input-container {
    width: 100%;
    display: flex;
    justify-content: space-between;
    margin-top: 5px;
}

.range-input {
    width: auto;
    text-align: center;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 14px;
}

.range-input::-webkit-inner-spin-button, 
.range-input::-webkit-outer-spin-button { 
    -webkit-appearance: none; 
    margin: 0; 
}

.range-input[type=number] {
    background: none;
    border: none;
    outline: none;
    -moz-appearance: textfield;
}
</style>
