require('dotenv').config({ path: '.env' });

module.exports = {
  default: {
    require: ['ts-node/register', 'world.ts', 'steps/**/*.steps.ts', 'steps/*.steps.ts'],
    requireModule: ['ts-node/register'],
    paths: ['features/**/*.feature'],
    format: ['progress', 'json:reports/cucumber-report.json'],
    publishQuiet: true,
  },
};
