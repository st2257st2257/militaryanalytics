<template>
  <div class="news_item" :key="item.id">
    <a :href="item.buttonLink">
      <div class="news_image" :style="{ backgroundImage: `url(${item.image})` }"></div>
    </a>
    <div class="news_details">
      <h3><a style="color: var(--color-black-text);" :href="item.buttonLink">{{ truncatedTitle }}</a></h3>
      <p><a style="color: var(--color-black-text);" :href="item.buttonLink">{{ item.content }}</a></p>
      <p style="margin-top: 15px;">{{ item.date }}</p>
      <div class="news_buttons">
        <a v-if="item.buttonLink" :href="item.buttonLink" class="btn transparent-btn">{{ item.buttonText }}</a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    item: Object,
  },
  computed: {
    truncatedTitle() {
      return this.item.title.length > 50 ? this.item.title.slice(0, 50) + '...' : this.item.title;
    },
  },
};
</script>

<style scoped>
.news_item {
  display: flex;
  width: 100%;
  min-width: 104px;
  min-height: 215px;
  max-height: 215px;
  border-radius: 35px;
  background: var(--color-background-soft);
  overflow: hidden;
  justify-content: space-between;
}

.news_image {
  height: 100%;
}

.news_item > a {
  width: 45%;
  height: 100%;
}

.news_details {
  width: 60%;
  height: 100%;
  padding: 20px;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: flex-start;
}

.news_item:hover {
  box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
}

.news_image {
  width: 100%;
  height: 100%;
  min-height: 215px;
  background-position: 50% 50%;
  background-size: cover;
  object-fit: cover;
}

.news_details h3 {
  cursor: pointer;
  font-size: 20px;
  font-weight: 500;
  line-height: 28.8px;
  letter-spacing: -0.02em;
  text-align: left;
  margin-bottom: 10px;
}

.news_details p {
  font-size: 14px;
  font-weight: 400;
  line-height: 16.8px;
  letter-spacing: -0.02em;
  text-align: left;
}

.news_buttons {
  display: flex;
  align-items: center;
  flex-flow: row wrap;
  gap: 15px;
  margin-top: auto;
}

.news_buttons .transparent-btn {
  height: fit-content;
  min-height: 0;
}
/* Media queries for responsiveness */

@media (min-width: 1024px) {
  .news_item {
    display: flex;
    width: 100%;
    min-height: 225px;
    max-height: 225px;
    border-radius: 40px;
    background: var(--color-background-soft);
    display: flex;
    overflow: hidden;
    justify-content: space-between;
  }

  .news_details {
    width: 60%;
    height: 100%;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
  }
}
</style>
