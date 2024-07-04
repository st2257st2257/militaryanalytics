<template>
  <div class="container">
    <div class="sidebar">
        <h2>Меню</h2>
        <ul class="menu">
            <li v-for="item in menuItems" :key="item.title">
                <div v-if="item.submenu" @click="toggleSubmenu(item)" class="menu-item has-submenu" :class="{ 'open': item.open }">
                    {{ item.title }}
                    <span class="arrow" :class="{'open': item.open}">></span>
                </div>
                <router-link
                    v-else-if="!item.disabled"
                    :to="`/profile${item.path}`"
                    class="menu-item"
                    :class="{'disabled': item.disabled}">
                    {{ item.title }}
                </router-link>
                <span v-else class="disabled-link">
                    {{ item.title }}
                </span>
                <ul v-if="item.submenu && item.open" class="submenu">
                    <li v-for="subitem in item.submenu" :key="subitem.title">
                        <router-link class="menu-item"
                            v-if="!subitem.disabled"
                            :to="`/profile${subitem.path}`">
                            {{ subitem.title }}
                        </router-link>
                        <span v-else class="disabled-link">{{ subitem.title }}</span>
                    </li>
                </ul>
            </li>
            <router-link style="margin-top: 25px;  width: 100%; padding: 10px; border-radius: 10px; height: 44px;" class="btn green-btn" :to="`/profile/chat`">
            Чаты
            </router-link>
            <button style="width: 100%; padding: 10px; border-radius: 10px; height: 44px;" class="btn green-btn" @click="openSupportChat">
            Тех. поддержка
            </button>
            <div class="btn exit-btn" @click="logout()">Выйти</div>
        </ul>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { inject } from 'vue';

export default {
  data() {
      return {
          chatsManager: inject('chatsManager'),
          menuItems: [
              { title: 'Профиль', path: '' },
              { title: 'Юридическая информация', path: '/legal-info'},
              { title: 'Ассортимент', path: '/upload' },
              { title: 'Заказы', path: '/orders'},
              { title: 'Настройки', path: '/settings/security'}
          ]
      };
  },
  computed: {
    ...mapGetters('user', ['currentUser', 'isAuthenticated'])
  },
  methods: {
      ...mapActions('user', ['logout']),
      async openSupportChat() {
        const isChatCreated = await this.chatsManager.addChat(this.currentUser.username, 'support');
        if (isChatCreated) {
          const supportChat = await this.chatsManager.getChatByUsers(this.currentUser.username, 'support');
          if (supportChat) {
            this.$router.push({ name: 'Chats', query: { chatId: 'support' } });
          }
        }
      },
      toggleSubmenu(item) {
          if (!item.disabled) {
              item.open = !item.open;
          }
      }
  }
};
</script>

<style scoped>
.container {
  position: relative;
  display: flex;
  gap: 20px;
  width: 32%;
  height: 100vh;
}

.sidebar {
  position: sticky;
  top: 15%;
  width: 20%;
  max-width: 300px;
  min-width: 300px;
  background: var(--color-background-soft);
  padding: 15px;
  border-radius: 15px;
  height: fit-content;
}

.has-submenu {
  max-height: 46px;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 5px;
  list-style-type: none;
  padding: 0;
  margin: 0;
  margin-top: 10px;
}

.menu li {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.menu .menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  width: 100%;
  border-radius: 10px;
  text-decoration: none;
  color: var(--color-btn-text);
  background-color: var(--color-background-hover);
  transition: background-color 0.3s, color 0.3s;
  border: 1px solid rgba(0,0,0,0);
}

.menu .menu-item:hover {
  border: 1px solid var(--color-btn-green-background);
  color: var(--color-text-hover);
}

.menu .menu-item.router-link-exact-active {
  background-color: var(--color-btn-green-background);
  color: var(--color-active-text);
}

.menu .disabled-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  width: 100%;
  border-radius: 10px;
  color: var(--color-btn-text);
  background-color: var(--color-background-hover);
  cursor: not-allowed;
}

.menu .arrow {
  margin-left: auto;
  font-size: 20px;
  transition: transform 0.3s ease;
}

.menu .arrow.open {
  transform: rotate(90deg);
}

.menu .submenu {
  display: flex;
  flex-flow: column;
  gap: 5px;
  padding-left: 15px;
  list-style-type: none;
}

.exit-btn {
  display: flex;
  padding: 10px;
  min-height: 52px;
  border-radius: 10px;
}

.exit-btn:hover {
  color: var(--color-active-text);
  background: var(--color-background-error);
}

@media (max-width: 1024px) { 
  .sidebar {
    width: 100%;
    max-width: none;
    min-width: none;
  }
}
</style>