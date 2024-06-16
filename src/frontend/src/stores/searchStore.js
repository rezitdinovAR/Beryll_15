import {defineStore} from "pinia";
import {apiSearchPopularVideo, apiSearchVideoByQuery, apiUploadVideo} from "@/service/api.js";

export const useSearchStore = defineStore("searchStore", {
    state: () => ({
        videos: [],
        searchString: "",
        uploadData: {
            loading: false,
            status: null,
            error: null
        },
        requestData: {
            loading: false,
            status: null,
            error: null
        }
    }),
    actions: {
        async searchVideosByQuery(query) {
            this.requestData.loading = true;
            try {
                const response = await apiSearchVideoByQuery(query);
                this.requestData.status = response.status
                if (response.status === 200){
                    this.videos = response.data;
                }
            } catch (e) {
                this.requestData.error = e;
            }
            this.requestData.loading = false;
        },
        async searchPopularVideos() {
            this.requestData.loading = true;
            try {
                const response = await apiSearchPopularVideo();
                this.requestData.status = response.status
                if (response.status === 200){
                    this.videos = response.data;
                }
            } catch (e) {
                this.requestData.error = e;
            }
            this.requestData.loading = false;
        },
        async uploadVideo(description, link) {
            this.uploadData.loading = true;
            try {
                const response = await apiUploadVideo(description, link);
                return response.status
            } catch (e) {
                this.uploadData.error = e;
            }
            this.uploadData.loading = false;
        }
    }
})
