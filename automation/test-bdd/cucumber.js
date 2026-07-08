require('dotenv').config({ path: '.env' });

module.exports = {
  default: {
    require: ['ts-node/register', 'world.ts', 'steps/**/*.steps.ts', 'steps/*.steps.ts'],
    requireModule: ['ts-node/register'],
    paths: ['features/**/*.feature', 'features/*.feature'],
    format: [
      "summary",
      // "progress-bar",
      // 'progress',
      'json:reports/cucumber-report.json',
      "allure-cucumberjs/reporter"
    ],
    formatOptions: {
      snippetInterface: "async-await",
      resultsDir: "allure-results",
    },
    // publishQuiet: true,
    dryRun: false,
  },
};
