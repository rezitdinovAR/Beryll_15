<script>

import {defineComponent} from "vue";
import Header from "@/components/Header.vue";

export default defineComponent({
    components: {Header}
})
</script>

<template>
    <Header/>
    <router-view/>
</template>

<style>
</style>
