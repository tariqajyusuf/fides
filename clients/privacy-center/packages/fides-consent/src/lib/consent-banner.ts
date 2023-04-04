import {Component, render, VNode} from 'preact';
import {html} from 'htm/preact'
import {CookieKeyConsent, hasSavedConsentCookie, setConsentCookieAcceptAll, setConsentCookieRejectAll,} from "./cookie";


export type ConsentBannerOptions = {
  // Whether or not debug log statements should be enabled
  debug?: boolean

  // API URL to use for obtaining user geolocation. Must be provided if isGeolocationEnabled = true
  // Expects this API to accept a basic HTTP GET and return a UserGeolocation response, e.g.
  // ```bash
  // curl "https://example-geolocation.com/getlocation?api_key=123"
  // {"country":"US","ip":"192.168.0.1:1234","location":"US-NY","region":"NY"}
  // ```
  geolocationApiUrl?: string

  // Whether or not the banner should be globally disabled
  isDisabled?: boolean 

  // Whether user geolocation should be enabled. Requires geolocationApiUrl
  isGeolocationEnabled?: boolean

  // List of country codes where the banner should be enabled. Requires isGeolocationEnabled = true
  isEnabledCountries?: string[]

  // Display labels used for the banner text
  labels?: {
    bannerDescription?: string
    primaryButton?: string
    secondaryButton?: string
    tertiaryButton?: string
  }

  // URL for the Privacy Center, used to customize consent preferences. Required.
  privacyCenterUrl?: string
};

export type UserGeolocation = {
  country?: string  // "US"
  ip?: string // "192.168.0.1:12345"
  location?: string // "US-NY"
  region?: string // "NY"
}

// Adapted from https://gist.github.com/henrik/1688572?permalink_comment_id=4317520#gistcomment-4317520o
// (NOTE: Surprisingly, there's not really a list of these anywhere easily...?)
const EU_COUNTRY_CODES = [
  "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "EL", "HU",
  "IE", "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES",
  "SE", "UK",

  // ...plus some aliases that might occur (see https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Imperfect_implementations)
  "GB",
  "GR", 

  // ...plus EEA countries
  "CH",
  "IS",
  "LI",
  "NO",
];

/**
 * Configuration options used for the consent banner. The default values (below)
 * will be mutated by the banner() function to override with any user-provided
 * options at runtime.
 * 
 * This is effectively a global variable, but we provide getter/setter functions
 * to make it seem safer and only export the getBannerOptions() one outside this
 * module.
 */
let globalBannerOptions: ConsentBannerOptions = {
  debug: true,
  geolocationApiUrl: "http://localhost:3000/location", // TODO: default?
  isDisabled: false,
  isGeolocationEnabled: false,
  isEnabledCountries: EU_COUNTRY_CODES,
  labels: {
    bannerDescription: "This website processes your data respectfully, so we require your consent to use cookies.",
    primaryButton: "Accept All",
    secondaryButton: "Reject All",
    tertiaryButton: "Manage Preferences",
  },
  privacyCenterUrl: "http://localhost:3000" // TODO: default?
};

/**
 * Get the configured options for the consent banner 
 */
export const getBannerOptions = (): ConsentBannerOptions => globalBannerOptions;

/**
 * Wrapper around 'console.log' that only logs output when the 'debug' banner
 * option is truthy
 */
type ConsoleLogParameters = Parameters<typeof console.log>
const debugLog = (...args: ConsoleLogParameters): void => {
  if (getBannerOptions().debug) {
    // eslint-disable-next-line no-console
    console.log(...args) // TODO: use console.debug instead?
  }
};

/**
 * Change the consent banner options.
 *
 * WARNING: If called after `banner()` has already ran, many of these options
 * will no longer take effect!
 */
const setBannerOptions = (options: ConsentBannerOptions): void => {
  globalBannerOptions = options;
};

/**
 * Validate the banner options. This checks for errors like using geolocation
 * without an API
 */
const validateBannerOptions = (options: ConsentBannerOptions): boolean => {
  // Check if options is an invalid type
  if (options === undefined || typeof options !== "object") {
    return false;
  }

  if (options.geolocationApiUrl) {
    try {
      // eslint-disable-next-line no-new
      new URL(options.geolocationApiUrl);
    } catch (e) {
      debugLog("Invalid banner options: geolocationApiUrl is an invalid URL!", options);
      return false;
    }
  }

  if (options.isGeolocationEnabled && !options.geolocationApiUrl) {
    debugLog("Invalid banner options: isGeolocationEnabled = true requires geolocationApiUrl!", options);
    return false;
  }

  if (typeof options.labels === "object") {
    let validLabels = true;
    Object.entries(options.labels).forEach((value: [string, string]) => {
      if (typeof value[1] !== "string") {
        debugLog(`Invalid banner options: labels.${value[0]} is not a string!`);
        validLabels = false;
      }
    });

    if (!validLabels) {
      return false;
    }
  }

  if (!options.privacyCenterUrl) {
    debugLog("Invalid banner options: privacyCenterUrl is required!");
    return false;
  }

  if (options.privacyCenterUrl) {
    try {
      // eslint-disable-next-line no-new
      new URL(options.privacyCenterUrl);
    } catch (e) {
      debugLog("Invalid banner options: geolocationApiUrl is an invalid URL!", options);
      return false;
    }
  }

  return true;
}

/**
 * Navigates to the Fides Privacy Center to manage consent settings
 */
const navigateToPrivacyCenter = (): void => {
  const options: ConsentBannerOptions = getBannerOptions();
  debugLog("Navigate to Privacy Center URL:", options.privacyCenterUrl);
  if (options.privacyCenterUrl) {
    window.location.assign(options.privacyCenterUrl);
  }
}

/**
 * Fetch the user's geolocation from an external API
 */
const getLocation = async (): Promise<UserGeolocation> => {
  debugLog("Running getLocation...");
  const options = getBannerOptions();
  if (!options.geolocationApiUrl) {
    debugLog("Missing geolocationApiUrl, cannot get location!");
    return {};
  }

  debugLog(`Calling geolocation API: GET ${options.geolocationApiUrl}...`);
  const fetchOptions: RequestInit = {
    mode: "cors"
  };
  const response = await fetch(options.geolocationApiUrl,fetchOptions);

  if (!response.ok) {
    debugLog("Error getting location from geolocation API, returning {}. Response:", response);
    return {};
  }

  try {
    const body = await response.json();
    debugLog("Got location response from geolocation API, returning:", body);
    return body;
  } catch (e) {
    debugLog("Error parsing response body from geolocation API, returning {}. Response:", response);
    return {};
  }
}

/**
 * Determine whether or not the banner should be enabled for the given location
 */
const isBannerEnabledForLocation = (location?: UserGeolocation): boolean => {
  const options = getBannerOptions();
  if (location === undefined || !location) {
    debugLog("Location unknown, assume banner must be shown. isBannerEnabledForLocation = true");
    return true;
  }

  // Get the user's country
  if (location.country === undefined || !location.country) {
    debugLog("Country unknown, assume banner must be shown. isBannerEnabledForLocation = true");
    return true;
  }

  if (options.isEnabledCountries) {
    if (options.isEnabledCountries.includes(location.country)) {
      debugLog(`Country ${location.country} included in isEnabledCountries, banner must be shown. isBannerEnabledForLocation = true`);
      return true;
    }
    debugLog(`Country ${location.country} not included in isEnabledCountries, banner must be hidden. isBannerEnabledForLocation = false`);
    return false;
  }

  debugLog("No location-specific rules matched, assume banner must be shown. isBannerEnabledForLocation = true");
  return true;
}




/**
 * Builds a 'style' element containing the CSS styles for the consent banner
 */
const buildStyles = (): VNode => html`<link rel="stylesheet" href="banner.css">`;

interface BannerProps {
  defaults: CookieKeyConsent;
  extraOptions?: ConsentBannerOptions;
}

interface BannerState {
  isShown: boolean
}

class Banner extends Component<BannerProps, BannerState> {

  /**
   * Builds a button DOM element with the given id, class name, and text label
   */
  static buildButton = (id: string, className: string, label?: string, onClick?: () => void): VNode =>
      html`<button id="${id}" class="fides-consent-banner-button ${className}" onClick="${onClick ? onClick() : null}">
  ${label || ""}
    </button>`;

  private readonly defaults: CookieKeyConsent;

  private readonly extraOptions?: ConsentBannerOptions;

  constructor(props: BannerProps) {
    super(props);
    this.state = { isShown: false };
    this.defaults = props.defaults;
    this.extraOptions = props.extraOptions;
  }


  /**
   * Builds the DOM elements for the consent banner (container, buttons, etc.) and
   * return a single div that can be added to the body.
   */
  buildBanner = (defaults: CookieKeyConsent): VNode => {
    const options: ConsentBannerOptions = getBannerOptions();
    // TODO: support option to specify top/bottom

    return html`<div id="fides-consent-banner" class="fides-consent-banner fides-consent-banner-bottom ${this.state.isShown ? '' : 'fides-consent-banner-hidden'}">
  <div id=fides-consent-banner-description" class="fides-consent-banner-description">
    ${options.labels?.bannerDescription || ""}
  </div>
  <div id="fides-consent-banner-buttons" class="fides-consent-banner-buttons">
    ${Banner.buildButton(
        "fides-consent-banner-button-tertiary",
        "fides-consent-banner-button-tertiary",
        options.labels?.tertiaryButton,
        navigateToPrivacyCenter,
    )}
    ${Banner.buildButton(
        "fides-consent-banner-button-secondary",
        "fides-consent-banner-button-secondary",
        options.labels?.secondaryButton,
        () => {
          setConsentCookieRejectAll(defaults);
          this.setState({ isShown: false })
          // TODO: save to Fides consent request API
          // eslint-disable-next-line no-console
          console.error("Could not save consent record to Fides API, not implemented!");
        },
    )}
    ${Banner.buildButton(
        "fides-consent-banner-button-primary",
        "fides-consent-banner-button-primary",
        options.labels?.primaryButton,
        () => {
          setConsentCookieAcceptAll(defaults);
          this.setState({ isShown: false })
          // TODO: save to Fides consent request API
          // eslint-disable-next-line no-console
          console.error("Could not save consent record to Fides API, not implemented!");
        },
    )}
  </div>
</div>`;
  };

  render(): VNode | null {
   let bannerBuild = null
    // If the user provides any extra options, override the defaults
    try {
      debugLog("Initializing Fides consent banner with consent cookie defaults...", this.defaults);
      if (this.extraOptions !== undefined) {
        if (typeof this.extraOptions !== "object") {
          // eslint-disable-next-line no-console
          console.error("Invalid 'extraOptions' arg for Fides.banner(), ignoring", this.extraOptions);
        } else {
          setBannerOptions({...getBannerOptions(), ...this.extraOptions});
        }
      }
      const options: ConsentBannerOptions = getBannerOptions();

      debugLog("Validating Fides consent banner options...", options);
      if (!validateBannerOptions(options)) {
        return null;
      }

      if (options.isDisabled) {
        debugLog("Fides consent banner is disabled, skipping banner initialization!");
        return null;
      }

      if (hasSavedConsentCookie()) {
        debugLog("Fides consent cookie already exists, skipping banner initialization!");
        return null;
      }

      debugLog("Fides consent banner is enabled and consent cookie does not exist. Continuing...");

      // if (options.isGeolocationEnabled) {
      //   debugLog("Fides consent banner geolocation is enabled. Getting user location...");
      //   const location = await getLocation();
      //
      //   debugLog("Checking if Fides consent banner should be displayed for location:", location);
      //   if (!isBannerEnabledForLocation(location)) {
      //     debugLog("Fides consent banner is not enabled for location, skipping banner initialization!");
      //     return;
      //   }
      // } else {
      //   debugLog("Fides consent banner geolocation is not enabled. Continuing...");
      // }
      // Show the banner after a small delay, to allow animation to occur
      setTimeout(() => this.setState({ isShown: true }), 100);

      debugLog("Fides consent banner should be shown! Building banner elements & styles...");
      bannerBuild = this.buildBanner(this.defaults);
    } catch (e) {
      console.log(e)
    }
    return bannerBuild

  }
}

/**
 * Initialize the Fides Consent Banner, with optional extraOptions to override defaults.
 *
 * (see the type definition of ConsentBannerOptions for what options are available)
 */
export const InitBanner = async(defaults: CookieKeyConsent, extraOptions?: ConsentBannerOptions): Promise<void> => {
  const styles = buildStyles();

  debugLog("Adding Fides consent banner CSS & HTML into the DOM...");
  render(styles, document.head);
  try {
    const banner = new Banner({defaults, extraOptions})
    render(banner, document.body);
    console.log(banner)
  } catch (e) {
    debugLog(e)
  }

  debugLog("Fides consent banner is now showing!");
};



