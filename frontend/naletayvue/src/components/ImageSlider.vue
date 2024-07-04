<template>
    <div class="image-slider">
        <!-- Основной слайдер -->
        <div class="thumbnails">
            <div v-for="(item, index) in validItems.slice(0, 5)" :key="index" class="thumbnail" :class="{ active: index === selectedIndex }" @click="selectItem(index)">
                <img v-if="isImage(item)" :src="item" :alt="'Thumbnail ' + (index + 1)" />
                <div v-else-if="isVideo(item)" class="video-thumbnail">Видео</div>
            </div>
        </div>
        <div class="main-media">
            <span style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; overflow: hidden;" v-if="isImage(currentItem)" @click.prevent="zoomImage">
                <img :src="currentItem" :alt="'Image ' + (selectedIndex + 1)" />
            </span>
            <iframe v-else-if="isVideo(currentItem)" :src="currentItem" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        </div>

        <!-- Зумированный режим -->
        <div v-if="isZoomed" class="zoomed-view-container" @click.self="closeZoom">
            <div class="zoomed-content" @click.stop>
                <button class="btn error-btn" style="align-self: flex-end;" @click="closeZoom">X</button>
                <div class="zoomed-main-media-container">
                    <div class="arrow left-arrow" @click="prevItem"><arrowIcon/></div>
                    <div class="zoomed-main-media" @click="closeZoom">
                        <img v-if="isImage(currentItem)" :src="currentItem" alt="Zoomed Image" />
                        <iframe v-else-if="isVideo(currentItem)" :src="currentItem" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                    </div>
                    <div class="arrow right-arrow" @click="nextItem"><arrowIcon/></div>
                </div>
                <div class="zoomed-thumbnails">
                    <div v-for="(item, index) in validItems" :key="index" class="thumbnail" :class="{ active: index === selectedIndex }" @click="selectZoomedItem(index)">
                        <img v-if="isImage(item)" :src="item" :alt="'Thumbnail ' + (index + 1)" />
                        <div v-else-if="isVideo(item)" class="video-thumbnail">Видео</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import arrowIcon from '@/assets/icons/arrow.svg'

export default {
    components: {
        arrowIcon
    },
    name: 'ImageSlider',
    props: {
        items: {
            type: Array,
            default: () => []
        },
    },
    data() {
        return {
            selectedIndex: 0,
            isZoomed: false,
            isZoomedIn: false,
        };
    },
    computed: {
        validItems() {
            return this.items.filter(item => this.isImage(item) || this.isVideo(item));
        },
        currentItem() {
            return this.validItems[this.selectedIndex] || '';
        }
    },
    methods: {
        selectItem(index) {
            this.selectedIndex = index;
            this.isZoomed = false;
            this.isZoomedIn = false;
        },
        selectZoomedItem(index) {
            this.selectedIndex = index;
            this.isZoomedIn = false;
        },
        isImage(item) {
            return /\.(jpeg|jpg|gif|png)$/.test(item.toLowerCase());
        },
        isVideo(item) {
            return /\.(mp4|webm|ogg)$/.test(item.toLowerCase());
        },
        zoomImage() {
            if (this.isImage(this.currentItem)) {
                this.isZoomed = true;
                this.isZoomedIn = false;
            }
        },
        closeZoom() {
            this.isZoomed = false;
            this.isZoomedIn = false;
        },
        toggleZoom() {
            this.isZoomedIn = !this.isZoomedIn;
        },
        prevItem() {
            if (this.selectedIndex > 0) {
                this.selectedIndex--;
            } else {
                this.selectedIndex = this.validItems.length - 1;
            }
        },
        nextItem() {
            if (this.selectedIndex < this.validItems.length - 1) {
                this.selectedIndex++;
            } else {
                this.selectedIndex = 0;
            }
        }
    },
};
</script>

<style>
.image-slider {
    display: flex;
    width: 50%;
    align-items: flex-start;
    gap: 10px;
}

.thumbnails {
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: 100%;
    max-width: 64px;
    height: 100%;
    max-height: 368px;
    overflow-y: auto;
}

.thumbnail {
    min-width: 64px;
    min-height: 64px;
    max-width: 64px;
    max-height: 64px;
    width: 100%;
    height: 100%;
    cursor: pointer;
    border: 2px solid transparent;
    border-radius: 5px;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f0f0f0;
}

.thumbnail img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.thumbnail.active {
    border-color: #97C2CF;
}

.main-media {
    flex-grow: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    background: var(--color-background-soft);
    border-radius: 10px;
    width: 100%;
    height: 100%;
    min-height: 360px;
    max-height: 360px;
    overflow: hidden;
}

.main-media img {
    pointer-events: none;
    user-select: none;
    width: 100%;
    height: 100%;
    min-height: 360px;
    object-fit: cover;
    border-radius: 10px;
    cursor: pointer;
}

.main-media iframe {
    width: 100%;
    height: 360px;
    border-radius: 10px;
}

/* Зумированный режим */
.zoomed-view-container {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.9);
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.zoomed-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    max-width: 1280px;
    width: 100%;
    height: 100%;
    gap: 20px;
    padding: 20px;
    position: relative;
}

.zoomed-thumbnails {
    display: flex;
    flex-flow: row;
    gap: 10px;
    width: 100%;
    overflow-x: auto;
    padding-bottom: 20px;
}

.zoomed-thumbnails .thumbnail {
    min-width: 64px;
    min-height: 64px;
    max-width: 100%;
    max-height: 100%;
    width: 64px;
    height: 64px;
}

.zoomed-main-media-container {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    background: var(--color-background-soft);
    border-radius: 10px;
    overflow: hidden;
    width: 100%;
    max-height: 80%;
}

.arrow {
    z-index: 4;
    user-select: none;
    pointer-events: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    height: 100%;
    width: 32px;
    font-size: 28px;
    font-weight: 600;
}

.arrow svg{
    width: 32px;
    height: 32px;
}

.arrow svg path {
    stroke: var(--color-btn-icon);
}

.left-arrow {
    transform: rotate(180deg);
}

@media (hover: hover) {
    .arrow:hover {
        background-color: rgba(0,0,0,.1);
    }
}

.zoomed-main-media {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.zoomed-main-media img,
.zoomed-main-media iframe {
    width: 100%;
    border-radius: 0;
    z-index: 3;
}

.zoomed-main-media img {
    transition: transform 0.3s ease;
}

.zoomed-main-media img.zoomed-in {
    transform: scale(2);
}

@media (max-width: 1320px) { 
    .image-slider {
        width: 100%;
        flex-flow: row;
    }

    .thumbnails {
        flex-direction: column;
        overflow-y: auto;
    }

}


@media (max-width: 540px) { 
    .image-slider {
        width: 100%;
        flex-flow: column;
    }

    .thumbnails {
        flex-direction: row;
        width: 100%;
        max-width: 100%;
        overflow-x: auto;
    }

    .zoomed-content {
        padding: 10px;
    }

    .zoomed-thumbnails {
        flex-direction: row;
        gap: 5px;
        width: 100%;
        overflow-x: auto;
        padding-bottom: 10px;
    }

    .zoomed-thumbnails .thumbnail {
        min-width: 50px;
        min-height: 50px;
        width: 50px;
        height: 50px;
    }

    .arrow {
        font-size: 1.5em;
    }

    .zoomed-main-media-container {
        max-height: 30%;
    }

    .zoomed-main-media img,
    .zoomed-main-media iframe {
        max-width: 100%;
        max-height: 60vh;
    }
}
</style>
