<template>
    <header :class="{ 'main-header': true, 'sticky': isSticky }">
        <div class="header-container">
            <nav class="navigation-links">
                <router-link class="link" to="/about">О проекте</router-link>
                <router-link class="link" to="/customers">Клиентам</router-link>
                <router-link class="link" to="/suppliers">Поставщикам</router-link>
                <router-link class="link" to="/programs">Государственные программы</router-link>
                <router-link class="link" to="/partners">Партнеры</router-link>
                <router-link class="link" disabled to="/">Новости</router-link>
            </nav>

            <div class="header-content" ref="headerContent">
                <div class="content-container">
                    <div class="logo-search-container">
                        <div class="logos-container">
                            <NaletayLogo @click="goToHome()" class="org-logo" />
                            <GTLKLogo class="org-logo" style="cursor: default;" />
                        </div>
                    </div>
                    <div class="search-container">
                        <QuickFiltersPanel/>
                        <CustomInput v-model="searchQuery" inputType="search" showSendButton="true" placeholder="Поиск..." @keydown.enter="searchProducts" @send="searchProducts" />
                    </div>
                    <p class="contact-phone">info@naletai.su</p>
                    <div class="contact-profile-container">
                        <div class="profile-icons">
                            <span @click="openProfile" class="icon-btn">
                                <profileIcon/>
                                <span v-if="isAuthenticated === true" class="authed"></span>
                            </span>
                            <span @click="openCart" class="icon-btn cart-icon">
                                <shoperIcon />
                                <span v-if="cartItemsTotal > 0" class="cart-count"></span>
                            </span>
                        </div>
                    </div>
                    <span class="localization-btn" @click="changeLocalization('RU')">
                        <localizationIcon style="margin-right: 10px;" /> RU
                    </span>
                </div>
            </div>
        </div>
    </header>
</template>

<script setup>
import NaletayLogo from '@/assets/icons/logo_naletay.svg';
import GTLKLogo from '@/assets/icons/logo_gtlk.svg';
import profileIcon from '@/assets/icons/profile.svg';
import shoperIcon from '@/assets/icons/shoper.svg';
import localizationIcon from '@/assets/icons/localization.svg';
</script>

<script>
import CustomInput from '@/components/inputs/CustomInput.vue';
import QuickFiltersPanel from '@/components/QuickFiltersPanel.vue';
import { mapGetters, mapActions } from 'vuex';

export default {
    components: {
        CustomInput,
        QuickFiltersPanel
    },
    computed: {
        ...mapGetters('cart', ['cartItemsTotal']),
        ...mapGetters('user', ['currentUser', 'isAuthenticated'])
    },
    data() {
        return {
            authModal: {
                username: '',
                password: ''
            },
            searchQuery: '',
            showQuickFilters: false,
            isSticky: false,
        };
    },
    mounted() {
        document.addEventListener('scroll', this.handleScroll);
    },
    beforeUnmount() {
        document.removeEventListener('scroll', this.handleScroll);
    },
    methods: {
        ...mapActions('user', ['login', 'logout']),
        goToHome() {
            this.$router.push({ name: 'Home' });
        },
        openCart() {
            this.$router.push({ name: 'CartPage' });
        },
        openProfile() {
            window.loginModal.open()
        },
        changeLocalization(localization) {
            alert('Вы сменили локализацию на ' + localization);
        },
        searchProducts() {
            const query = {};
            if (this.searchQuery !== '') {
                query.name = this.searchQuery;
            }
            this.$router.push({ name: 'CatalogPage', query });
        },
        toggleQuickFilters() {
            this.showQuickFilters = !this.showQuickFilters;
        },
        hideQuickFilters() {
            this.showQuickFilters = false;
        },
        handleScroll() {
            this.isSticky = window.scrollY > 0;
        }
    }
};
</script>

<style>
.main-header {
    position: sticky;
    top: 0;
    z-index: 3;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: box-shadow 0.3s ease;
    width: 100%;
    background: var(--color-background);
    box-sizing: border-box
}

.main-header.sticky {
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.header-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-flow: column;
    max-width: 1280px;
    width: 100%;
}

.navigation-links {
    display: flex;
    width: 100%;
    padding: 10px 5px;
    font-size: 14px;
    justify-content: flex-start;
    border-bottom: 1px solid var(--color-border);
}

.navigation-links .link {
    margin-right: 25px;
}

.header-content {
    display: flex;
    justify-content: center;
    width: 100%;
    flex-flow: row wrap;
    align-items: center;
}

.content-container {
    display: flex;
    justify-content: space-between;
    flex-flow: row wrap;
    gap:15px;
    width: 100%;
    max-width: 1280px;
    padding: 15px 15px;
}

.logo-search-container {
    display: flex;
    align-items: center;
}

.logos-container {
    display: flex;
    gap:10px;
    align-items: center;
    min-height: 44px;
}

.org-logo {
    cursor: pointer;
    height: 32px;
}

.icon-btn svg{
    display: flex;
    width: 24px;
    height: 24px;
    position: relative;
}

.cart-count {
    position: absolute;
    background-color: var(--color-background-error);
    color: white;
    border-radius: 50%;
    width: 10px;
    height: 10px;
    font-size: 12px;
    margin-left: 20px;
    margin-bottom: 20px
}

.authed {
    position: absolute;
    background-color: var(--color-background-info);
    color: white;
    border-radius: 50%;
    width: 10px;
    height: 10px;
    font-size: 12px;
    margin-left: 20px;
    margin-bottom: 20px
}

.search-container {
    display: flex;
    align-items: center;
    gap:10px;
    flex: 1;
}

.search-container .custom-input {
    min-width: 280px;
}

.contact-profile-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.contact-phone {
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1rem;
    color: var(--color-black-text);
}

.profile-icons {
    display: flex;
    width: 100%;
    gap:10px;
    align-items: center;
}

.icon-btn {
    cursor: pointer;
}

.localization-btn {
    cursor: pointer;
    display: flex;
    align-items: center;
}

.hamburger {
    width: 38px;
    height: 38px;
}

@media (min-width: 1024px) {
    .navigation-links {
        flex-flow: row wrap;
        justify-content: flex-start;
    }

    .header-content {
        padding: 5px 0px;
        flex-flow: row wrap;
        align-items: flex-start;
        min-height: 88px;
    }

    .contact-phone {
        flex: 0.25;
    }

    .logo-search-container {
        display: flex;
        flex-flow: row wrap;
        align-items: flex-end;
        gap: 10px;
        margin-right: 45px;
    }

    .search-container {
        display: flex;
        align-items: center;
        flex:0.5;
    }

    .contact-profile-container {
        display: flex;
        flex: 0.2;
        flex-flow: row;
        justify-content: space-between;
        align-items: center;
    }

    .profile-icons {
        justify-content: flex-end;
        width: 100%;
    }

}

@media (min-width: 768px) and (max-width: 1020px) {
    .header-content {
        flex-flow: row wrap;
        align-items: flex-start;
    }

    .logo-search-container {
        flex-flow: row wrap;
        align-items: flex-start;
        gap: 10px;
    }

    .search-container {
        width: 100%;
        order: 1;
    }
    
    .contact-profile-container {
        width: 40%;
        justify-content: flex-end;
        align-items: center;
        order: 2;
    }

    .contact-phone {
        display: flex;
        width: 50%;
        justify-content: flex-end;
    }

    .profile-icons {
        justify-content: flex-end;
    }

}

@media (min-width: 480px) and (max-width: 768px) {
    .navigation-links {
        display: none;
    }
s
    .localization-btn {
        display: flex;
    }

    .content-container {
        justify-content: space-between;
    }

    .header-content {
        flex-direction: column;
        align-items: flex-start;
    }

    .logo-search-container {
        width: 40%;
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }

    .search-container {
        width: 100%;
        order: 2;
    }

    .logos-container {
        width: 100%;
        order: 1;
    }
    
    .contact-profile-container {
        width: 20%;
        flex-direction: column;
        align-items: flex-start;
    }

    .contact-phone {
        display: flex;
        width: 10%;
        opacity: 0;
    }

    .profile-icons {
        justify-content: flex-end;
        width: 100%;
    }

    .localization-btn {
        display: none;
    }

}

@media (max-width: 480px) {
    .navigation-links {
        display: none;
    }
    
    .localization-btn {
        display: flex;
    }

    .content-container {
        justify-content: space-between;
    }

    .header-content {
        flex-direction: column;
        align-items: flex-start;
    }

    .logo-search-container {
        width: 40%;
        min-width: 200px;
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }

    .search-container {
        width: 100%;
        order: 2;
    }

    .logos-container {
        width: 100%;
        order: 1;
    }
    
    .contact-profile-container {
        flex-direction: column;
        align-items: flex-start;
    }

    .contact-phone {
        display: none;
    }

    .profile-icons {
        justify-content: flex-start;
        width: 100%;
    }

    .localization-btn {
        display: none;
    }

    .hamburger {
        display: flex;
        order: 0;
    }
}
</style>
