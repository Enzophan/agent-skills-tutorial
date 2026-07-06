import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { ICustomWorld } from '../world';

Given('{{GivenContext}}', async function (this: ICustomWorld) {
  // e.g., await this.page!.goto(process.env.BASE_URL!);
});

When('{{WhenAction}}', async function (this: ICustomWorld) {
  // e.g., await this.page!.locator('[data-testid="submit"]').click();
});

Then('{{ThenOutcome}}', async function (this: ICustomWorld) {
  // e.g., await expect(this.page!).toHaveURL('/dashboard');
});
