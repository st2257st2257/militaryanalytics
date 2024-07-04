<template>
    <div class="logo-uploader" @mouseover="showUpload = true" @mouseleave="showUpload = false">
        <img v-if="logoUrl" :src="logoUrl" alt="Company Logo" class="logo"/>
        <div v-if="isEditMode && showUpload" class="upload-overlay">
            <input type="file" id="file-upload" accept="image/*" @change="onLogoUpload" class="file-input"/>
            <label for="file-upload" class="upload-label">Загрузить логотип</label>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        logoUrl: {
            type: String,
            required: false
        },
        isEditMode: {
            type: Boolean,
            required: true
        }
    },
    data() {
        return {
            showUpload: false
        };
    },
    methods: {
        onLogoUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.$emit('logo-upload', file);
            }
        }
    }
};
</script>

<style scoped>
.logo-uploader {
    position: relative;
    width: 256px;
    height: 256px;
    margin-left: 20px;
    padding: 10px;
    text-align: right;
    border-radius: 100%;
    order: 2;
    background: var(--color-background);
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

.logo {
    width: 60%;
    height: 60%;
    object-fit: contain;
}

.upload-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
}

.file-input {
    display: none;
}

.upload-label {
    cursor: pointer;
    color: white;
    font-size: 16px;
}

.upload-label:hover {
    text-decoration: underline;
}
</style>
