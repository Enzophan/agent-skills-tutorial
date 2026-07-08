import { Given, When, Then } from "@cucumber/cucumber";
import { expect } from "@playwright/test";
import { ICustomWorld } from "../world";

Given(
  "the user is on the {string} page",
  async function (this: ICustomWorld, string) {
    // Write code here that turns the phrase above into concrete actions
    await this.page?.goto(process.env.BASE_URL!);
    await this.page?.waitForLoadState("domcontentloaded");
    await this.page?.waitForTimeout(1000);
    await expect(this.page?.title()).resolves.toMatch(string);
    return;
  },
);

When(
  "the user clicks on the {string} image.",
  async function (this: ICustomWorld, string) {
    console.log(`Clicking on the ${string} image.`);
    await this.page?.locator("div > a.site-logo > img").click();
    await this.page?.waitForLoadState("domcontentloaded");
    await this.page?.waitForTimeout(1000);
    return;
  },
);

When(
  "the user clicks on the {string} link.",
  async function (this: ICustomWorld, string) {
    console.log(`Clicking on the ${string} link.`);
    await this.page
      ?.locator(
        `.side-bar > nav > ul.default-navigation-links > li > a:has-text("${string}")`,
      )
      .click();
    await this.page?.waitForLoadState("domcontentloaded");
    await this.page?.waitForTimeout(1000);
    return;
  },
);

Then(
  "the user should be redirected to the {string} page",
  async function (this: ICustomWorld, string) {
    console.log(`Verifying that the user is redirected to the ${string} page.`);
    switch (string) {
      case "Home":
        // await expect(this.page?.url()).resolves.toMatch(process.env.BASE_URL!);
        expect(
          await this.page
            ?.locator(".side-bar > nav > ul.default-navigation-links > li")
            .count(),
        ).toBeGreaterThan(10);
        return;
      case "DEV Challenges":
        await expect(this.page?.title()).resolves.toMatch(
          "DEV Online Hackathons and Writing Challenges - DEV Community",
        );
        return;
      default:
        return;
    }
  },
);
