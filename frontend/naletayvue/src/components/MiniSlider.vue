<template>
    <div class="mini-slider__container">
        <span class="mini-slider__button mini-slider__button--left" @click="slideLeft">
            <arrowIcon class="mini-slider__arrow mini-slider__arrow--left"/>
        </span>
        <div class="mini-slider__slider-container" @touchstart="startTouch" @touchmove="moveTouch">
            <div class="mini-slider__supplier-logos" :style="{ transform: `translateX(-${currentIndex * (100 / visibleItems)}%)` }">
                <div 
                    class="mini-slider__logo-placeholder" 
                    v-for="(supplier, index) in suppliers" 
                    :key="index">
                    <img :src="supplier.company_logo" alt="Supplier Logo" class="mini-slider__logo-img" />
                </div>
            </div>
        </div>
        <span class="mini-slider__button mini-slider__button--right" @click="slideRight">
            <arrowIcon class="mini-slider__arrow mini-slider__arrow--right"/>
        </span>
    </div>
</template>

<script>
import arrowIcon from '@/assets/icons/arrow.svg'

export default {
    components: {
        arrowIcon
    },
    props: {
        suppliers: {
            type: Array,
            required: true
        },
        visibleItems: {
            type: Number,
            default: 4
        }
    },
    data() {
        return {
            currentIndex: 0,
            startX: 0,
            currentX: 0
        };
    },
    methods: {
        slideLeft() {
            if (this.currentIndex > 0) {
                this.currentIndex--;
            }
        },
        slideRight() {
            if (this.currentIndex < this.suppliers.length - this.visibleItems) {
                this.currentIndex++;
            }
        },
        startTouch(event) {
            this.startX = event.touches[0].clientX;
        },
        moveTouch(event) {
            this.currentX = event.touches[0].clientX;
            const diffX = this.startX - this.currentX;
            if (diffX > 50) {
                this.slideRight();
            } else if (diffX < -50) {
                this.slideLeft();
            }
        }
    }
};
</script>

<style>
.mini-slider__container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    position: relative;
}

.mini-slider__slider-container {
    display: flex;
    align-items: center;
    overflow: hidden;
    width: 90%;
}

.mini-slider__supplier-logos {
    display: flex;
    transition: transform 0.3s ease;
    white-space: nowrap;
}

.mini-slider__logo-placeholder {
    display: inline-block;
    width: 100px;
    height: 50px;
    margin: 10px;
    transition: transform 0.3s ease;
}

.mini-slider__logo-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}

.mini-slider__button {
    background: none;
    border: none;
    font-size: 2em;
    cursor: pointer;
    z-index: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 50px;
    height: 50px;
}

.mini-slider__button--left {
    position: absolute;
    left: 10px;
    transform: rotate(180deg);
}

.mini-slider__button--right {
    position: absolute;
    right: 10px;
    transform: rotate(0deg);
}

.mini-slider__arrow {
    width: 32px;
    height: 32px;
}

.mini-slider__arrow path{
    stroke: var(--color-btn-green-background);
}


.mini-slider__logo-placeholder:hover {
    transform: scale(1.1);
}
</style>
