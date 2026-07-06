import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { ICustomWorld } from '../../world';

Given('the user is on the relevant page', async function (this: ICustomWorld) {
  // e.g., await this.page!.goto(process.env.BASE_URL!);
});

When('the user performs the action for "User sees an error message with invalid credentials"', async function (this: ICustomWorld) {
  // e.g., await this.page!.locator('[data-testid="submit"]').click();
});

Then('the expected outcome for "User sees an error message with invalid credentials" is displayed', async function (this: ICustomWorld) {
  // e.g., await expect(this.page!).toHaveURL('/dashboard');
});
