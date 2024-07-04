<template>
    <div class="usage-container">
        <h2>Применение БАС</h2>
        <div class="usage-grid">
            <a
                v-for="(item, index) in usageItems"
                :key="index"
                class="usage-card"
            >
                <component :is="item.icon" class="icon-placeholder" />
                <p>{{ item.title }}</p>
            </a>
        </div>
    </div>
</template>

<script>
import oilDerrickIcon from '@/assets/icons/oil-derrick.svg'
import mapIcon from '@/assets/icons/map.svg'
import plantsIcon from '@/assets/icons/plants.svg'
import factoryIcon from '@/assets/icons/factory.svg'
import truckIcon from '@/assets/icons/truck.svg'
import craneIcon from '@/assets/icons/crane.svg'
import cameraIcon from '@/assets/icons/camera.svg'
import videoCameraIcon from '@/assets/icons/video-camera.svg'

export default {
    components: {
        oilDerrickIcon,
        mapIcon,
        plantsIcon,
        factoryIcon,
        truckIcon,
        craneIcon,
        cameraIcon,
        videoCameraIcon,
    },
    name: 'UsageOfBAS',
    data() {
        return {
            usageItems: [
                { title: 'Нефтегазовая отрасль', link: '/', icon: 'oilDerrickIcon' },
                { title: 'Геодезия и картография', link: '/', icon: 'mapIcon' },
                { title: 'Сельское хозяйство', link: '/', icon: 'plantsIcon' },
                { title: 'Электроэнергетика', link: '/', icon: 'factoryIcon' },
                { title: 'Транспорт', link: '/', icon: 'truckIcon' },
                { title: 'Строительство', link: '/', icon: 'craneIcon' },
                { title: 'Фотосъемка', link: '/', icon: 'cameraIcon' },
                { title: 'Видеосъемка', link: '/', icon: 'videoCameraIcon' }
            ]
        };
    }
};
</script>

<style>
.usage-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.usage-container h2 {
    font-size: 36px;
    font-weight: 600;
    color: var(--color-mute-text);
}

.usage-container .usage-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-top: 20px;
    width: 100%;
}

.usage-container .usage-card {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    width: 100%;
    height: 180px;
    background-color: #f9f9f9;
    border-radius: 25px;
    padding: 20px;
    text-align: center;
    text-decoration: none;
    color: inherit;
    transition: all 0.3s;
}

@media (hover: hover) {
    .usage-container .usage-card:hover {
        background-color: rgba(0, 155, 155, 0.1);
        backdrop-filter: blur(15px);
        transform: translateY(-5px);
    }
}

.usage-container .icon-placeholder {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 64px;
    height: 64px;
    margin-bottom: 10px;
}

.usage-container .icon-placeholder svg{
    display: flex;
    justify-content: center;
    align-items: center;
    width: fit-content;
    height: fit-content;
}

.usage-container .icon-placeholder path{
    width: 100%;
    height: 100%;
    fill: var(--color-btn-green-background);
}

.usage-container .usage-card p {
    font-size: 16px;
    font-weight: 500;
    color: var(--color-black-text);
}

@media (max-width: 1200px) {
    .usage-container .usage-grid {
        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(2, auto) auto;
        grid-column: span 2;
        gap: 20px;
    }

    .usage-container .usage-grid a:nth-child(1),
    .usage-container .usage-grid a:nth-child(2),
    .usage-container .usage-grid a:nth-child(3),
    .usage-container .usage-grid a:nth-child(4) {
        grid-column: span 2;
    }

    .usage-container .usage-grid a:nth-child(5),
    .usage-container .usage-grid a:nth-child(6),
    .usage-container .usage-grid a:nth-child(7),
    .usage-container .usage-grid a:nth-child(8) {
        grid-column: span 1;
    }
}

@media (max-width: 768px) {
    .usage-container .usage-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-top: 20px;
        width: 100%;
    }

    .usage-container .usage-grid a {
        box-sizing: border-box;
        min-width: 150px;
    }

    .usage-container .usage-grid a:nth-child(1),
    .usage-container .usage-grid a:nth-child(2),
    .usage-container .usage-grid a:nth-child(3),
    .usage-container .usage-grid a:nth-child(4) {
        grid-column: span 1;
    }

    .usage-container .usage-grid a:nth-child(5),
    .usage-container .usage-grid a:nth-child(6),
    .usage-container .usage-grid a:nth-child(7),
    .usage-container .usage-grid a:nth-child(8) {
        grid-column: span 1;
    }

    .usage-container .icon-placeholder {
        width: 48px;
        height: 48px;
    }

    .usage-container .usage-grid p {
        text-align: left;
        font-size: 14px;
    }

    .usage-container .usage-grid a {
        display: flex;
    }
    
    .usage-container h2 {
        font-size: 28px;
    }
}

</style>
