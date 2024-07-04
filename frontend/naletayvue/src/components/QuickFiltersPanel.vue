<template>
    <span @click="toggleQuickFilters" class="icon-btn hamburger" ref="hamburgerButton">
        <hamburger-icon />
    </span>
    <div v-if="isMenuOpen" class="arrow-container" :style="arrowContainerStyle">
        <svg class="arrow-menu" viewBox="0 0 20 10">
            <polygon points="0,0 30,0 15,25" class="arrow-shape"/>
        </svg>
    </div>
    <div v-if="isMenuOpen" class="menu-container" @click.stop ref="menuContainer" :style="menuStyle">
        <div class="menu">
                <router-link 
                    @click.native="closeMenu" 
                    :to="{ name: 'CatalogPage', query: {type: categoryFilter } }"
                    v-for="category in categories" 
                    :key="category.value" 
                    class="menu-item" 
                    @mouseenter="selectCategory(category.value)" 
                    :class="{ active: selectedCategory === category.value }"
                >
                    <h3>
                    {{ category.label }}
                        <arrowIcon class="arrow-icon" v-if="getSubItems(category.value).length > 0" />
                    </h3>
                </router-link>
        </div>
        <div class="submenu">
            <ul>
                <li v-for="subItem in getVisibleItems()" :key="subItem.text">
                    <router-link @click.native="closeMenu" :to="{ name: 'CatalogPage', query: { ...subItem.query } }">
                        {{ subItem.text }}
                    </router-link>
                </li>
                <span v-if="getSubItems().length > maxItems" @click="toggleShowMore(selectedCategory)" class="show-more">
                    {{ getShowMoreText() }} 
                    <arrowIcon class="arrow-icon green-stroke" :class="arrowDirection" />
                </span>
            </ul>
        </div>
    </div>
</template>


<script>
import { nextTick } from 'vue';
import hamburgerIcon from '@/assets/icons/hamburger.svg';
import arrowIcon from '@/assets/icons/arrow.svg';

export default {
    components: {
        hamburgerIcon,
        arrowIcon
    },
    data() {
        return {
            maxItems: 6,
            isMenuOpen: false,
            selectedCategory: null,
            menuStyle: {},
            arrowContainerStyle: {},
            categories: [
                { label: 'Беспилотники', value: 'commodity' },
                { label: 'По применению', value: 'application' },
                { label: 'По отраслям', value: 'industry' },
                { label: 'Дронопорты', value: 'droneHub' },
                { label: 'Услуги', value: 'service' },
            ],
            items: {
                commodity: {
                    showMore: false,
                    list: [
                        { text: 'Самолет легкий: до 30 кг', query: { type: 'commodity', category: 'Самолет легкий: максимальная взлетная масса до 30 кг' } },
                        { text: 'Самолет средний: от 30 кг до 500 кг', query: { type: 'commodity', category: 'Самолет средний: максимальная взлетная масса от 30 кг до 500 кг' } },
                        { text: 'Вертолет легкий: до 30 кг', query: { type: 'commodity', category: 'Вертолет легкий: максимальная взлетная масса до 30 кг' } },
                        { text: 'Вертолет средний: от 30 кг до 500 кг', query: { type: 'commodity', category: 'Вертолет средний: максимальная взлетная масса от 30 кг до 500 кг' } },
                        { text: 'Вертолет тяжелый: от 500 кг', query: { type: 'commodity', category: 'Вертолет тяжелый: максимальная взлетная масса от 500 кг' } },
                        { text: 'Мультиротор легкий: до 30 кг', query: { type: 'commodity', category: 'Мультиротор легкий: максимальная взлетная масса до 30 кг' } },
                        { text: 'Мультиротор средний: от 30 кг до 500 кг', query: { type: 'commodity', category: 'Мультиротор средний: максимальная взлетная масса от 30 кг до 500 кг' } },
                        { text: 'Мультиротор тяжелый: от 500 кг', query: { type: 'commodity', category: 'Мультиротор тяжелый: максимальная взлетная масса от 500 кг' } },
                        { text: 'Образовательные: до 1 кг', query: { type: 'commodity', category: 'Образовательные: максимальная взлетная масса до 1 кг' } }
                    ]
                },
                service: {
                    showMore: false,
                    list: [
                        { text: 'Логистика', query: { type: 'service', category: 'Логистика' } },
                        { text: 'Мониторинг', query: { type: 'service', category: 'Мониторинг' } },
                        { text: 'Сельское хозяйство', query: { type: 'service', category: 'Сельское хозяйство' } },
                        { text: 'Аэрофотосъемка', query: { type: 'service', category: 'Аэрофотосъемка' } },
                        { text: 'Дистанционное зондирование', query: { type: 'service', category: 'Дистанционное зондирование' } },
                        { text: 'Образование', query: { type: 'service', subcategory: 'Образование' } },
                        { text: 'Поиск и спасание', query: { type: 'service', subcategory: 'Поиск и спасание' } },
                        { text: 'Сельское хозяйство', query: { type: 'service', subcategory: 'Сельское хозяйство' } },
                        { text: 'Лесное хозяйство', query: { type: 'service', subcategory: 'Лесное хозяйство' } },
                        { text: 'Атомная промышленность', query: { type: 'service', subcategory: 'Атомная промышленность' } },
                        { text: 'Добыча полезных ископаемых', query: { type: 'service', subcategory: 'Добыча полезных ископаемых' } },
                        { text: 'Электроэнергетика', query: { type: 'service', subcategory: 'Электроэнергетика' } },
                        { text: 'ЖКХ', query: { type: 'service', subcategory: 'ЖКХ' } },
                        { text: 'Наука', query: { type: 'service', subcategory: 'Наука' } },
                        { text: 'ЧС и безопасность', query: { type: 'service', subcategory: 'ЧС и безопасность' } },
                        { text: 'Экология', query: { type: 'service', subcategory: 'Экология' } },
                        { text: 'Инновации', query: { type: 'service', subcategory: 'Инновации' } }
                    ]
                },
                application: {
                    showMore: false,
                    list: [
                        { text: 'Логистика', query: { type: 'commodity', mainPurposes: 'Логистика' }, categories: ['commodity', 'service'] },
                        { text: 'Мониторинг', query: { type: 'commodity', mainPurposes: 'Мониторинг' }, categories: ['commodity', 'service'] },
                        { text: 'Сельское хозяйство', query: { type: 'commodity', mainPurposes: 'Сельское хозяйство' }, categories: ['commodity', 'service'] },
                        { text: 'Аэрофотосъемка', query: { type: 'commodity', mainPurposes: 'Аэрофотосъемка' }, categories: ['commodity', 'service'] },
                        { text: 'Дистанционное зондирование', query: { type: 'commodity', mainPurposes: 'Дистанционное зондирование' }, categories: ['commodity', 'service'] },
                        { text: 'Образование', query: { type: 'commodity', mainPurposes: 'Образование' }, categories: ['commodity', 'service'] },
                        { text: 'Поиск и спасание', query: { type: 'commodity', mainPurposes: 'Поиск и спасание' }, categories: ['commodity', 'service'] }
                    ]
                },
                industry: {
                    showMore: false,
                    list: [
                        { text: 'Сельское хозяйство', query: { type: 'commodity', mainBranches: 'Сельское хозяйство' }, categories: ['commodity', 'service'] },
                        { text: 'Лесное хозяйство', query: { type: 'commodity', mainBranches: 'Лесное хозяйство' }, categories: ['commodity', 'service'] },
                        { text: 'Атомная промышленность', query: { type: 'commodity', mainBranches: 'Атомная промышленность' }, categories: ['commodity', 'service'] },
                        { text: 'Добыча полезных ископаемых', query: { type: 'commodity', mainBranches: 'Добыча полезных ископаемых' }, categories: ['commodity', 'service'] },
                        { text: 'Электроэнергетика', query: { type: 'commodity', mainBranches: 'Электроэнергетика' }, categories: ['commodity', 'service'] },
                        { text: 'ЖКХ', query: { type: 'commodity', mainBranches: 'ЖКХ' }, categories: ['commodity', 'service'] },
                        { text: 'Наука', query: { type: 'commodity', mainBranches: 'Наука' }, categories: ['commodity', 'service'] },
                        { text: 'ЧС и безопасность', query: { type: 'commodity', mainBranches: 'ЧС и безопасность' }, categories: ['commodity', 'service'] },
                        { text: 'Экология', query: { type: 'commodity', mainBranches: 'Экология' }, categories: ['commodity', 'service'] },
                        { text: 'Инновации', query: { type: 'commodity', mainBranches: 'Инновации' }, categories: ['commodity', 'service'] }
                    ]
                },
                droneHub: {
                    showMore: false,
                    list: [
                    ]
                }
            }
        };
    },
    computed: {
        categoryFilter() {
            if (['industry', 'application'].includes(this.selectedCategory) != false) {
                return 'all'
            } else {
                return this.selectedCategory
            }
        },
        arrowDirection() {
            if (!this.selectedCategory) return 'bottom';
            return this.items[this.selectedCategory].showMore ? 'top' : 'bottom';
        }
    },
    methods: {
        toggleQuickFilters(event) {
            this.isMenuOpen = !this.isMenuOpen;
            if (this.isMenuOpen) {
                this.openMenu(event);
                document.addEventListener('click', this.handleOutsideClick);
            } else {
                document.removeEventListener('click', this.handleOutsideClick);
            }
        },
        selectCategory(category) {
            this.selectedCategory = category;
        },
        getSelectedCategoryText() {
            const category = this.categories.find(cat => cat.value === this.selectedCategory);
            return category ? category.label : '';
        },
        getSubItems(category = this.selectedCategory) {
            return category ? this.items[category].list : [];
        },
        closeMenu() {
            this.isMenuOpen = false;
            this.selectedCategory = null;
            document.removeEventListener('click', this.handleOutsideClick);
        },
        openMenu(event) {
            nextTick(() => {
                const buttonRect = this.$refs.hamburgerButton.getBoundingClientRect();
                const menuContainer = this.$refs.menuContainer;
                const menuWidth = menuContainer.offsetWidth;
                const menuHeight = menuContainer.offsetHeight;
                const viewportWidth = window.innerWidth;
                const viewportHeight = window.innerHeight;

                let top = buttonRect.bottom + 10;
                let left = buttonRect.left + (buttonRect.width / 2) - (menuWidth / 2);

                if (left < 10) left = 10;
                if (left + menuWidth > viewportWidth - 10) left = viewportWidth - menuWidth - 10;
                if (top + menuHeight > viewportHeight - 10) top = viewportHeight - menuHeight - 10;

                this.menuStyle = { top: `${top + 5}px`, left: `${left}px` };
                this.arrowContainerStyle = { top: `${buttonRect.bottom + 15}px`, left: `${buttonRect.left + (buttonRect.width / 2) - 5.5}px` };

                this.selectedCategory = 'commodity';
                window.addEventListener('resize', this.handleWindowResize);
            });
        },
        handleWindowResize() {
            this.closeMenu();
        },
        handleOutsideClick(event) {
            if (!this.$refs.menuContainer.contains(event.target) && !this.$refs.hamburgerButton.contains(event.target)) {
                this.closeMenu();
            }
        },
        toggleShowMore(category) {
            if (!category) return;
            this.items[category].showMore = !this.items[category].showMore;
        },
        getVisibleItems() {
            if (!this.selectedCategory) return [];
            const items = this.getSubItems();
            const showMore = this.items[this.selectedCategory].showMore;
            return showMore ? items : items.slice(0, this.maxItems);
        },
        getShowMoreText() {
            if (!this.selectedCategory) return 'Еще';
            return this.items[this.selectedCategory].showMore ? 'Свернуть' : 'Еще';
        }
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.handleWindowResize);
        document.removeEventListener('click', this.handleOutsideClick);
    }
};
</script>


<style scoped>
.menu-container {
    position: absolute;
    display: flex;
    flex-direction: row;
    background-color: white;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 90%;
    max-width: 750px;
    min-height: 300px;
    border-radius: 15px;
    overflow: hidden;
    z-index: 3;
    transition: none;
}

.menu {
    display: flex;
    padding: 10px;
    flex-direction: column;
    width: 40%;
    gap:8px;
    background: #F8F9FA;
    font-size: 14px;
    position: relative;
}

.menu-item {
    width: 100%;
    cursor: pointer;
    padding: 10px 30px;
    position: relative;
    color: #343A40;
    font-size: 14px;
}

.menu-item.active{
    border-radius: 50px;
    background: #E8ECF0;
}

.menu-item h3 {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin: 0;
}

.arrow-container {
    position: absolute;
    width: 20px;
    height: 10px;
    z-index: 4;
    transform: rotate(180deg);
    transition: none;
}

.show-more {
    cursor: pointer;
    font-weight: 500;
    color: var(--color-btn-green-background);
}

.arrow-menu {
    width: 20px;
    height: 10px;
    overflow: visible;
}

.arrow-icon {
    width: 14px;
    height: 14px;
}

.arrow-shape {
    fill: white;
    filter: drop-shadow(0px 8px 4px rgba(0, 0, 0, 0.05));
}

.submenu {
    width: 60%;
    display: flex;
    flex-direction: column;
    padding: 10px;
    font-size: 14px;
}

.submenu h3 {
    margin: 0 0 8px 0;
}

.submenu ul {
    list-style-type: none;
    padding: 0;
    margin: 0;
}

.submenu ul li {
    margin: 4px 0;
}

.submenu ul li a {
    text-decoration: none;
    color: #7E858C;
}

.submenu ul li a:hover {
    color: black;
    text-decoration: none;
}

.arrow-icon.bottom {
    width: 10px;
    height: 10px;
    transform: rotate(90deg);
}

.arrow-icon.top {
    width: 10px;
    height: 10px;
    transform: rotate(-90deg);
}

@media (max-width: 768px) {
    .menu-container {
        flex-direction: column;
        align-items: center;
    }
    .menu, .submenu {
        width: 100%;
    }
    .arrow-container {
        top: 30px;
    }

    .arrow-shape {
        fill: #F8F9FA;
        filter: drop-shadow(0px 8px 4px rgba(0, 0, 0, 0.05));
    }

}
</style>
