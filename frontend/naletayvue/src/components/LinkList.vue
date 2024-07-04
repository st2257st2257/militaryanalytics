<template>
    <div class="list__container">
        <h2>{{ header }}</h2>
        <ul class="container_news" v-if="!loading">
            <LinkCard
            v-for="(item, index) in visibleItems"
            :key="item.id"
            :item="item"
            />
        </ul>
        <div v-if="loading" class="loading-indicator">Идет загрузка...</div>
        <div class="centred_info" v-if="items.length === 0 && !loading">{{ noItemsMessage }}</div>
        <span class='button__more'>
            <button v-if="buttons" style="margin-top: 25px;" class="btn soft-btn" @click="showMoreItems">Показать еще</button>
        </span>
    </div>
</template>

<script>
import LinkCard from '@/components/cards/LinkCard.vue';
import { linkService } from '@/classes/news/LinkService.js';

export default {
    props: {
        header: {
            type: String,
            default: "Список новостей"
        },
        buttons: {
            type: Boolean,
            default: true
        },
        type: {
            type: String,
            default: "news",
            validator: value => ["news", "posts"].includes(value)
        }
    },
    components: {
        LinkCard
    },
    data() {
        return {
            visibleItemsCount: 3,
            step: 3,
            loading: true
        };
    },
    computed: {
        items() {
            return this.type === "news" ? linkService.getAllNews() : linkService.getAllPosts();
        },
        visibleItems() {
            return this.items.slice(0, this.visibleItemsCount);
        },
        noItemsMessage() {
            return this.type === "news" ? "Тут пока нет новостей :(" : "Тут пока нет постов :(";
        }
    },
    methods: {
        showMoreItems() {
            this.visibleItemsCount += this.step;
        },
        fetchItems() {
            if (this.type === "news") {
                linkService.addNews('В России стартовали испытания системы наблюдения за БПЛА', '', '16 мая 2024', '/img/plug_for_products.jpg');
                linkService.addNews('Россия учтёт индийский опыт развития беспилотной авиации', '', '15 мая 2024', '/img/plug_for_products.jpg');
                linkService.addNews('Ученые ЦАГИ представили инновационную разработку на международном форуме-выставке «Беспилотная авиация – 2024»', '', '14 мая 2024', '/img/plug_for_products.jpg');
            } else {
                linkService.addPost('Услуги аренды беспилотных комплексов', '', '', '/img/service.png', 'Подробнее', '/catalog?category=service');
                linkService.addPost('Индивидуальный запрос по собственной спецификации', '', '', '/img/individual.jpg', 'Подробнее', '/');
                linkService.addPost('Программа ГГЗ', '', '', '/img/ggz_program.jpg', 'Подробнее', '/programs');
            }
            this.loading = false;
        }
    },
    mounted() {
        if (this.loading) {
            this.fetchItems();
        }
    },
    beforeUnmount() {
        linkService.deleteAllNews()
        linkService.deleteAllLinks()
    }
};
</script>

<style scoped>
.container_news {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    width: 100%;
}

.loading-indicator,
.centred_info {
    text-align: center;
    width: 100%;
    margin-top: 20px;
}

.btn.soft-btn {
    display: block;
    padding: 10px 20px;
}

.button__more {
    display: flex;
    width: 100%;
}

@media (max-width: 1024px) {
    .container_news {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 768px) {
    .list__container h2 {
        text-align: center;
    }

    .container_news {
        grid-template-columns: repeat(2, 1fr);
    }

    .btn.soft-btn {
        width: 40%;
    }
}

@media (max-width: 580px) {
    .container_news {
        grid-template-columns: repeat(1, 1fr);
    }

    .btn.soft-btn {
        width: 100%;
    }
}
</style>
