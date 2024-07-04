<template>
    <div class="placeholder_container">
        <NaletayLogo class="placeholder_logo" />
        <p class="animated_text">В разработке</p>
    </div>
</template>

<script>
import NaletayLogo from '@/assets/icons/logo_naletay.svg';

export default {
    components: {
        NaletayLogo
    }
}
</script>

<style>
.main-container {
    margin: 0 !important;
    padding: 0 !important;
}

.placeholder_container {
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-flow: column;
    justify-content: center;
    align-items: center;
    gap: 25px;
    background: linear-gradient(180deg, #f5f7fa, rgba(8, 139, 149, 0.25));
    padding:0;
    margin: 0;
}

.placeholder_logo {
    width: 340px;
    animation: logoBounce 2s infinite;
}

.placeholder_container p {
    font-size: 22px;
    padding: 10px 35px;
    background: var(--color-background-soft);
    border-radius: 25px;
    color: #000;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.25)
}

@keyframes logoBounce {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-20px);
    }
}
</style>
