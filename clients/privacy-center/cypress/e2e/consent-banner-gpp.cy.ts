/**
 * The GPP extension is often cached by the Cypress browser. You may need to manually
 * clear your Cypress browser's cache in the Network tab if you are making changes to
 * the source file while also running tests.
 */

/* eslint-disable no-underscore-dangle */
import { CONSENT_COOKIE_NAME, FidesEndpointPaths } from "fides-js";
import { API_URL, TCF_VERSION_HASH } from "../support/constants";
import { mockCookie } from "../support/mocks";
import { stubConfig } from "../support/stubs";

describe("Fides-js GPP extension", () => {
  beforeEach(() => {
    cy.intercept("PATCH", `${API_URL}${FidesEndpointPaths.NOTICES_SERVED}`, {
      fixture: "consent/notices_served_tcf.json",
    }).as("patchNoticesServed");
  });

  it("does not load the GPP extension if it is not enabled", () => {
    cy.fixture("consent/experience_tcf.json").then((experience) => {
      stubConfig({
        options: {
          isOverlayEnabled: true,
          tcfEnabled: true,
          gppEnabled: false,
        },
        experience: experience.items[0],
      });
    });
    cy.waitUntilFidesInitialized().then(() => {
      cy.get("@FidesUIShown").should("have.been.calledOnce");
      cy.get("div#fides-banner").should("be.visible");
      cy.window().then((win) => {
        expect(win.__gpp).to.eql(undefined);
      });
    });
  });

  describe("with TCF and GPP enabled", () => {
    beforeEach(() => {
      cy.fixture("consent/experience_tcf.json").then((experience) => {
        stubConfig({
          options: {
            isOverlayEnabled: true,
            tcfEnabled: true,
            gppEnabled: true,
          },
          experience: experience.items[0],
        });
      });
    });

    it("loads the gpp extension if it is enabled", () => {
      cy.waitUntilFidesInitialized().then(() => {
        cy.get("@FidesUIShown").should("have.been.calledOnce");
        cy.get("div#fides-banner").should("be.visible");
        cy.window().then((win) => {
          win.__gpp("ping", cy.stub().as("gppPing"));
          cy.get("@gppPing")
            .should("have.been.calledOnce")
            .its("lastCall.args")
            .then(([data, success]) => {
              expect(success).to.eql(true);
              expect(data.signalStatus).to.eql("not ready");
            });
        });
      });
    });

    /**
     * Follows the flow documented here for Event Order Example 1:
     * https://github.com/InteractiveAdvertisingBureau/Global-Privacy-Platform/blob/main/Core/CMP%20API%20Specification.md#eventlistener-
     * 1. initial data from stub
     * 2. listenerRegistered
     * 3. cmpStatus = loaded
     * 4. cmpDisplayStatus = visible
     * 5. User makes a choice
     * 6. cmpDisplayStatus = hidden
     * 7. sectionChange = tcfeuv2
     * 8. signalStatus = ready
     */
    it("fires appropriate gpp events for first time user", () => {
      cy.waitUntilFidesInitialized().then(() => {
        cy.get("@FidesUIShown").should("have.been.calledOnce");
        // TODO(PROD#1439): Because the stub is too late right now, we can't listen for events
        // 3 and 4 yet.
        cy.window().then((win) => {
          win.__gpp("addEventListener", cy.stub().as("gppListener"));
        });

        cy.get("@gppListener")
          .should("have.been.calledOnce")
          .its("lastCall.args")
          .then(([data, success]) => {
            expect(success).to.eql(true);
            expect(data.eventName).to.eql("listenerRegistered");
            const { cmpDisplayStatus, signalStatus, gppString } = data.pingData;
            expect(cmpDisplayStatus).to.eql("visible");
            expect(signalStatus).to.eql("not ready");
            expect(gppString).to.eql("DBAA"); // empty string, header only
          });

        cy.get("button").contains("Opt in to all").click();
        cy.get("@FidesUpdated").should("have.been.calledOnce");

        const expected = [
          { eventName: "cmpDisplayStatus", data: "hidden" },
          { eventName: "sectionChange", data: "tcfeuv2" },
          { eventName: "signalStatus", data: "ready" },
        ];

        cy.get("@gppListener")
          .its("args")
          .then((args) => {
            expect(args.length).to.eql(4);
            // we already checked the first arg, so inspect the other three
            [args[1], args[2], args[3]].forEach(([data, success], idx) => {
              expect(success).to.eql(true);
              expect(data.eventName).to.eql(expected[idx].eventName);
              expect(data.data).to.eql(expected[idx].data);
            });
            // The gpp string should also have an extra section now and the header should
            // indicate TCF
            expect(args[3][0].pingData.gppString).to.contain("DBABMA~");
          });
      });
    });

    /**
     * Follows the flow documented here for Event Order Example 2:
     * https://github.com/InteractiveAdvertisingBureau/Global-Privacy-Platform/blob/main/Core/CMP%20API%20Specification.md#eventlistener-
     * 1. initial data from stub
     * 2. listenerRegistered
     * 3. cmpStatus = loaded
     * 4. signalStatus = ready
     * 5. User opens the consent layer to change their voice
     * 6. signalStatus = not ready
     * 7. cmpDisplayStatus = visible
     * 8. User makes their choice
     * 9. cmpDisplayStatus = hidden
     * 10. sectionChange = tcfeuv2
     * 11. signalStatus = ready
     */
    it("fires appropriate gpp events for returning user", () => {
      const tcString = "CPziCYAPziCYAGXABBENATEIAACAAAAAAAAAABEAAAAA";
      // Set a cookie to mimic a returning user
      const cookie = mockCookie({
        tcf_version_hash: TCF_VERSION_HASH,
        fides_string: tcString,
      });
      cy.setCookie(CONSENT_COOKIE_NAME, JSON.stringify(cookie));
      cy.fixture("consent/experience_tcf.json").then((experience) => {
        stubConfig({
          options: {
            isOverlayEnabled: true,
            tcfEnabled: true,
            gppEnabled: true,
          },
          experience: experience.items[0],
        });
      });

      cy.waitUntilFidesInitialized().then(() => {
        cy.get("@FidesUIShown").should("not.have.been.called");
        // TODO(PROD#1439): Because the stub is too late right now, we can't listen for events
        // 3 and 4 yet.
        cy.window().then((win) => {
          win.__gpp("addEventListener", cy.stub().as("gppListener"));
        });

        // Check initial data which should signal Ready and have the cookie's TC string
        cy.get("@gppListener")
          .should("have.been.calledOnce")
          .its("lastCall.args")
          .then(([data, success]) => {
            expect(success).to.eql(true);
            expect(data.eventName).to.eql("listenerRegistered");
            const { cmpDisplayStatus, signalStatus, gppString, cmpStatus } =
              data.pingData;
            expect(cmpStatus).to.eql("loaded");
            expect(cmpDisplayStatus).to.eql("hidden");
            expect(signalStatus).to.eql("ready");
            expect(gppString).to.contain(tcString);
          });

        // User opens the modal so signal should be "not ready" and display should be "visible"
        cy.get("#fides-modal-link").click();
        cy.get("@gppListener")
          .its("args")
          .then((args) => {
            expect(args.length).to.eql(3);
            const expected = [
              { eventName: "signalStatus", data: "not ready" },
              { eventName: "cmpDisplayStatus", data: "visible" },
            ];
            [args[1], args[2]].forEach(([data, success], idx) => {
              expect(success).to.eql(true);
              expect(data.eventName).to.eql(expected[idx].eventName);
              expect(data.data).to.eql(expected[idx].data);
            });
          });

        // User makes a choice
        cy.getByTestId("consent-modal").within(() => {
          cy.get("button").contains("Opt out of all").click();
          cy.get("@FidesUpdated").should("have.been.calledOnce");
        });
        cy.get("@gppListener")
          .its("args")
          .then((args) => {
            expect(args.length).to.eql(6);
            const expected = [
              { eventName: "cmpDisplayStatus", data: "hidden" },
              { eventName: "sectionChange", data: "tcfeuv2" },
              { eventName: "signalStatus", data: "ready" },
            ];
            [args[3], args[4], args[5]].forEach(([data, success], idx) => {
              expect(success).to.eql(true);
              expect(data.eventName).to.eql(expected[idx].eventName);
              expect(data.data).to.eql(expected[idx].data);
            });
            // Check that the TC string changed-still the same header, but different contents
            const { gppString } = args[5][0].pingData;
            expect(gppString).to.contain("DBABMA~");
            expect(gppString).not.to.contain(tcString);
          });
      });
    });

    /**
     * Expected flow for a returning user who opens but then closes the modal without making a change:
     * 1. listenerRegistered
     * 2. User opens the modal
     * 3. signalStatus = not ready
     * 4. cmpDisplayStatus = visible
     * 5. User closes the modal without saving anything
     * 6. cmpDisplayStatus = hidden
     * 7. signalStatus = ready
     */
    it("can handle returning user closing the modal without a preference change", () => {
      const cookie = mockCookie({
        tcf_version_hash: TCF_VERSION_HASH,
      });
      cy.setCookie(CONSENT_COOKIE_NAME, JSON.stringify(cookie));
      cy.fixture("consent/experience_tcf.json").then((experience) => {
        stubConfig({
          options: {
            isOverlayEnabled: true,
            tcfEnabled: true,
            gppEnabled: true,
          },
          experience: experience.items[0],
        });
      });
      cy.waitUntilFidesInitialized().then(() => {
        cy.window().then((win) => {
          win.__gpp("addEventListener", cy.stub().as("gppListener"));
        });
        cy.get("#fides-modal-link").click();
        const expected = [
          { eventName: "listenerRegistered", data: true },
          { eventName: "signalStatus", data: "not ready" },
          { eventName: "cmpDisplayStatus", data: "visible" },
          { eventName: "cmpDisplayStatus", data: "hidden" },
          { eventName: "signalStatus", data: "ready" },
        ];
        cy.get("@gppListener")
          .its("args")
          .then(
            (
              args: [{ eventName: string; data: string | boolean }, boolean][]
            ) => {
              args.forEach(([data, success], idx) => {
                expect(success).to.eql(true);
                expect(data.eventName).to.eql(expected[idx].eventName);
                expect(data.data).to.eql(expected[idx].data);
              });
            }
          );
      });
    });
  });

  describe("with TCF disabled and GPP enabled", () => {
    beforeEach(() => {
      stubConfig({
        options: {
          isOverlayEnabled: true,
          tcfEnabled: false,
          gppEnabled: true,
        },
      });
    });

    it("loads the gpp extension if it is enabled", () => {
      cy.waitUntilFidesInitialized().then(() => {
        cy.get("@FidesUIShown").should("have.been.calledOnce");
        cy.get("div#fides-banner").should("be.visible");
        cy.window().then((win) => {
          win.__gpp("ping", cy.stub().as("gppPing"));
          cy.get("@gppPing")
            .should("have.been.calledOnce")
            .its("lastCall.args")
            .then(([data, success]) => {
              expect(success).to.eql(true);
              expect(data.signalStatus).to.eql("not ready");
            });
        });
      });
    });
  });
});
