/**
 * Fides-tcf.js: Javascript library for Fides (https://github.com/ethyca/fides), including
 * features for supporting the Transparency Consent Framework
 *
 * This JS module provides easy access to interact with Fides from a webpage, including the ability to:
 * - initialize the page with default consent options (e.g. opt-out of advertising cookies, opt-in to analytics, etc.)
 * - read/write the current user's consent preferences to their browser as a cookie
 * - push the current user's consent preferences to other systems via integrations (Google Tag Manager, Meta, etc.)
 *
 * See https://fid.es for more information!
 *
 * Basic usage of this module in an HTML page is:
 * ```
 * <script src="https://privacy.{company}.com/fides.js"></script>
 * <script>
 *   window.Fides.init({
 *     consent: {
 *       options: [{
 *         cookieKeys: ["data_sales"],
 *         default: true,
 *         fidesDataUseKey: "advertising"
 *       }]
 *     },
 *     experience: {},
 *     geolocation: {},
 *     options: {
 *           debug: true,
 *           isDisabled: false,
 *           isGeolocationEnabled: false,
 *           geolocationApiUrl: "",
 *           overlayParentId: null,
 *           modalLinkId: null,
 *           privacyCenterUrl: "http://localhost:3000"
 *         }
 *   });
 * </script>
 * ```
 *
 * ...and later:
 * ```
 * <script>
 *   // Query user consent preferences
 *   if (window.Fides.consent.data_sales) {
 *     // ...enable advertising scripts
 *   }
 * ```
 */
import type { TCData } from "@iabtechlabtcf/cmpapi";
import { gtm } from "./integrations/gtm";
import { meta } from "./integrations/meta";
import { shopify } from "./integrations/shopify";

import { FidesConfig, PrivacyExperience } from "./lib/consent-types";

import { tcf } from "./lib/tcf";
import {
  getInitialCookie,
  getInitialFides,
  initialize,
} from "./lib/initialize";
import type { Fides } from "./lib/initialize";
import { dispatchFidesEvent } from "./lib/events";
import { FidesCookie, hasSavedTcfPreferences, isNewFidesCookie } from "./fides";
import { renderOverlay } from "./lib/tcf/renderOverlay";

declare global {
  interface Window {
    Fides: Fides;
    __tcfapiLocator?: Window;
    __tcfapi?: (
      command: string,
      version: number,
      callback: (tcData: TCData, success: boolean) => void,
      parameter?: number | string
    ) => void;
  }
}

// The global Fides object; this is bound to window.Fides if available
// eslint-disable-next-line no-underscore-dangle,@typescript-eslint/naming-convention
let _Fides: Fides;

const updateCookie = async (
  oldCookie: FidesCookie,
  experience: PrivacyExperience
): Promise<FidesCookie> => {
  // First check if the user has never consented before
  if (!hasSavedTcfPreferences(experience)) {
    return { ...oldCookie, tc_string: "" };
  }

  // Usually at this point, we'd look at the Experience from the backend and update
  // the user's browser cookie to match the preferences in the Experience. However,
  // TCF requires pre-fetching an experience. A prefetch'd experience will never have user
  // specific consents. We rely on the cookie to fill those in. Therefore, we do nothing
  // here, since the cookie is the source of truth, not the backend Experience.
  return oldCookie;
};

/**
 * Initialize the global Fides object with the given configuration values
 */
const init = async (config: FidesConfig) => {
  const cookie = getInitialCookie(config);
  const initialFides = getInitialFides({ ...config, cookie });
  if (initialFides) {
    Object.assign(_Fides, initialFides);
    dispatchFidesEvent("FidesInitialized", cookie, config.options.debug);
    dispatchFidesEvent("FidesUpdated", cookie, config.options.debug);
  }
  const experience = initialFides?.experience ?? config.experience;
  const updatedFides = await initialize({
    ...config,
    experience,
    cookie,
    renderOverlay,
    updateCookie,
  });
  Object.assign(_Fides, updatedFides);

  // Dispatch the "FidesInitialized" event to update listeners with the initial
  // state. Skip if we already initialized due to an existing cookie.
  // For convenience, also dispatch the "FidesUpdated" event; this allows
  // listeners to ignore the initialization event if they prefer
  if (isNewFidesCookie(cookie)) {
    dispatchFidesEvent("FidesInitialized", cookie, config.options.debug);
  }
  dispatchFidesEvent("FidesUpdated", cookie, config.options.debug);

  tcf();
};

// The global Fides object; this is bound to window.Fides if available
_Fides = {
  consent: {},
  experience: undefined,
  geolocation: {},
  options: {
    debug: true,
    isOverlayEnabled: false,
    isPrefetchEnabled: false,
    isGeolocationEnabled: false,
    geolocationApiUrl: "",
    overlayParentId: null,
    modalLinkId: null,
    privacyCenterUrl: "",
    fidesApiUrl: "",
    serverSideFidesApiUrl: "",
    tcfEnabled: true,
  },
  fides_meta: {},
  identity: {},
  tcf_consent: {},
  gtm,
  init,
  initialized: false,
  meta,
  shopify,
};

if (typeof window !== "undefined") {
  window.Fides = _Fides;
}

// Export everything from ./lib/* to use when importing fides-tcf.mjs as a module
export * from "./components";
export * from "./lib/consent";
export * from "./lib/consent-context";
export * from "./lib/consent-types";
export * from "./lib/consent-utils";
export * from "./lib/consent-value";
export * from "./lib/cookie";
export * from "./lib/events";