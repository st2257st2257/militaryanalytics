<template>
    <div class="upload-container">
        <div 
        @dragenter.prevent="dragEnter"
        @dragover.prevent="dragOver"
        @dragleave.prevent="dragLeave"
        @drop.prevent="drop"
        :class="{ 'dragging-over': dragging,  'uploading': uploading }"
        class="container_uploading">
            <span class="header_upload">{{ headerText }}</span>
            <label for="fileInput" class="upload-button">
                <upload-icon/>
                <span class="upload-files">
                    <p>{{ uploading && selectedItemName ? 'Идет загрузка' : '' }}</p>
                    {{ selectedItemName }}
                    <b v-if="totalSize">{{ formatSize(totalSize) }}</b>
                </span>
            </label>
            <input id="fileInput" type="file" @change="handleFileChange" ref="fileInput" :disabled="uploading" hidden />
                <div v-if="progress !== 100 && uploading" class="progress-bar-container">
                <div class="progress-bar" :style="{ width: progress + '%' }"></div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed } from 'vue';
import uploadIcon from '@/assets/icons/uploadFile_icon.svg';

export default {
    components: {
        uploadIcon
    },
    setup(props, { emit }) {
    const uploading = ref(false);
    const fileToSave = ref(null);
    const selectedItemName = ref('');
    const dragging = ref(false);
    const totalSize = ref(0);
    const progress = ref(0);

    const formatSize = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            fileToSave.value = file;
            selectedItemName.value = file.name;
            totalSize.value = file.size;
            emit('file-selected', file);
        }
    };

    const clearSelection = () => {
        selectedItemName.value = '';
        fileToSave.value = null;
        totalSize.value = 0;
        progress.value = 0;
        uploading.value = false;
        this.$refs.fileInput.value = null;
    };

    const dragEnter = (event) => {
        dragging.value = true;
    };

    const dragOver = (event) => {
        dragging.value = true;
    };

    const dragLeave = (event) => {
        dragging.value = false;
    };

    const drop = (event) => {
        dragging.value = false;
        const file = event.dataTransfer.files[0];

        if (file) {
            fileToSave.value = file;
            selectedItemName.value = file.name;
            totalSize.value = file.size;
            emit('file-selected', file);
        }
    };

    const headerText = computed(() => {
        return dragging.value ? 'Перетащите файл сюда' : 'Перетащите файл или выберите его';
    });

    return {
        uploading,
        fileToSave,
        selectedItemName,
        dragging,
        totalSize,
        progress,
        formatSize,
        handleFileChange,
        clearSelection,
        dragEnter,
        dragOver,
        dragLeave,
        drop,
        headerText
    };
    }
};
</script>

<style scoped>

.upload-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.container_uploading {
    display: flex;
    flex-flow: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    max-width: 750px;
    height: 450px;
    background: rgb(47, 131, 157, 0.1);
    border: 2px dashed #2F849E;
    backdrop-filter: blur(15.75px);
    border-radius: 10px;
    transition: all 1s ease;
}

.upload-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: all 0.5s ease;
    width: 55%;
    height: 55%;
}

.upload-icon {
    max-width: 250px;
    max-height: 250px;
    transition: all 0.5s ease;
}

.upload-files {
    display: flex;
    position: relative;
    font-size: 1.09rem;
    font-weight: 700;
    transition: all 0.5s ease;
    color: #252525;
}

.upload-files p {
    margin-right: 5px;
    font-size: 1.09rem;
    font-weight: 600;
}

.upload-files b {
    display: flex;
    margin-left: 10px;
    font-size: 0.8rem;
    font-weight: 700;
    color: #636363;
    transition: all 0.5s ease;
}

.progress-bar-container {
    width: 52%;
    height: 40px;
    background: #56727A;
    border: 4px solid #97C2CF;
    border-radius: 5px;
    margin-top: 15px;
    transition: all 0.5s ease;
}

.progress-bar {
    height: 100%;
    background-color: #97C2CF;
    transition: all 0.5s ease;
}

.header_upload {
    display: flex;
    margin-bottom: 35px;
    font-size: 1.4rem;
    text-align: center;
    font-weight: 600;
    color: var(--color-black-text);
    transition: all 0.5s ease;
}

.dragging-over {
    padding: 15px;
    width: 100%;
    height: 100%;
    transition: all 0.5s ease;
}

.dragging-over ~ .container_uploading {
    position: absolute;
    display: flex;
    flex-flow: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    max-width: none;
    height: 100%;
    background: #2f849e1a;
    border: 2px dashed #2F849E;
    backdrop-filter: blur(30.75px);
    border-radius: 10px;
    transition: all 0.5s ease;
}

.uploading .upload-icon {
    max-width: 128px;
    max-height: 128px;
    transition: all 0.5s ease;
}

/* Медиа-запросы для мобильных устройств */
@media (max-width: 768px) {
    .header_upload {
        display: flex;
        margin-bottom: 35px;
        font-size: 1rem;
        text-align: center;
        font-weight: 600;
        color: #000;
        transition: all 0.5s ease;
    }

    .container_uploading {
        display: flex;
        flex-flow: column;
        justify-content: center;
        align-items: center;
        width: 85%;
        height: 100%;
        transition: all 0.5s ease;
    }

    .upload-icon {
        max-width: 90%;
        max-height: 90%;
        transition: all 0.5s ease;
    }

    .upload-files {
        display: flex;
        flex-flow: column;
        justify-content: center;
        align-items: center;
    }

    .progress-bar-container {
        width: 70%;
        transition: all 0.5s ease;
    }
}
</style>
