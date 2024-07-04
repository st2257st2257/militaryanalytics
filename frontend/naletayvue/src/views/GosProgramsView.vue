<template>
    <div class="program_container">
      <SingleCarousel :autoScroll="true" :scrollInterval="5000" :singleBanner="true" :path="'programs_carusels'"/>
      <section class="paragraph">
        <h2>Государственный гражданский заказ (ГГЗ)</h2>
        <span class="content">
          <p>
            ГГЗ — это инструмент прямого заказа и поставок БАС для нужд государственных структур и ведомств в рамках национального проекта 
            «Беспилотные авиационные системы», Базовым поставщиком по ГГЗ назначено АО «Государственная транспортная лизинговая компания». 
            Платформа НАЛЕТАЙ.РФ является инструментом АО «ГТЛК» по сбору заявок на участие в данной программе.
          </p>
          <p>
            Если вы отечественный производитель, аккредитованный на участие в программе ГГЗ, и желаете существенно расширить свой охват и клиентскую базу, 
            присоединяйтесь к платформе НАЛЕТАЙ.РФ.
          </p>
          <p>
            Если у вас есть потребность в закупке БАС в рамках программы ГГЗ, просто заполните форму заявки. Наш менеджер свяжется с вами и проконсультирует по дальнейшим шагам.
          </p>
          <button class="btn green-btn" @click="openContactForm()">Отправить заявку на участие ГГЗ</button>
        </span>
      </section>
      <section class="paragraph">
        <h2>ЛЬГОТНЫЙ ЛИЗИНГ</h2>
        <span class="content">
          <p>
            Программа льготного лизинга разработана АО «Государственная транспортная лизинговая компания» действует в рамках национального проекта «Беспилотные авиационные системы». 
            В рамках программы применяется льготная лизинговая ставка от 3,5 до 8,5%, зависящая от ключевой. Срок лизинга от 3 до 5 лет. 
            Авансовый платеж оператора составляет до 30% от стоимости поставляемого в лизинг имущества. 
          </p>
          <p>
            Если вы желаете воспользоваться льготной программой, просто заполните форму заявки. Наш менеджер свяжется с вами и проконсультирует по дальнейшим шагам.
          </p>
          <button class="btn green-btn" @click="openContactForm()">Отправить заявку на участие ГГЗ</button>
        </span>
      </section>
    </div>
</template>

<script>
import SingleCarousel from '@/components/Carousel.vue';

export default {
  components: {
        SingleCarousel,
  },
  methods: {
    openContactForm() {
     window.contactModal.open();
    },
  },
};
</script>

<style scoped>
.program_container {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  max-width: 1280px;
  gap: 80px;
  margin-bottom: 200px;
  padding: 0px 20px;
  box-sizing: border-box;
}

.paragraph h2{
  font-size: 32px;
  font-weight: 500;
}

.paragraph{
  display: flex;
  flex-flow: column;
  gap:15px;
}

.content {
  display: flex;
  flex-flow: column;
  gap: 25px;
}

.content p{
  font-size: 18px;
}
</style>