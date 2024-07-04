<template>
    <ToolTip ref="tooltip" :text="description">
        <div 
            class="badge" 
            @mouseenter="showTooltip" 
            @mouseleave="hideTooltip"
            @mousemove="updateArrowPosition"
            @click="updateTooltipPosition"
            :class="badgeClass"
        >
            <slot name="icon"></slot>
            <span class="hidden badge-text">{{ text }}</span>
        </div>
    </ToolTip>
</template>

<script>
import ToolTip from './ToolTip.vue';

export default {
    components: {
        ToolTip
    },
    props: {
        text: {
            type: String,
            required: true
        },
        description: {
            type: String,
            required: true
        },
        badgeClass: {
            type: String,
            default: ''
        }
    },
    methods: {
        showTooltip(event) {
            this.$refs.tooltip.showTooltip();
            this.updateTooltipPosition(event);
        },
        hideTooltip() {
            this.$refs.tooltip.hideTooltip();
        },
        updateTooltipPosition(event) {
            this.$refs.tooltip.updateTooltipPosition(event);
        },
        updateArrowPosition(event) {
            this.$refs.tooltip.updateArrowPosition(event);
        }
    }
};
</script>

<style>
.badge-element .badge {
    user-select: none;
    display: flex;
    max-height: 36px;
}

.badge .badge-text {
    display: inline-block;
    white-space: nowrap;
    text-align: left;
}

.badge-icon {
    width: 16px;
    height: 16px;
}

@media (max-width: 768px) {
    .badge .badge-text {
        display: none;
    }
}
</style>
