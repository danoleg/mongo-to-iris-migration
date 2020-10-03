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
        <md-button :to="{ name: 'collection', params: { collection: collection.name }}">Open</md-button>
      </md-card-actions>
    </md-card>
</template>

<script>
    export default {
        name: "CollectionCard",
        props: ['collection'],
    }
</script>

<style scoped>

</style>