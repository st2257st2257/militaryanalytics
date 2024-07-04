<template>
  <div class="service_item" :key="service.id" :service="service">
      <router-link class="service_image" :to="{ name: 'ProductPage', params: { id: service.id }}">
          <img :src="productImageSrc" :alt="service.name">
      </router-link>
      <div class="service_details">
          <h3>{{ service.name.length > 40 ? service.name.substring(0, 40) + '...' : service.name }}</h3>
          <div class="service_buttons">
              <router-link v-if="service.id" :to="{ name: 'ProductPage', params: { id: service.id }}">
                  <button class="btn transparent-btn">Подробнее</button>
              </router-link>
          </div>
      </div>
  </div>
</template>

<script>
export default {
  props: {
      service: Object,
  },
  computed: {
      productImageSrc() {
          if (this.service && this.service.settings && this.service.settings.link1) {
              return this.service.settings.link1.value;
          } else {
              return '';
          }
      },
  },
};
</script>

<style scoped>
@media (min-width: 1024px) {
  .service_item {
    display: flex;
    width: 100%;
    max-width: 625px;
    min-width: 104px;
    min-height: 215px;
    max-height: 215px;
    border-radius: 35px;
    background: var(--color-background-soft);
    overflow: hidden;
    justify-content: space-between;
  }

  .service_details {
    width: 60%;
    height: 100%;
    padding: 15px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    overflow: hidden;
    box-sizing: border-box;
  }
  
  .service_image {
    width: 215px;
    height: 215px;
    overflow: hidden;
  }

  .service_image img {
    width: 50%;
    height: 100%;
    object-fit: contain;
  }
}

.service_item:hover {
    box-shadow: 0px 0px 15px rgba(0,0,0,.2);
}

.service_content {
  display: flex;
  text-align: left;
  justify-content: space-between;
  align-items: flex-start;
  height: 100%;
  border-radius: 25px;
  overflow: hidden;
}

.service_image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.service_details h3 {
  font-size: 20px;
  font-weight: 500;
  line-height: 28.8px;
  letter-spacing: -0.02em;
  text-align: left;
  margin-bottom: 10px;
}

.service_details p {
  font-size: 14px;
  font-weight: 400;
  line-height: 16.8px;
  letter-spacing: -0.02em;
  text-align: left;
}

.service_buttons {
  display: flex;
  align-items: center;
  flex-flow: row wrap;
  gap: 15px;
  margin-top: auto;
}

/* Медиа-запросы для мобильных устройств */
@media (max-width: 1024px) {
  .service_buttons {
    display: flex;
    margin-top: 15px;
  }
  
  .service_image {
    width: 40%;
    height: 250px;
    min-width: 140px;
    min-height: 225px;
    overflow: hidden;
  }

  .service_image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .service_details {
    width: 60%;
    height: 100%;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: flex-start;
  }

  .service_item {
    width: 100%;
    min-width: 104px;
    height: 250px;
    border-radius: 25px;
    background: var(--color-background-soft);
    transition: all 0.25s ease-in-out;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    overflow: hidden;
    transition: all 0.25s ease-in-out;
  }
}
</style>
