<template>
    <div v-if="addons.length > 0" class="addon-constructor" ref="addonConstructor">
        <h2 @click="toggleVisibility" class="addon-constructor-header">
            <div class="header-text">
                <img src="../assets/icons/puzzle.svg" class="title-icon" alt="icon" />
                <span class="title-text">Дополнительные опции</span>
            </div>
            <span class="mini-btn white-btn">{{ isVisible ? '-' : '+' }}</span>
        </h2>
        <div v-if="isVisible" class="addon-list">
            <CheckboxGroup
                v-model="tempSelectedAddons"
                :checkboxesData="formattedAddons"
                inputType="checkbox"
                displayType="button"
                :minSelects="0"
                :maxSelects="formattedAddons.length"
            />
            <button class="btn green-btn" @click="applyAddons">Применить</button>
        </div>
        <div v-if="selectedAddons.length > 0" class="selected-addons">
            <ul>
                <li>
                    + {{ selectedAddons.length }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import CheckboxGroup from '@/components/inputs/CheckboxGroup.vue';

export default {
    components: {
        CheckboxGroup,
    },
    props: {
        addons: {
            type: Array,
            required: true,
            default: () => []
        },
    },
    data() {
        return {
            tempSelectedAddons: [],
            selectedAddons: [],
            isVisible: false,
        };
    },
    computed: {
        formattedAddons() {
            return this.addons.map(addon => ({
                ...addon,
                checked: this.selectedAddons.some(selected => selected.id === addon.id)
            }));
        }
    },
    methods: {
        applyAddons() {
            this.selectedAddons = [...this.tempSelectedAddons];
            this.$emit('applyAddons', this.selectedAddons);
            this.isVisible = false;
        },
        toggleVisibility() {
            if (!this.isVisible) {
                this.tempSelectedAddons = [...this.selectedAddons];
            }
            this.isVisible = !this.isVisible;
        },
        handleClickOutside(event) {
            if (this.$refs.addonConstructor && !this.$refs.addonConstructor.contains(event.target)) {
                this.isVisible = false;
            }
        }
    },
    watch: {
        addons: {
            handler(newAddons) {
                this.tempSelectedAddons = newAddons.filter(addon => addon.checked);
                this.selectedAddons = newAddons.filter(addon => addon.checked);
            },
            deep: true,
            immediate: true
        }
    },
    mounted() {
        document.addEventListener('click', this.handleClickOutside);
        this.tempSelectedAddons = this.formattedAddons.filter(addon => addon.checked);
        this.selectedAddons = this.formattedAddons.filter(addon => addon.checked);
    },
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside);
    }
};
</script>

<style scoped>
.addon-constructor {
    position: relative;
    display: flex;
    flex-flow: row;
    gap: 15px;
    border-radius: 8px;
    width: fit-content;
}

.addon-constructor-header {
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 16px;
    padding: 5px;
    gap: 5px;
    border-radius: 10px;
    background: #f8f9fa;
}

.header-text {
    display: flex;
    justify-content: center;
    align-items: center;
}

.title-icon {
    width: 32px;
    height: 32px;
    margin-right: 10px;
}

.title-text {
    width: 100%;
    font-size: 14px;
    font-weight: bold;
    color: var(--color-primary);
}

.addon-list {
    z-index: 2;
    margin-top: 55px;
    position: absolute;
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding: 10px;
    border-radius: 15px;
    background: #f8f9fa;
    width: 100%;
    min-width: 250px;
    box-shadow: 0px 5px 15px rgba(0,0,0,.1);
}

.selected-addons {
    width: fit-content;
    border-radius: 8px;
    max-width: 400px;
}

.selected-addons h3 {
    margin-bottom: 10px;
}

.selected-addons ul {
    display: flex;
    flex-flow: row wrap;
    gap: 15px;
    list-style-type: none;
    padding: 0;
}

.selected-addons li {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    width: 46px;
    height: 46px;
    padding: 9px;
    border-radius: 30px;
    border: 2px solid var(--color-background-info);
}

@media (max-width: 768px) {
    .addon-constructor {
        flex-flow: row wrap;
    }
}
</style>
