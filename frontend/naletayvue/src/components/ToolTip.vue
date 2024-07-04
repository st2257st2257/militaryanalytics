<template>
    <div style="width: fit-content;" ref="tooltipWrapper" @mouseenter="showTooltip" @mouseleave="hideTooltip" @mousemove="updateArrowPosition" @click="handleClick">
        <slot ref="tooltipForElement"></slot>
        <transition name="fade">
            <div v-if="isVisible" class="tooltip" :style="tooltipStyle">
                <span>{{ text }}</span>
                <div class="arrow" :style="arrowStyle"></div>
            </div>
        </transition>
    </div>
</template>

<script>
export default {
    props: {
        text: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            isVisible: false,
            tooltipStyle: {},
            arrowStyle: {},
            isClicked: false
        };
    },
    methods: {
        showTooltip() {
            this.isVisible = true;
            this.updateTooltipPosition();
        },
        hideTooltip() {
            this.isVisible = false;
            this.isClicked = false;
        },
        handleClick() {
            if (window.innerWidth <= 768) {
                this.isClicked = true;
                this.isVisible = !this.isVisible;
                if (this.isVisible) {
                    this.centerArrow();
                }
            } else {
                this.centerArrow();
            }
        },
        centerArrow() {
            this.$nextTick(() => {
                const wrapper = this.$refs.tooltipForElement;
                const wrapperRect = wrapper.getBoundingClientRect();
                const arrowLeft = `${wrapperRect.width / 2}px`;

                this.arrowStyle = {
                    left: arrowLeft,
                    top: '100%',
                    transform: 'translateX(-50%) rotate(180deg)'
                };
            });
        },
        updateTooltipPosition() {
            this.$nextTick(() => {
                const tooltip = this.$el.querySelector('.tooltip');
                const wrapper = this.$refs.tooltipWrapper;
                const wrapperRect = wrapper.getBoundingClientRect();
                const { innerWidth, innerHeight } = window;
                const tooltipWidth = tooltip.offsetWidth;
                const tooltipHeight = tooltip.offsetHeight;

                let tooltipTop, tooltipLeft, arrowTop, arrowTransform;

                const offset = 10;

                if (wrapperRect.top - tooltipHeight - offset > 0) {
                    tooltipTop = wrapperRect.top - tooltipHeight - offset;
                    tooltipLeft = wrapperRect.left + (wrapperRect.width / 2) - (tooltipWidth / 2);
                    arrowTop = '100%';
                    arrowTransform = 'rotate(180deg)';
                } else if (wrapperRect.bottom + tooltipHeight + offset < innerHeight) {
                    tooltipTop = wrapperRect.bottom + offset;
                    tooltipLeft = wrapperRect.left + (wrapperRect.width / 2) - (tooltipWidth / 2);
                    arrowTop = '-5px';
                    arrowTransform = '';
                } else if (wrapperRect.right + tooltipWidth + offset < innerWidth) {
                    tooltipTop = wrapperRect.top + (wrapperRect.height / 2) - (tooltipHeight / 2);
                    tooltipLeft = wrapperRect.right + offset;
                    arrowTop = '50%';
                    arrowTransform = 'rotate(90deg)';
                } else if (wrapperRect.left - tooltipWidth - offset > 0) {
                    tooltipTop = wrapperRect.top + (wrapperRect.height / 2) - (tooltipHeight / 2);
                    tooltipLeft = wrapperRect.left - tooltipWidth - offset;
                    arrowTop = '50%';
                    arrowTransform = 'rotate(-90deg)';
                } else {
                    tooltipTop = wrapperRect.bottom + offset;
                    tooltipLeft = wrapperRect.left + (wrapperRect.width / 2) - (tooltipWidth / 2);
                    arrowTop = '-5px';
                    arrowTransform = '';
                }

                if (tooltipLeft < offset) {
                    tooltipLeft = offset;
                } else if (tooltipLeft + tooltipWidth > innerWidth - offset) {
                    tooltipLeft = innerWidth - tooltipWidth - offset;
                }
                if (tooltipTop < offset) {
                    tooltipTop = offset;
                } else if (tooltipTop + tooltipHeight > innerHeight - offset) {
                    tooltipTop = innerHeight - tooltipHeight - offset;
                }

                this.tooltipStyle = {
                    top: `${tooltipTop + window.scrollY}px`,
                    left: `${tooltipLeft}px`,
                    maxWidth: `${innerWidth - 2 * offset}px`
                };

                if (this.isClicked) {
                    const wrapperRect = this.$refs.tooltipForElement.getBoundingClientRect();
                    const arrowLeft = `${wrapperRect.width / 2}px`;

                    this.arrowStyle = {
                        left: arrowLeft,
                        top: '100%',
                        transform: 'translateX(-50%) rotate(180deg)'
                    };
                }
            });
        },
        updateArrowPosition(event) {
            if (!this.isClicked) {
                this.$nextTick(() => {
                    const tooltip = this.$el.querySelector('.tooltip');
                    const tooltipRect = tooltip.getBoundingClientRect();
                    const relativeX = event.clientX - tooltipRect.left;

                    const arrowLeft = `${Math.min(Math.max(relativeX, 10), tooltipRect.width - 10)}px`;

                    this.arrowStyle = {
                        left: arrowLeft,
                        top: '100%',
                        transform: 'translateX(-50%) rotate(180deg)'
                    };
                });
            }
        }
    },
    mounted() {
        window.addEventListener('resize', this.hideTooltip);
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.hideTooltip);
    }
};
</script>

<style>
.tooltip {
    position: absolute;
    display: inline-block;
    background: var(--tooltip-background, rgba(0, 0, 0, 0.75));
    color: var(--tooltip-color, white);
    padding: 5px 10px;
    border-radius: 4px;
    white-space: normal;
    font-size: 14px;
    z-index: 3;
    overflow-wrap: break-word;
    width: fit-content;
    max-width: 100%;
}

.tooltip .arrow {
    width: 0;
    height: 0;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid var(--tooltip-arrow-color, rgba(0, 0, 0, 0.75));
    position: absolute;
    transform: rotate(0deg) !important;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity 0.2s;
}

.fade-enter, .fade-leave-to {
    opacity: 0;
}

@media (max-width: 768px) {
    .tooltip {
        width: fit-content !important;
        left: 20px !important;
        right: 20px !important;
    }
}
</style>
