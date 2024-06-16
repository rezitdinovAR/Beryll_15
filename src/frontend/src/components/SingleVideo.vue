<template>
    <div class="px-4 flex-grow-1 d-flex flex-column">
        <div class="d-flex flex-column align-items-center flex-grow-1 justify-content-center">
            <div class="card bg-dark-color border-0 d-flex flex-row justify-content-center flex-grow-1 align-items-center">
                <div v-if="requestData.loading || !currentVideoLink"
                     style="aspect-ratio: calc(9/16)"
                     class="d-flex align-items-center bg-gray-color m-2 rounded is-loading">
                </div>
                <div v-else class="d-flex align-items-start justify-content-center">
                    <video  class="m-2 rounded w-50" :src="currentVideoLink" style="aspect-ratio: calc(9/16)" controls/>
                    <div class="mx-2 my-4 d-flex flex-column">
                        <h2 class="text-white">Описание:</h2>
                        <p v-if="currentVideoDesc" class="text-white mx-1">{{ currentVideoDesc }}</p>
                        <p v-else class="text-white mx-1">Описание отсутствует</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import {mapState, mapWritableState} from "pinia";
import {useSearchStore} from "@/stores/searchStore.js";

export default {
    name: 'Video',
    data() {
        return {
            currentVideoLink: null,
            currentVideoDesc: null
        }
    },
    mounted() {
        const videoId = Number(this.$route.params.id);
        for (let i = 0; i < this.videos.length; i++) {
            if (this.videos[i].ID === videoId) {
                this.currentVideoLink = this.videos[i].url;
                this.currentVideoDesc = this.videos[i].description;
                break;
            }
        }
    },
    computed: {
        ...mapState(useSearchStore, {
            requestData: "requestData",
            videos: "videos"
        })
    }
}
</script>

<style scoped>

</style>