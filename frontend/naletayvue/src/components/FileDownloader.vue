<template>
    <div @click="handleDownloadClick" class="filedownloader_container">
        <div class="progress-circle">
            <svg viewBox="0 0 100 100">
                <circle class="progress-circle-background" cx="50" cy="50" r="45"></circle>
                <circle class="progress-circle-progress" cx="50" cy="50" r="45" :style="{ strokeDasharray: circleDasharray, strokeDashoffset: circleDashoffset }"></circle>
                <!-- Иконка -->
                <g class="download-icon" fill="none" v-if="!downloading">
                    <path d="M38.25 31.25L38.25 57.25" stroke="white" stroke-width="5" stroke-linecap="round"/>
                    <path d="M28.5 47.5L38.25 57.25L48 47.5" stroke="white" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M15.6462 47.5C-1.93601 47.5 -1.93588 21.5018 15.9717 21.5018C15.9777 14.7694 19.298 8.22382 25.2328 4.61555C34.0891 -0.768834 45.4135 2.42658 50.5266 11.7526C59.9007 11.7526 67.5 19.7549 67.5 29.6263C67.5 35.6712 64.6504 41.0153 60.2886 44.25" stroke="white" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
                </g>
            </svg>
            <div v-if="downloading" class="progress-text">{{ progress }}%</div>
        </div>

        <div class="file-info">
            <p>Нажмите чтобы начать загрузку</p>
            <!--TODO-->
            <!-- <p>Имя файла: {{ fileName }}</p> -->
            <!-- <p>Расширение файла: {{ fileExtension }}</p> -->
            <!-- <p>Размер файла: {{ formattedFileSize }}</p> -->
            <!-- <p>Статус: {{ status }}</p> -->
        </div>
    </div>
</template>

<script>
import downloadIcon from '@/assets/icons/download.svg'

export default {
    components: {
        downloadIcon
    },
    props: {
        fileUrl: String
    },
    data() {
        return {
            status: 'Не начата',
            progress: 0,
            fileSize: 0,
            formattedFileSize: '',
            fileExtension: '',
            fileName: '',
            circleDasharray: '283',
            circleDashoffset: '283',
            downloading: false
        };
    },
    async created() {
        await this.getFileSize();
    },
    methods: {
        async getFileSize() {
            try {
                const response = await fetch(this.fileUrl, { method: 'HEAD' });
                const contentLength = response.headers.get('Content-Length');
                const contentType = response.headers.get('Content-Type');
                const fileName = response.headers.get('Content-Disposition').split('filename=')[1].replace(/"/g, '');

                this.fileSize = parseFloat(contentLength) || 0;
                this.formattedFileSize = this.formatFileSize(this.fileSize);
                this.fileExtension = this.getFileExtension(fileName);
                this.fileName = fileName;
            } catch (error) {
                console.error('Ошибка получения данных о файле:', error);
            }
        },
        async handleDownloadClick() {
            /*
            if (!this.downloading) {
                await this.downloadFile();
            } else {
                this.openDownloadedFile();
            }*/
            window.open(this.fileUrl, '_blank');
        },
        async downloadFile() {
            try {
                const response = await fetch(this.fileUrl);
                const reader = response.body.getReader();
                let receivedLength = 0;
                this.downloading = true;
                this.status = 'Загрузка начата';
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) {
                        break;
                    }
                    receivedLength += value.length;
                    this.progress = Math.floor((receivedLength / this.fileSize) * 100);
                    this.updateProgressCircle();
                }
                this.status = 'Загрузка завершена';
            } catch (error) {
                console.error('Ошибка загрузки файла:', error);
                this.status = 'Ошибка загрузки';
            } finally {
                this.downloading = false;
            }
        },
        openDownloadedFile() {
            const extension = this.getFileExtension(this.fileName).toLowerCase();
            const supportedExtensions = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'];
            if (supportedExtensions.includes(extension)) {
                window.open(this.fileUrl, '_blank');
            } else {
                this.downloadFile();
            }
        },
        updateProgressCircle() {
            const progress = this.progress / 100;
            const circumference = Math.PI * 2 * 45;
            this.circleDashoffset = (circumference * (1 - progress)).toFixed(2);
        },
        formatFileSize(size) {
            if (size === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
            const i = Math.floor(Math.log(size) / Math.log(k));
            return parseFloat((size / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },
        getFileExtension(fileName) {
            return fileName.split('.').pop();
        }
    }
};
</script>

<style scoped>
.filedownloader_container {
    cursor: pointer;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    flex-flow: row;
    padding: 10px;
    border-radius: 10px;
    background: var(--color-background-soft);
    margin-bottom: 5px;
}

.download-icon {
    transform: translate(32%, 35%) scale(0.5);
}

.filedownloader_container:hover .download-icon{
    transform: translate(22%, 27%) scale(0.8);
}

.download-icon path {
    stroke: #e6e6e6;
    transition: stroke 0.3s ease;
}

.filedownloader_container:hover .download-icon path {
    stroke: #ccc;
}

.progress-circle {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    width: 100px;
    height: 100px;
}

.progress-circle svg {
    width: 100%;
    height: 100%;
}

.progress-circle circle {
    fill: none;
    stroke-width: 6;
}

.progress-circle-background {
    stroke: #e6e6e6;
}

.progress-circle-progress {
    stroke: var(--color-btn-green-background);
    stroke-linecap: round;
}


.progress-text {
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    border-radius: 100%;
    width: 90%;
    height: 90%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 16px;
    font-weight: bold;
    background: rgba(255,255,255,.25);
}

.file-info {
    display: flex;
    padding-left: 15px;
    flex-direction: column;
}
</style>
