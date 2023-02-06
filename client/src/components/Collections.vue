<template>
    <div class="md-layout md-gutter">
        <md-progress-spinner v-if="loading===true" style="margin:0 auto;" md-mode="indeterminate"></md-progress-spinner>
        <p v-if="collections.length === 0 & loading !== true">Collections not found.  Check connection in <a href="/#/settings">settings</a></p>
        <CollectionCard v-for="collect in collections" v-bind:key="collect.name"
                        v-bind:collection="collect"></CollectionCard>
<!--        <DoughnutChart data="[40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]"></DoughnutChart>-->
    </div>
</template>

<script>
    import CollectionCard from './CollectionCard.vue'
    // import DoughnutChart from './DoughnutChart.vue'
    import axios from 'axios';

    export default {
        name: "Collections",
        data() {
            return {
                collections: [],
                loading: true
            };
        },
        components: {
            // DoughnutChart,
            CollectionCard
        },
        mounted() {
            let that = this;
            axios.get('http://127.0.0.1:8011/mongodb-collections').then(
                function (response) {
                    that.collections = response.data.collections;
                    that.loading = false;
                });

        },
    }
</script>

<style scoped>

</style>