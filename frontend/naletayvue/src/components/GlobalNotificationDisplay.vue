<template>
    <span class="notification-container" ref="containerRef">
        <transition-group name="notification">
            <div
                v-for="(notification, index) in visibleNotifications"
                :key="`item-${notification.id}`"
                class="notification-item"
                @click="handleClose(notification.id)"
                :style="{ bottom: `${notification.offsetTop}px`, transitionDuration: `${animationDuration}ms` }"
                :class="[ 'notification-item', notification.type, { 'fade-in': notification.appearing, 'fade-out': notification.dismissing } ]"
                ref="notificationItems"
            >
                <span>{{ notification.message }}</span>
                <div class="progress-bar" :style="{ animationDuration: `${notification.duration}ms` }"></div>
            </div>
        </transition-group>
    </span>
</template>

<script>
import { ref, inject, nextTick } from 'vue';

export default {
    setup() {
        const visibleNotifications = ref([]);
        const containerRef = ref(null);
        const notificationItems = ref([]);
        const notificationManager = inject('notificationManager');
        const queue = [];
        const animationDuration = 150;

        const handleNotificationChange = (notifications) => {
            const nonEmptyNotifications = notifications.filter(notification => !!notification.message.trim());

            const removedNotifications = visibleNotifications.value.filter(prev => !nonEmptyNotifications.some(curr => curr.id === prev.id));

            removedNotifications.forEach(removedNotification => {
                const index = visibleNotifications.value.findIndex(notification => notification.id === removedNotification.id);
                if (index !== -1) {
                    animateDismissal(removedNotification.id);
                }
            });

            if (removedNotifications.length >= 0) {
                showNotifications(nonEmptyNotifications);
            }
        };

        const handleClose = (id) => {
            animateDismissal(id);
            setTimeout(() => {
                notificationManager.handleClose(id);
            }, 500);
        };

        const animateDismissal = (id) => {
            const notification = visibleNotifications.value.find(notification => notification.id === id);
            if (notification) {
                notification.dismissing = true;
                setTimeout(() => {
                    visibleNotifications.value = visibleNotifications.value.filter(item => item.id !== id);
                    if (queue.length > 0) {
                        handleNotificationChange(queue.shift());
                    }
                }, 470);
            }
        };

        const showNotifications = async (notifications) => {
            visibleNotifications.value = [...notifications];
            await nextTick();
            
            let offsetTop = 0;
            visibleNotifications.value.forEach((notification, i) => {
                const element = notificationItems.value[i];
                if (element) {
                    notification.offsetTop = offsetTop;
                    offsetTop += element.offsetHeight + 10;
                }
                setTimeout(() => {
                    notification.appearing = true;
                    setTimeout(() => {
                        notification.dismissing = true;
                        handleClose(notification.id);
                    }, notification.duration);
                }, i * animationDuration);
            });
        };

        const handleTransitionEnd = (e) => {
            if (e.target === containerRef.value && queue.length > 0) {
                showNotifications(queue.shift());
            }
        };

        notificationManager.onNotificationsChange(handleNotificationChange);

        return {
            visibleNotifications,
            handleClose,
            containerRef,
            notificationItems,
            handleTransitionEnd,
            animationDuration
        };
    }
};
</script>

<style scoped>
.notification-container {
    width: 100%;
    z-index: 8;
    bottom: 15px;
    pointer-events: none;
    position: fixed;
    display: flex;
    justify-content: flex-end;
    flex-flow: column;
    align-items: center;
    box-sizing: border-box;
    transition: all 0.5s ease-in-out;
    height:100%;
    overflow: hidden;
}

.notification-item {
    cursor: pointer;
    pointer-events: auto;
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    width: 35%;
    max-width: 450px;
    min-width: 300px;
    padding: 20px 20px;
    color: var(--color-active-text);
    transition: all 0.5s ease-in-out;
    opacity: 1;
    box-sizing: border-box;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0px 2px 15px rgba(0,0,0,.1);
}

.notification-item.success {
    background: var(--color-background-success);
}

.notification-item.warning {
    background: var(--color-background-warning);
}

.notification-item.info {
    background: var(--color-background-info);
}

.notification-item.error {
    background: var(--color-background-error);
}

.notification_close {
    cursor: pointer;
    font-size: 22px;
    font-weight: bold;
    margin-right: 15px;
}

.notification-item.fade-in {
    opacity: 1;
    transition: all 0.5s ease-in-out;
}

.notification-item.fade-out {
    opacity: 0;
    transition: all 0.5s ease-in-out;
}

.progress-bar {
    height: 4px;
    background-color: rgba(255, 255, 255, 0.8);
    width: 100%;
    position: absolute;
    bottom: 0;
    left: 0;
    transition: all 0.5s ease-in-out;
    animation: progress-bar-animation 4.5s linear forwards;
}

@keyframes progress-bar-animation {
    0% {
        width: 100%;
    }
    100% {
        width: 0;
    }
}
</style>
