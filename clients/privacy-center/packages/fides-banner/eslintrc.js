module.exports = {
  extends: [require.resolve("@fidesui/config/eslint"), "preact"],
  root: true,
  settings: {
    "import/resolver": {
      typescript: {},
    },
  },
  plugins: [],
  rules: {},
};
