<template>
    <ModalWindow ref="confirmModal" title="Подтверждение">
        <template #content>
            <p>{{ message }}</p>
        </template>
        <template #buttons>
            <button class="btn green-btn" @click="apply">Применить</button>
            <button class="btn error-btn" @click="close">Отменить</button>
        </template>
    </ModalWindow>
</template>

<script>
import ModalWindow from '@/components/modals/ModalWindow.vue';

export default {
    components: {
        ModalWindow,
    },
    data() {
        return {
            message: '',
            resolvePromise: null,
        };
    },
    methods: {
        open(customMessage) {
            this.message = customMessage;
            this.$refs.confirmModal.open();
            return new Promise((resolve) => {
                this.resolvePromise = resolve;
            });
        },
        close() {
            this.$refs.confirmModal.close();
            if (this.resolvePromise) {
                this.resolvePromise(false);
                this.resolvePromise = null;
            }
        },
        apply() {
            this.$refs.confirmModal.close();
            if (this.resolvePromise) {
                this.resolvePromise(true);
                this.resolvePromise = null;
            }
        },
    },
    mounted() {
        window.confirmModal = this;
    },
};
</script>
