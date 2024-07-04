<template>
    <div class="form-container">
        <h3>{{ title }}</h3>
        <form class="form-wrapper" @submit.prevent="submitForm">
            <slot :formData="formData" :errors="errors" :handleInputError="handleInputError" :submitted="submitted"></slot>
            <button type="submit" class="btn green-btn">{{ submitButtonText }}</button>
        </form>
    </div>
</template>

<script>
import api from '@/authAPI.js';
import { mapGetters } from 'vuex';
import { reactive, toRefs } from 'vue';

export default {
    props: {
        title: {
            type: String,
            required: true,
        },
        requests: {
            type: [Array, Object],
            required: true,
        },
        submitButtonText: {
            type: String,
            default: 'Submit',
        },
        formData: {
            type: Object,
            required: true,
        }
    },
    computed: {
        ...mapGetters('user', ['currentUser']),
    },
    setup() {
        const state = reactive({
            errors: {},
            submitted: false
        });

        return {
            ...toRefs(state)
        };
    },
    methods: {
        async submitForm() {
            this.submitted = true;

            const hasErrors = Object.keys(this.errors).length > 0;
            if (hasErrors) {
                window.notificationManager.addNotification('error', 'Исправьте ошибки в форме', 2000);
                return;
            }

            const requestsArray = Array.isArray(this.requests) ? this.requests : [this.requests];

            try {
                for (const request of requestsArray) {
                    const payload = request.createPayload(this.formData, this.currentUser?.username);

                    if (payload != null) {
                        const response = await api.post(request.url, payload);

                        if (response.status !== 200 || response.data.result !== true) {
                            throw new Error(response.data["Error: "] || 'Ошибка при отправке данных');
                        }
                    }
                }
                window.notificationManager.addNotification('success', 'Данные успешно изменены', 2000);
                this.$emit('submit-success');
            } catch (error) {
                window.notificationManager.addNotification('error', error.message || 'Ошибка при отправке данных', 2000);
            }
        },
        handleInputError({ variableName, error }) {
            if (error) {
                this.errors[variableName] = error;
            } else {
                this.clearError(variableName);
            }
        },
        clearError(variableName) {
            delete this.errors[variableName];
        },
    }
};
</script>

<style scoped>
.form-container {
    display: flex;
    flex-flow: column;
    width: 100%;
    max-width: 600px;
    height: fit-content;
    padding: 10px;
    border-radius: 15px;
    background: var(--color-background-soft);
}

button {
    margin-top: 10px;
}

.form-wrapper {
    display: flex;
    flex-flow: column;
    gap: 5px;
}

.note {
    font-size: 12px;
    color: gray;
}

h3 {
    font-weight: 500;
    width: 100%;
    border-bottom: 1px solid var(--color-background-hover);
    margin-bottom: 15px;
}
</style>
