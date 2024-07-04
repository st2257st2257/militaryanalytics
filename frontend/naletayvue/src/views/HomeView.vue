<template>
  <div class="home_container">
    <Carousel :autoScroll="true" :scrollInterval="30000" :path="'home_carusels'" />
    <LinkList type="posts" header="" :buttons="false"/>

    <CommodityList/>
    <ServicesList/>
    <useBasHome/>
    <AboutHome/>
    <LinkList type="news"/>
  </div>
</template>

<script>
import Carousel from '@/components/Carousel.vue';
import CommodityList from '@/components/CommodityList.vue';
import LinkList from '@/components/LinkList.vue';
import ServicesList from '@/components/ServicesList.vue';
import AboutHome from '@/components/HomeComps/AboutHome.vue';
import useBasHome from '@/components/HomeComps/useBasHome.vue';

export default {
  components: {
    Carousel,
    CommodityList,
    ServicesList,
    LinkList,
    AboutHome,
    useBasHome
  },
  name: 'HomeView',
  mounted() {
  },
  methods: {
  }
};
</script>

<style scoped>

.about-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.about-block {
  background-color: #f1f1f1;
  padding: 20px;
  border-radius: 10px;
}

.about-text h3 {
  margin-top: 0;
}

.about-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.about-card {
  flex: 1 1 calc(25% - 20px);
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.about-card .icon {
  width: 40px;
  height: 40px;
  background-color: #cccccc;
  border-radius: 50%;
  margin-bottom: 10px;
}

.mission {
  background-color: #3dc981;
  color: #fff;
}

.development {
  background-color: #f2c94c;
  color: #fff;
}

.communication {
  background-color: #cccccc;
  color: #000;
}

.assortment {
  background-color: #333333;
  color: #fff;
}

.about-stats {
  display: flex;
  justify-content: space-around;
  padding: 20px;
  background-color: #f1f1f1;
  border-radius: 10px;
  margin-top: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-item .icon {
  width: 60px;
  height: 60px;
  background-color: #cccccc;
  border-radius: 50%;
  margin-bottom: 10px;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
}

.home_container {
  display: flex;
  align-items: center;
  text-align: center;
  flex-direction: column;
  height: 100%;
  width: 100%;
  max-width: 1280px;
  padding-top: 15px;
  padding-bottom: 50px;
  box-sizing: border-box;
  gap: 48px;
  margin-bottom: 15px;
  padding: 20px;
}
</style>