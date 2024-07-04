<template>
    <div class="loading-container">
        <div v-if="loading" class="container_loader">
            <div class="loading-spinner"></div>
        </div>
        <div v-if="error" class="error-container">
            <h3>{{ errorMessage }}</h3>
            <p>Повторная попытка через {{ retryCountdown }} секунд...</p>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
    props: {
        fetchData: {
            type: Function,
            required: true
        }
    },
    setup(props) {
        const loading = ref(true);
        const error = ref(false);
        const errorMessage = ref('');
        const retryCountdown = ref(30);
        const retryInterval = 30000; 

        const executeFetch = async () => {
            loading.value = true;
            error.value = false;
            try {
                await props.fetchData();
                loading.value = false;
            } catch (err) {
                loading.value = false;
                error.value = true;
                errorMessage.value = err.message;
                startRetryCountdown();
            }
        };

        const startRetryCountdown = () => {
            let countdown = retryCountdown.value;
            const interval = setInterval(() => {
                countdown -= 1;
                retryCountdown.value = countdown;

                if (countdown === 0) {
                    clearInterval(interval);
                    retryCountdown.value = 30;
                    executeFetch();
                }
            }, 1000);
        };

        onMounted(() => {
            executeFetch();
        });

        return {
            loading,
            error,
            errorMessage,
            retryCountdown
        };
    }
};
</script>

<style>

.loading-container {
    width: 100%;
    height: 100%;
}


.container_loader {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}

.loading-spinner {
    z-index: 1;
    position: relative;
    border: 10px solid rgba(0, 0, 0, 0.1);
    border-left-color: #97C2CF;
    border-radius: 50%;
    width: 128px;
    height: 128px;
    animation: spin 1s infinite cubic-bezier(0.5, 0, 0.5, 1);
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.error-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    color: red;
    font-size: 14px;
}

.error-container > h3{
    font-weight: 600;
}

.error-container > p{
    padding: 10px 25px;
    border-radius: 10px;
    border: 1px solid red;
    background: rgba(155,0,0,0.2);
    backdrop-filter: blur(100px);
    color: var(--color-active-text);
}


</style>
