<template>
    <div class="carousel-container" @mousemove="handleMouseMove">
        <div class="carousel" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
            <div 
                class="carousel-item" 
                v-for="(item, index) in items" 
                :key="index" 
                :style="{ backgroundImage: `url(${getImageUrl(item)})`, backgroundSize: 'cover', backgroundPosition: 'center' }"
            >
                <div class="carousel-content">
                    <label v-if="item.title || item.text" :style="`color: ${item.color || '#000'} !important`">
                        <h3 v-if="item.title" class="carousel-title">{{ item.title }}</h3>
                        <p v-if="item.text" class="carousel-text">{{ item.text }}</p>
                    </label>
                    <button v-if="item.btn" @click="navigateTo(item.link)" :style="`background: ${item.btn.color || '#000'}; color: ${item.btn.textColor || '#fff'}`" class="btn white-btn">{{ item.btn.text }}</button>
                </div>
            </div>
        </div>
        <div v-if="!singleBanner" class="carousel-arrows">
            <div @click="prev" class="arrow left">
                <svg width="100%" height="100%" viewBox="0 0 17 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path :stroke="arrowColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M1 1L16 16L1 31"/>
                </svg>
            </div>
            <div @click="next" class="arrow right">
                <svg width="100%" height="100%" viewBox="0 0 17 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path :stroke="arrowColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M1 1L16 16L1 31"/>
                </svg>
            </div>
        </div>
    </div>
</template>

<script scoped>

export default {
    props: {
        autoScroll: {
            type: Boolean,
            default: false
        },
        scrollInterval: {
            type: Number,
            default: 5000
        },
        singleBanner: {
            type: Boolean,
            default: false
        },
        path: {
            type: String,
            required: true
        }
    },
    computed: {
        arrowColor() {
            if (this.items.length > 0 && this.items[this.currentIndex].color) {
                return this.items[this.currentIndex].color;
            } else {
                return '#fff';
            }
        }
    },
    data() {
        return {
            currentIndex: 0,
            items: [],
            mouseX: 0
        };
    },
    methods: {
        async fetchCarouselData() {
            try {
                const response = await fetch(`src/assets/carousels/${this.path}/carouselData.json`);
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                this.items = await response.json();
            } catch (error) {
                console.error('Error fetching carousel data:', error);
            }
        },
        getImageUrl(item) {
            if (window.innerWidth < 768) {
                return item.mobileImage;
            } else if (window.innerWidth < 1024) {
                return item.tabletImage;
            } else {
                return item.desktopImage;
            }
        },
        prev() {
            this.currentIndex = (this.currentIndex - 1 + this.items.length) % this.items.length;
        },
        next() {
            this.currentIndex = (this.currentIndex + 1) % this.items.length;
        },
        handleMouseMove(event) {
            this.mouseX = event.pageX;
        },
        navigateTo(link) {
            this.$router.push(link);
        },
        startAutoScroll() {
            if (this.autoScroll) {
                setInterval(() => {
                    this.next();
                }, this.scrollInterval);
            }
        }
    },
    mounted() {
        this.fetchCarouselData();
        this.startAutoScroll();
    }
};
</script>

<style>
.carousel-container {
    position: relative;
    overflow: hidden;
    color: #000;
    width: 100%;
    min-height: 360px;
    max-height: 440px;
    height: auto;
    border-radius: 20px;
    color: var(--color-active-text);
}

.carousel {
    z-index: 2;
    display: flex;
    transition: transform 0.5s ease;
    height: auto;
}

.carousel-item {
    position: relative;
    flex: 0 0 100%;
    width: 100%;
    min-height: 360px;
    max-height: 440px;
    height: auto;
    background-size: cover;
    background-position: center;
}

.carousel-bg {
    position: absolute;
    right: 0;
    transform: rotate(30deg);
}

.carousel-content {
    display: flex;
    flex-flow: column;
    justify-content: space-between;
    align-items: flex-start;
    width: 100%;
    height: 100%;
    padding: 45px;
}

.carousel-title {
    text-align: left;
    font-size: 28px;
    max-width: 500px;
    margin-bottom: 10px;
    font-weight: 600;
    line-height: 40px;
}

.carousel-text {
    text-align: left;
    font-size: 14px;
    max-width: 450px;
    margin-bottom: 20px;
}

.carousel-arrows {
    z-index: 1;
    pointer-events: none;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.carousel-container .arrow {
    user-select: none;
    pointer-events: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    height: 100%;
    width: 34px;
    padding: 10px;
    font-size: 18px;
    font-weight: 600;
}

.carousel-container .arrow.left {
    transform: rotate(180deg);
}

.carousel-container .arrow svg {
    width: 32px;
    height: 32px;
}

@media (hover: hover) {
    .carousel-container .arrow:hover {
        background-color: rgba(0,0,0,.1);
    }
}
</style>
