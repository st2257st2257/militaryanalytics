<template>
    <div class="filters">
        <CustomInput
            label="Название"
            variableName="name"
            v-model="filters.name"
            inputType="search"
            placeholder="Название товара"
            @input="updateFilters"
        />
        <div class="price-filter">
            <p>Цена: от {{ formattedMinPrice }} до {{ formattedMaxPrice }}</p>
            <RangeSlider
                :min="0"
                :max="10000000"
                :step="10000"
                v-model="filters.price"
                @input="updateFilters"
            />
        </div>

        <div class="option-filters">
            <CustomInput
                label="Каталоги"
                variableName="type"
                v-model="filters.type"
                :options="typeOptions"
                inputType="select"
                @change="updateType"
            />
        </div>

        <div v-if="filters.type && filters.type !== 'Везде'" style="display:flex; flex-flow:column; gap:10px;">
            <div class="option-filters" v-for="(option, index) in dropdownFilters" :key="`dropdown-${index}`">
                <CustomInput
                    v-if="option.options.length > 0"
                    :label="option.label"
                    :variableName="option.variableName"
                    v-model="filters[option.variableName]"
                    :options="option.options"
                    inputType="select"
                    @change="updateFilters"
                />
            </div>

            <div class="option-filters">
                <template v-for="(field, index) in characteristicFilters">
                    <CustomInput
                        v-if="field.inputType === 'select'"
                        :key="`custom-${index}`"
                        :label="field.label"
                        :variableName="field.variableName"
                        v-model="filters[field.variableName]"
                        :options="field.options"
                        :inputType="field.inputType"
                        @change="updateFilters"
                    />
                    <RangeSlider
                        v-else
                        :key="`range-${index}`"
                        :label="field.label"
                        :min="getRangeMinValue(field)"
                        :max="getRangeMaxValue(field)"
                        :step="getRangeStepValue(field)"
                        :unit="field.unit"
                        v-model="filters[field.variableName]"
                        @input="updateFilters"
                    />
                </template>
            </div>
        </div>

        <div v-if="filters.type === 'Везде'" style="display:flex; flex-flow:column; gap:10px;">
            <div class="option-filters" v-for="(option, index) in allDropdownFilters" :key="`all-dropdown-${index}`">
                <CustomInput
                    v-if="option.options.length > 0"
                    :label="option.label"
                    :variableName="option.variableName"
                    v-model="filters[option.variableName]"
                    :options="option.options"
                    inputType="select"
                    @change="updateFilters"
                />
            </div>

            <div class="option-filters">
                <template v-for="(field, index) in allCharacteristicFilters">
                    <CustomInput
                        v-if="field.inputType === 'select'"
                        :key="`custom-all-${index}`"
                        :label="field.label"
                        :variableName="field.variableName"
                        v-model="filters[field.variableName]"
                        :options="field.options"
                        :inputType="field.inputType"
                        @change="updateFilters"
                    />
                    <RangeSlider
                        v-else
                        :key="`range-all-${index}`"
                        :label="field.label"
                        :min="getRangeMinValue(field)"
                        :max="getRangeMaxValue(field)"
                        :step="getRangeStepValue(field)"
                        :unit="field.unit"
                        v-model="filters[field.variableName]"
                        @input="updateFilters"
                    />
                </template>
            </div>
        </div>

        <button @click="resetFilters" class="mini-btn transparent-btn reset-button">Сбросить фильтры</button>
    </div>
</template>

<script>
import { nextTick } from 'vue';
import CustomInput from '@/components/inputs/CustomInput.vue';
import RangeSlider from '@/components/inputs/RangeSlider.vue';
import { mapGetters } from 'vuex';
import { formatCurrency } from '@/utils/format.js';

export default {
    components: {
        CustomInput,
        RangeSlider
    },
    data() {
        return {
            filters: this.initializeFilters(),
            characteristicFilters: [],
            allCharacteristicFilters: [],
            typeOptions: [],
            typeMapping: {
                all: 'Все',
                commodity: 'Беспилотники',
                service: 'Услуги',
                droneHub: 'Дронопорты'
            }
        };
    },
    computed: {
        ...mapGetters('products', ['types', 'getFilterDataByType', 'getAllFilters']),
        dropdownFilters() {
            if (!this.filters.type || this.filters.type === 'Везде') return [];
            const filterData = this.getFilterDataByType(this.convertTypeToMachineReadable(this.filters.type));
            return [
                { label: 'Категория', variableName: 'category', options: this.createOptions(filterData.categories) },
                { label: 'Подкатегория', variableName: 'subcategory', options: this.createOptions(filterData.subcategories) },
                { label: 'Производитель', variableName: 'manufacturer', options: this.createOptions(filterData.suppliers) },
                { label: 'Отрасли', variableName: 'mainBranches', options: this.createOptions(filterData.industries) },
                { label: 'Применение', variableName: 'mainPurposes', options: this.createOptions(filterData.applications) },
            ];
        },
        allDropdownFilters() {
            const filterData = this.getAllFilters;
            return [
                { label: 'Категория', variableName: 'category', options: this.createOptions(filterData.categories) },
                { label: 'Подкатегория', variableName: 'subcategory', options: this.createOptions(filterData.subcategories) },
                { label: 'Производитель', variableName: 'manufacturer', options: this.createOptions(filterData.suppliers) },
                { label: 'Отрасли', variableName: 'mainBranches', options: this.createOptions(filterData.industries) },
                { label: 'Применение', variableName: 'mainPurposes', options: this.createOptions(filterData.applications) },
            ];
        },
        formattedMinPrice() {
            return formatCurrency(this.filters.price.min, 'RUB');
        },
        formattedMaxPrice() {
            return formatCurrency(this.filters.price.max, 'RUB');
        }
    },
    watch: {
        filters: {
            handler(newFilters, oldFilters) {
                if (JSON.stringify(newFilters) !== JSON.stringify(oldFilters)) {
                    this.updateFilters();
                }
            },
            deep: true
        },
        types: {
            handler(newTypes) {
                this.fetchTypes(newTypes);
            },
            immediate: true
        },
        '$route.query': {
            handler(newQuery) {
                this.updateFiltersFromQuery(newQuery);
            },
            immediate: true
        },
        'filters.type': {
            handler(newType) {
                this.filters.type = this.typeMapping[newType] || newType;
            }
        }
    },
    methods: {
        createOptions(items, labelFunc = null) {
            return items ? items.map(item => ({
                label: labelFunc ? labelFunc(item) : item,
                value: item,
            })) : [];
        },
        rangeObjectToString(range) {
            return JSON.stringify(range);
        },
        stringToRangeObject(str) {
            try {
                return JSON.parse(str);
            } catch (e) {
                return { min: 0, max: 1000000 };
            }
        },
        async updateType() {
            const newType = this.filters.type;
            await this.resetFilters();
            this.filters.type = newType;
            const type = this.convertTypeToMachineReadable(this.filters.type);
            if (type && type !== 'all') {
                this.characteristicFilters = await this.getCharacteristicFiltersByType(type);
            } else {
                this.characteristicFilters = [];
                this.allCharacteristicFilters = await this.getAllCharacteristicFilters();
            }
            await this.updateFilters();
        },
        getCharacteristicFiltersByType(type) {
            const filters = {
                commodity: [
                    { label: 'Макс. длительность полета', variableName: 'maxDuration', placeholder: 'Введите длительность', min: 0, max: 1000, step: 10, unit: 'мин' },
                    { label: 'Макс. скорость полета', variableName: 'maxFlightSpeed', placeholder: 'Введите скорость', min: 0, max: 1000, step: 10, unit: 'км/ч' },
                    { label: 'Макс. дальность полета', variableName: 'maxRangePayload', placeholder: 'Введите дальность', min: 0, max: 1000, step: 10, unit: 'км' },
                    { label: 'Кол-во двигателей', variableName: 'numberOfEngines', placeholder: 'Введите количество', min: 1, max: 10, step: 1, unit: 'шт' },
                    { label: 'Тип двигателя', variableName: 'engineType', placeholder: 'Выберите тип двигателя', inputType: 'select', 
                        options: [
                            { "label": "Внутреннее сгорание", "value": "Внутреннее сгорание" },
                            { "label": "Электрический", "value": "Электрический" },
                            { "label": "Другое", "value": "Другое" } 
                        ]
                    },
                    { label: 'Дальность линии связи', variableName: 'communicationRange', placeholder: 'Введите дальность', min: 0, max: 1000, step: 10, unit: 'км' },
                    { label: 'Макс. высота полета', variableName: 'maxFlightAltitude', placeholder: 'Введите высоту', min: 0, max: 10000, step: 100, unit: 'м' },
                    { label: 'Мин. состав экипажа', variableName: 'minCrew', placeholder: 'Введите состав', min: 1, max: 10, step: 1, unit: 'чел' },
                    { label: 'Мин. скорость взлета', variableName: 'minTakeoffSpeed', placeholder: 'Введите скорость', min: 0, max: 100, step: 1, unit: 'км/ч' },
                    { label: 'Гарантия', variableName: 'warranty', placeholder: 'Выберите срок гарантии', inputType: 'select', 
                        options: [
                            { "label": "Да", "value": "Да" },
                            { "label": "Нет", "value": "Нет" },
                        ]
                    },
                ],
                service: [],
                droneHub: []
            };
            return filters[type] || [];
        },
        getAllCharacteristicFilters() {
            return [
                ...this.getCharacteristicFiltersByType('commodity'),
                ...this.getCharacteristicFiltersByType('service'),
                ...this.getCharacteristicFiltersByType('droneHub'),
            ];
        },
        async fetchTypes(types) {
            await nextTick();
            this.typeOptions = this.createOptions(types, type => this.typeMapping[type] || type);
        },
        updateFilters() {
            const queryParams = this.stringifyObjectValues(this.filters);
            const trimmedQueryParams = {};

            Object.keys(queryParams).forEach(key => {
                if (typeof queryParams[key] === 'string' && queryParams[key].trim() === '') {
                    return;
                }
                if (key === 'type') {
                    trimmedQueryParams[key] = this.convertTypeToMachineReadable(this.filters[key]);
                } else {
                    trimmedQueryParams[key] = queryParams[key];
                }
            });

            this.$router.push({ path: this.$route.path, query: trimmedQueryParams }).catch(() => {});
        },
        resetFilters() {
            this.filters = this.initializeFilters();
            this.updateFilters();
        },
        async updateFiltersFromQuery(query) {
            const newFilters = this.initializeFilters();

            Object.keys(query).forEach(key => {
                if (this.filters.hasOwnProperty(key)) {
                    if (key === 'price') {
                        newFilters[key] = this.stringToRangeObject(query[key]);
                    } else {
                        try {
                            newFilters[key] = JSON.parse(query[key]);
                        } catch (e) {
                            newFilters[key] = query[key];
                        }
                    }
                }
            });

            newFilters.type = this.convertTypeToHumanReadable(newFilters.type);

            this.filters = newFilters;
            this.characteristicFilters = this.getCharacteristicFiltersByType(this.convertTypeToMachineReadable(this.filters.type));
            if (this.filters.type === 'Везде') {
                this.allCharacteristicFilters = this.getAllCharacteristicFilters();
            }
        },
        initializeFilters() {
            return {
                name: '',
                category: '',
                subcategory: '',
                type: '',
                price: { min: 0, max: 10000000 },
                manufacturer: '',
                mainBranches: '',
                mainPurposes: '',
                maxDuration: '',
                maxFlightSpeed: '',
                maxRangePayload: '',
                numberOfEngines: '',
                engineType: '',
                communicationRange: '',
                maxFlightAltitude: '',
                minCrew: '',
                minTakeoffSpeed: '',
                warranty: ''
            };
        },
        getRangeMinValue(field) {
            return field.min !== undefined ? field.min : 0;
        },
        getRangeMaxValue(field) {
            return field.max !== undefined ? field.max : 10000000;
        },
        getRangeStepValue(field) {
            return field.step !== undefined ? field.step : 1;
        },
        stringifyObjectValues(obj) {
            const newObj = { ...obj };
            Object.keys(newObj).forEach(key => {
                if (typeof newObj[key] === 'object' && newObj[key] !== null) {
                    newObj[key] = JSON.stringify(newObj[key]);
                }
            });
            return newObj;
        },
        convertTypeToHumanReadable(type) {
            return this.typeMapping[type] || type;
        },
        convertTypeToMachineReadable(type) {
            const invertedMapping = Object.entries(this.typeMapping).reduce((acc, [key, value]) => {
                acc[value] = key;
                return acc;
            }, {});
            return invertedMapping[type] || type;
        },
    },
    async mounted() {
        await this.fetchTypes(this.types);
    }
};
</script>

<style scoped>
.filters {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 10px;
    padding: 15px;
    box-sizing: border-box;
    border-radius: 15px;
    min-width: 300px;
    background: var(--color-background-soft);
}

.option-filters {
    display: flex;
    flex-flow: column;
    gap: 15px;
}

@media (min-width: 768px) {
    .filters {
        flex-direction: row wrap;
        gap: 10px;
    }
    .price-filter {
        flex-direction: row;
    }
}

.price-filter {
    display: flex;
    flex-direction: column;
    font-size: 12px;
}

@media (max-width: 388px) {
    .filters {
        flex-direction: row wrap;
        max-width: 92%;
        gap: 10px;
    }
}

.reset-button {
    margin-top: 25px;
}

.reset-button:hover {
    color: var(--color-background-error);
    border-color: var(--color-background-error);
}
</style>
