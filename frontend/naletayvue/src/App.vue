<template>
  <section class="window-program">
    <HeaderMenu v-if="showHeaderFooter" />
    <main class="main-container">
      <Breadcrumbs v-if="showHeaderFooter" />
      <router-view v-slot="{ Component }">
        <component :is="Component" />
        <button class="btn green-btn help-me" @click="openHelpMenu">?</button>
      </router-view>
    </main>
    <FooterMenu v-if="showHeaderFooter" />
    <LoginModal />
    <ContactForm />
    <LeasingForm />
    <ConfirmModal />
    <GlobalNotificationDisplay />
  </section>
</template>

<script>
import { inject, computed } from 'vue';
import { useRoute } from 'vue-router';
import HeaderMenu from '@/components/Header.vue';
import FooterMenu from '@/components/Footer.vue';
import LoginModal from '@/components/modals/LoginModal.vue';
import ContactForm from '@/components/modals/ContactForm.vue';
import LeasingForm from '@/components/modals/LeasingForm.vue';
import ConfirmModal from '@/components/modals/ConfirmModal.vue';
import GlobalNotificationDisplay from '@/components/GlobalNotificationDisplay.vue';
import Breadcrumbs from '@/components/BreadCrumbs.vue';

export default {
  components: {
    HeaderMenu,
    FooterMenu,
    LoginModal,
    ContactForm,
    LeasingForm,
    ConfirmModal,
    Breadcrumbs,
    GlobalNotificationDisplay
  },
  setup() {
    const notificationManager = inject('notificationManager');
    const chatsManager = inject('chatsManager');
    const route = useRoute();
    
    const showHeaderFooter = computed(() => {
      return route.name !== 'Placeholder';
    });

    window.notificationManager = notificationManager;
    window.chatsManager = chatsManager;
    
    window.alert = function(message) {
      notificationManager.addNotification('info', message, 3000, true);
    };

    return {
      showHeaderFooter
    };
  },
  methods: {
    openHelpMenu() {
      window.contactModal.open()
    }
  }
};
</script>

<style scoped>
.window-program {
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
}

.main-container {
  margin: 0;
  padding: 0;
  margin-top: 25px;
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-flow: column;
  align-items: center;
  box-sizing: border-box;
}

.help-me {
  position: fixed;
  right: 25px;
  bottom: 15px;
  z-index: 10;
  width: 52px;
  height: 52px;
  padding: 0;
}

</style>
