<template>
  <div v-show="isVisible" class="modal" @mousedown.self="close">
    <div class="modal-content">
      <header class="modal-header">
        <h2>{{ title }}</h2>
        <span class="close-btn" @click="close">×</span>
      </header>
      <section class="modal-body">
        <slot name="content"></slot>
      </section>
      <footer class="modal-footer">
        <slot name="buttons"></slot>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isVisible = ref(false);

function open() {
    isVisible.value = true;
}

function close() {
    isVisible.value = false;
}

defineExpose({ open, close });
</script>

<script>
export default {
    props: {
        title: {
            type: String,
            required: true
        }
    },
}
</script>

<style scoped>
.modal {
    z-index: 5;
    position: fixed;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    flex-flow: column;
    justify-content: center;
    align-items: center;
    backdrop-filter: blur(2px);
}

.modal-content {
    z-index: 5;
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    width: 95%;
    max-width: 400px;
    height: fit-content;
    margin: 0 25px 0 25px;
}

.modal-body {
    display: flex;
    flex-flow: column;
    width: 95%;
    gap: 5px;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.modal-footer {
    display: flex;
    gap: 15px;
    margin-top: 25px;
}

.close-btn {
    padding-left: 5px;
    padding-right: 5px;
    width: 36px;
    height: 36px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    border-radius: 5px;
    border: none;
    background: #fff;
    font-size: 1.5rem;
    cursor: pointer;
    box-sizing: border-box;
}

.close-btn:active {
    background: rgba(0,0,0,0.05);
}

@media (hover: hover) {
    .close-btn:hover {
        background: rgba(0,0,0,0.05);
    }
}

</style>
  