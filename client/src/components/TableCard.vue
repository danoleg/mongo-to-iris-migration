<template>
    <md-card class="md-primary">
      <md-card-header>
        <md-card-header-text>
          <div class="md-title">{{collection.name}}</div>
        </md-card-header-text>

        <md-card-media>
        </md-card-media>
      </md-card-header>

      <md-card-actions>
        <md-button :to="{ name: 'table', params: { table: collection.name }}">Open</md-button>
      </md-card-actions>
    </md-card>
</template>

<script>
    export default {
        name: "TableCard",
        props: ['collection'],
    }
</script>

<style scoped>

</style>