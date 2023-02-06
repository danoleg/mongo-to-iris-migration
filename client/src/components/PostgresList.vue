<template>
  <div className="md-layout md-gutter" style="max-width: 500px">
    <md-progress-spinner v-if="loading===true" style="margin:0 auto;" md-mode="indeterminate"></md-progress-spinner>
    <TableCard v-for="collect in collections" v-bind:key="collect.name"
                    v-bind:collection="collect"></TableCard>
    <!--        <DoughnutChart data="[40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11]"></DoughnutChart>-->
  </div>
</template>

<script>
import TableCard from './TableCard.vue'
import axios from 'axios';

export default {
  name: "PostgresList",
  data() {
    return {
      collections: [],
      loading: true
    };
  },
  components: {
    // DoughnutChart,
    TableCard
  },
  mounted() {
    let that = this;
    axios.get('http://127.0.0.1:8011/postgresql-tables').then(
        function (response) {
          that.collections = response.data.collections;
          that.loading = false;
        });

  },
}
</script>

<style scoped>

</style>