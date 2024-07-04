<template>
    <nav class="breadcrumb-container" aria-label="breadcrumb" v-if="showBreadcrumbs.value == true && breadcrumbs.length">
        <ol class="breadcrumb">
            <li class="breadcrumb-item">
                <router-link to="/">Главная</router-link>
            </li>
            <li v-for="(crumb, index) in breadcrumbs" :key="index" class="breadcrumb-item" :class="{ active: index === breadcrumbs.length - 1 }">
                <span style="margin-left: 10px; margin-right: 10px; color: #999;">></span>
                <router-link v-if="index !== breadcrumbs.length - 1" :to="crumb.path">{{ crumb.breadcrumb }}</router-link>
                <span v-else>{{ crumb.breadcrumb }}</span>
            </li>
        </ol>
    </nav>
</template>

<script>
import { reactive, watch } from 'vue';
import { useRoute } from 'vue-router';

export default {
    name: 'Breadcrumbs',
    setup() {
        const route = useRoute();
        const breadcrumbs = reactive([]);
        const showBreadcrumbs = reactive({ value: false });

        const getBreadcrumbs = () => {
            const matched = route.matched.slice();
            const breadcrumbList = [];
            const paramsValues = Object.values(route.params);
            const firstParam = paramsValues.length > 0 ? paramsValues[0] : '';
            let profileAdded = false;

            matched.forEach((route, index) => {
                if (route.meta.breadcrumb) {
                    let breadcrumbText = route.meta.breadcrumb;
                    if (firstParam && breadcrumbText.includes('№')) {
                        breadcrumbText += `${firstParam}`;
                    }
                    breadcrumbList.push({
                        path: route.path,
                        breadcrumb: breadcrumbText
                    });

                    if (route.meta.parent && !profileAdded) {
                        if (route.meta.parent === 'UserProfile') {
                            breadcrumbList.splice(breadcrumbList.length - 1, 0, { path: '/profile', breadcrumb: 'Профиль' });
                            profileAdded = true;
                        }
                    }
                }
            });

            breadcrumbs.splice(0, breadcrumbs.length, ...breadcrumbList);
            showBreadcrumbs.value = matched.some(route => route.meta.showBreadcrumbs);
        };

        watch(
            () => route.fullPath,
                () => {
                    getBreadcrumbs();
                },
            { immediate: true }
        );

        return {
            breadcrumbs,
            showBreadcrumbs
        };
    }
};
</script>

<style scoped>
.breadcrumb-container {
    width: 100%;
    max-width: 1280px;
}

.breadcrumb {
    display: flex;
    flex-wrap: wrap;
    list-style: none;
    margin-bottom: 25px;
    padding-left: 5px;
}

.breadcrumb-item a:hover{
    color: var(--color-btn-green-background);
}

.breadcrumb-item a{
    color: #999;
}

.breadcrumb-item.active {
    color: #1E2028 !important;
}
</style>
