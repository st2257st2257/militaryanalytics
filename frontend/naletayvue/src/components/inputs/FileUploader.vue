<template>
    <div class="file-uploader" @mouseover="showUpload = true" @mouseleave="showUpload = false">
        <label for="file-upload" class="upload-label">
            <fileUploadIcon class="file-icon upload-icon" />
            <span>{{ file ? file.name : 'Загрузить файл' }}</span>
        </label>
        <div class="file-details" v-if="showUpload && file">
            {{ file ? file.name : 'Не загружен' }}
        </div>
        <input type="file" id="file-upload" @change="onFileUpload" class="file-input" ref="fileInput" />
    </div>
</template>

<script>
import fileUploadIcon from '@/assets/icons/saveFiles.svg';

export default {
    components: {
        fileUploadIcon
    },
    data() {
        return {
            file: null,
            showUpload: false,
        };
    },
    methods: {
        onFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.file = file;
                this.$emit('file-upload', file);
            }
        },
        triggerFileInput() {
            this.$refs.fileInput.click();
        }
    }
};
</script>

<style scoped>
.file-uploader {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    cursor: pointer;
    width: fit-content;
    background: var(--color-btn-icon);
    padding: 5px 15px;
    border-radius: 10px;
}

.file-input {
    display: none;
}

.upload-label {
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: white;
}

.upload-icon {
    width: 32px;
    height: 32px;
}

.upload-button {
    background: var(--color-primary);
    border: none;
    color: white;
    padding: 5px 10px;
    cursor: pointer;
    margin-top: 10px;
    border-radius: 5px;
}

.file-details {
    position: absolute;
    top: 50px;
    left: 0;
    width: 100%;
    background: var(--color-background-soft);
    box-shadow: 0px 5px 10px rgba(0,0,0,0.5);
    border-radius: 10px;
    padding: 10px;
    z-index: 3;
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
