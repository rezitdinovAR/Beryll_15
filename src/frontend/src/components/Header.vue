<template>
    <div v-if="isUploading"
         class="position-fixed container h-100 d-flex align-items-center justify-content-center bg-dark-color-div"
         style="z-index: 10000; min-width: 100%">
        <div
            class="mb-3 p-5 bg-dark-color rounded d-flex gap-1 flex-column justify-content-center align-items-center position-relative modal-border">
            <button class="btn close position-absolute p-0 d-flex align-items-center justify-content-center"
                    aria-label="close" style="top: 20px; right: 20px; width: 20px; height: 20px"
                    @click="isUploading=false">
                <span aria-hidden="true" class="text-white">&times;</span>
            </button>
            <h1 class="text-white">Загрузите ваше видео</h1>
            <form class="col-12 col-lg-auto  position-relative d-flex flex-column align-items-center"
                  @submit.prevent="fetchUploadData">
                <input v-model="uploadDescription"
                       class="form-control form-control-dark bg-gray-color text-white mb-3"
                       style="min-width: 50vw"
                       placeholder="Описание..."
                       aria-label="Описание">
                <input v-model="uploadLink"
                       class="form-control form-control-dark bg-gray-color text-white mb-3"
                       placeholder="Ссылка на видео..."
                       aria-label="Ссылка на видео">
                <button type="button" class="btn btn-outline-light me-2 primary d-flex align-items-center"
                        @click="fetchUploadData">
                    <span v-if="uploadData.loading" class="loader" style="width: 25px; height: 25px"></span>
                    <span v-else>Загрузить</span>
                </button>
                <p v-if="uploadError" class="text-white mt-2">{{ this.uploadError }}</p>
            </form>
        </div>
    </div>
    <header class="p-3 bg-dark-color text-white position-sticky" style="top: 0; left: 0; z-index: 5000">
        <div class="pt-1 px-4">
            <div class="d-flex flex-wrap align-items-center justify-content-between">
                <div class="d-flex ">
                    <a href="/" class="d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none">
                        <img alt="Yappy logo" fetchpriority="high" width="80" height="24" decoding="async" data-nimg="1"
                             style="color:transparent" src="/logo-full.svg">
                    </a>
                </div>
                <div class="d-flex position-relative">
                    <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3 position-relative" @submit.prevent="fetchData">
                        <input v-model="searchString"
                               type="search"
                               class="form-control form-control-dark bg-gray-color text-white"
                               placeholder="Поиск..."
                               aria-label="Search"
                               @input="isSearching=true"
                               @click="isSearching=true"
                               @submit.prevent="fetchData"
                        >
                        <div
                            class="py-2 px-1 position-absolute border-1 bg-gray-color rounded d-flex justify-content-center w-100"
                            v-if="isSearching"
                            style="top: 60px">
                            <button
                                class="btn close position-absolute p-0 d-flex align-items-center justify-content-center"
                                aria-label="close" style="top: 10px; right: 10px; width: 20px; height: 20px"
                                @click="isSearching=false">
                                <span aria-hidden="true" class="text-white">&times;</span>
                            </button>
                            <button type="button" class="btn btn-outline-dark bg-gray-color mx-3 my-2"
                                    style="margin-top: 30px !important;"
                                    @click="fetchData">
                                Перейти
                                к результатам
                            </button>
                        </div>
                    </form>
                    <div class="text-end">
                        <button type="button" class="btn btn-outline-light me-2 primary" @click="isUploading=true">
                            Загрузить
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </header>

</template>

<script>
import {useSearchStore} from "@/stores/searchStore.js";
import {mapActions, mapWritableState} from "pinia";
import {nextTick} from "vue";
import router from "@/router/router.js";

export default {
    name: "Header",
    data() {
        return {
            isSearching: false,
            isUploading: false,
            uploadDescription: null,
            uploadLink: null,
            uploadError: null
        }
    },
    watch: {
        isUploading(newValue) {
            if (newValue) {
                document.body.classList.add('no-scroll');
            } else {
                document.body.classList.remove('no-scroll');
            }
        },
    },
    methods: {
        ...mapActions(useSearchStore, {
            searchVideosByQuery: "searchVideosByQuery",
            uploadVideo: "uploadVideo"
        }),
        async fetchData() {
            console.log("Button clicked!")
            this.isSearching = false;
            this.videos = []
            await router.push({path: '/video', query: {q: this.searchString}})
        },
        async fetchUploadData() {
            if (!this.uploadDescription || !this.uploadLink) {
                this.uploadError = "Введите описание и ссылку"
                return
            }
            const status = await this.uploadVideo(this.uploadDescription, this.uploadLink);
            console.log(status)
            if (status === 200) {
                this.uploadError = null;
                this.isUploading = false;
            } else {
                this.uploadError = "Произошла ошибка, попробуйте еще раз"
            }
        },
    },
    computed: {
        ...mapWritableState(useSearchStore, {
            requestData: "requestData",
            uploadData: "uploadData",
            searchString: "searchString",
            videos: "videos"
        })
    },
}
</script>

<style lang="scss">

</style>