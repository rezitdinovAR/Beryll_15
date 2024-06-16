<template>
    <div class="px-4 pt-3">
        <h2 class="text-white px-2">{{ headerText }}</h2>
        <p v-if="requestData.status === 404" class="text-white px-2" style="margin-left: 2px">Результатов нет</p>
        <div class="w-100 pt-4">
            <div v-if="!videos || videos.length === 0" class="d-flex flex-row flex-wrap w-100">
                <div v-for="index in [1,2,3,4,5,6,7,8]" :key="index"
                     class="card w-25 bg-dark-color border-0 rounded">
                    <div
                        style="aspect-ratio: calc(9/16)"
                        class="d-flex align-items-center justify-content-center bg-gray-color m-2 rounded is-loading">
                    </div>
                </div>
            </div>
            <div v-else class="d-flex flex-row flex-wrap w-100">
                <div v-for="video in videos" :key="video.id" class="card w-25 bg-dark-color border-0">
                    <router-link :to="{ name: 'Video', params: { id: video.ID }}" class="d-block rounded m-2"
                                 style="background-color: #000; aspect-ratio: calc(9/16); overflow: hidden">
                        <video class="w-100 h-100" :id="video.ID" :src="video.url"
                               @mouseenter="e => e.target.play()"
                               @mouseleave="e => {
                                    e.target.pause();
                                    e.target.currentTime = 0;
                               }" loop muted>
                        </video>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import {mapActions, mapState, mapWritableState} from "pinia";
import {useSearchStore} from "@/stores/searchStore.js";

export default {
    name: "Videos",
    data() {
        return {
            headerText: null,
        }
    },
    methods: {
        ...mapActions(useSearchStore, {
            searchVideosByQuery: "searchVideosByQuery",
            searchPopularVideos: "searchPopularVideos",
        }),
        play() {
            v.play();
        },
        stop() {

        }
    },
    watch: {
        '$route.query.q': function (newValue) {
            if (newValue) {
                this.searchString = newValue;
                this.headerText = `Результаты поиска ${"\"" + this.searchString + "\""}`
                this.searchVideosByQuery(this.searchString)
            } else {
                this.headerText = "Популярные видео";
                this.searchPopularVideos()
            }
        }
    },
    mounted() {
        this.searchString = this.$route.query.q;

        if (this.searchString) {
            this.headerText = `Результаты поиска ${"\"" + this.searchString + "\""}`
            this.searchVideosByQuery(this.searchString)
        } else {
            this.headerText = "Популярные видео";
            this.searchPopularVideos()
        }
    },
    computed: {
        ...mapWritableState(useSearchStore, ["searchString"]),
        ...mapState(useSearchStore, {
            requestData: "requestData",
            videos: "videos"
        })
    }
}

</script>

<style>
</style>