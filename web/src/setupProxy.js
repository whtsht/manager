const { createProxyMiddleware } = require('http-proxy-middleware');
const process = require('process')

module.exports = function(app) {
  app.use(
    '/web',
    createProxyMiddleware({
      target: process.env.APP_SERVER,
    })
  );
};