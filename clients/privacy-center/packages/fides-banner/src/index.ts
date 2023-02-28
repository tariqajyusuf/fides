import habitat from "preact-habitat";

import Widget from "./components/Widget";

const _habitat = habitat(Widget);

_habitat.render({
  selector: '[data-widget-host="fides-banner"]',
  clean: true,
});
