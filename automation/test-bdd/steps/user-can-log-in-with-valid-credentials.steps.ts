import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { ICustomWorld } from '../world';

Given('the user is on the relevant page', async function (this: ICustomWorld) {
  await this.page!.goto(process.env.BASE_URL!);
});

When('the user performs the action for "User can log in with valid credentials"', async function (this: ICustomWorld) {
  // TODO: implement Playwright action (click, fill, etc.)
});

Then('the expected outcome for "User can log in with valid credentials" is displayed', async function (this: ICustomWorld) {
  // TODO: implement assertion with Playwright
});
