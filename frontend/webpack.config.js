const path = require("path");
const webpack = require("webpack");

module.exports = {
  // where is the entry js file??
  entry: "./src/index.js",
  // where should we output this file to?
  output: {
    // path.resolve(__dirname) -> it gets us the current directory
    path: path.resolve(__dirname, "./static/frontend"),
    filename: "[name].js",
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
    ],
  },
  optimization: {
    // if the js file is too big, it's going to take a lot of time to load on web browser
    // so it minimizes it by removing all the white blank and such in the file
    minimize: true,
  },
  plugins: [
    new webpack.DefinePlugin({
      "process.env": {
        // This has effect on the react lib size
        NODE_ENV: JSON.stringify("production"),
      },
    }),
  ],
};
