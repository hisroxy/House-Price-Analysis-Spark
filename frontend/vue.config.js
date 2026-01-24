module.exports = {
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  outputDir: '../house_price_analysis/frontend/dist',
  assetsDir: 'static'
}